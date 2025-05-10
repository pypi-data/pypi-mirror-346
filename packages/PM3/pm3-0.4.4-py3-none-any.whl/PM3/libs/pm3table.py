from PM3.model.pm3_protocol import ION
from PM3.model.process import Process
from tinydb import where
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from tinydb import TinyDB
import logging
import hashlib
import gzip
import os
from configparser import ConfigParser

logger = logging.getLogger(__name__)

def hidden_proc(x: str) -> bool:
    return x.startswith('__') and x.endswith('__')

class Pm3Database:
    def __init__(self, db_path: str, backup_dir: Optional[str] = None):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir) if backup_dir else self.db_path.parent / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._db: Optional[TinyDB] = None
        self._table = None
        self._last_backup_hash = None
        
        # Leggi il numero massimo di backup dal file di configurazione
        config = ConfigParser()
        config_file = Path('~/.pm3/config.ini').expanduser()
        if config_file.exists():
            config.read(config_file)
            self.max_backups = int(config['main_section'].get('max_backups', '20'))
        else:
            self.max_backups = 20  # Valore predefinito se il file di configurazione non esiste

    def _calculate_file_hash(self, file_path: Path, is_compressed: bool = False) -> str:
        """Calcola l'hash SHA-256 di un file, gestendo sia file normali che compressi."""
        sha256_hash = hashlib.sha256()
        try:
            if is_compressed:
                with gzip.open(file_path, 'rb') as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
            else:
                with open(file_path, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Errore durante il calcolo dell'hash del file {file_path}: {e}")
            return ""

    def _get_latest_backup(self) -> Tuple[Optional[Path], Optional[str]]:
        """Trova l'ultimo backup disponibile e il suo hash."""
        try:
            backups = sorted(self.backup_dir.glob(f"{self.db_path.stem}_*.json.gz"))
            if not backups:
                return None, None
            
            latest_backup = backups[-1]
            backup_hash = self._calculate_file_hash(latest_backup, is_compressed=True)
            return latest_backup, backup_hash
        except Exception as e:
            logger.error(f"Errore nel recupero dell'ultimo backup: {e}")
            return None, None

    def _compress_file(self, source_path: Path, dest_path: Path) -> bool:
        """Comprime un file usando gzip."""
        try:
            with open(source_path, 'rb') as f_in:
                with gzip.open(dest_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True
        except Exception as e:
            logger.error(f"Errore durante la compressione del file: {e}")
            return False

    def _decompress_file(self, source_path: Path, dest_path: Path) -> bool:
        """Decomprime un file gzip."""
        try:
            with gzip.open(source_path, 'rb') as f_in:
                with open(dest_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True
        except Exception as e:
            logger.error(f"Errore durante la decompressione del file: {e}")
            return False

    def _create_backup(self) -> bool:
        """Crea una copia di backup del database prima di una modifica."""
        try:
            if not self.db_path.exists():
                return True

            # Verifica che il file sia un JSON valido prima di fare il backup
            try:
                with open(self.db_path, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Database corrotto: {e}")
                return False

            # Calcola l'hash del file corrente
            current_hash = self._calculate_file_hash(self.db_path, is_compressed=False)

            # Se l'hash è uguale all'ultimo backup, non creare un nuovo backup
            if current_hash == self._last_backup_hash:
                logger.debug("Nessuna modifica rilevata, backup non necessario")
                return True

            # Crea il nuovo backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_backup_path = self.backup_dir / f"{self.db_path.stem}_{timestamp}.json"
            backup_path = self.backup_dir / f"{self.db_path.stem}_{timestamp}.json.gz"
            
            # Prima crea una copia temporanea non compressa
            shutil.copy2(self.db_path, temp_backup_path)
            
            # Poi comprimi il file
            if not self._compress_file(temp_backup_path, backup_path):
                temp_backup_path.unlink()
                return False
            
            # Rimuovi il file temporaneo
            temp_backup_path.unlink()
            
            # Verifica che il backup compresso sia valido
            try:
                with gzip.open(backup_path, 'rt') as f:
                    json.load(f)
            except Exception as e:
                logger.error(f"Backup compresso non valido: {e}")
                backup_path.unlink()
                return False
            
            self._last_backup_hash = current_hash
            logger.debug(f"Backup compresso creato: {backup_path}")

            # Rimuovi i backup più vecchi
            self._cleanup_old_backups()
            
            return True
        except Exception as e:
            logger.error(f"Errore durante la creazione del backup: {e}")
            return False

    def _cleanup_old_backups(self):
        """Rimuove i backup più vecchi mantenendo solo gli ultimi N."""
        try:
            backups = sorted(self.backup_dir.glob(f"{self.db_path.stem}_*.json.gz"))
            if len(backups) > self.max_backups:
                for old_backup in backups[:-self.max_backups]:
                    old_backup.unlink()
                    logger.debug(f"Rimosso vecchio backup: {old_backup}")
        except Exception as e:
            logger.error(f"Errore durante la pulizia dei vecchi backup: {e}")

    def _validate_json(self, data: Dict[str, Any]) -> bool:
        """Valida che i dati siano un JSON valido."""
        try:
            json.dumps(data)
            return True
        except (TypeError, ValueError) as e:
            logger.error(f"Errore di validazione JSON: {e}")
            return False

    def get_db(self) -> TinyDB:
        """Ottiene l'istanza del database, creandola se necessario."""
        if self._db is None:
            self._db = TinyDB(self.db_path)
            # Inizializza l'hash dell'ultimo backup
            if self.db_path.exists():
                self._last_backup_hash = self._calculate_file_hash(self.db_path, is_compressed=False)
        return self._db

    def get_table(self, table_name: str):
        """Ottiene una tabella dal database."""
        if self._table is None:
            self._table = self.get_db().table(table_name)
        return self._table

    def safe_write(self, operation: callable, *args, **kwargs) -> bool:
        """Esegue un'operazione di scrittura sul database in modo sicuro."""
        if not self._create_backup():
            return False

        try:
            result = operation(*args, **kwargs)
            # Verifica che il database sia ancora un JSON valido dopo la modifica
            with open(self.db_path, 'r') as f:
                json.load(f)
            return result
        except Exception as e:
            logger.error(f"Errore durante l'operazione di scrittura: {e}")
            return False

class Pm3Table:
    def __init__(self, tbl, db_path: str):
        self.tbl = tbl
        self.db = Pm3Database(db_path)

    def next_id(self, start_from=None):
        if start_from:
            # Next Id start from specific id
            pm3_id = start_from
            while self.check_exist(pm3_id):
                pm3_id += 1
            return pm3_id
        else:
            if len(self.tbl.all()) > 0:
                return max([i['pm3_id'] for i in self.tbl.all()])+1
            else:
                return 1

    def check_exist(self, val, col='pm3_id'):
        return self.tbl.contains(where(col) == val)

    def select(self, proc, col='pm3_id'):
        return self.tbl.get(where(col) == proc.dict()[col])

    def delete(self, proc, col='pm3_id'):
        if self.select(proc, col):
            return self.db.safe_write(
                lambda: self.tbl.remove(where(col) == proc.dict()[col])
            )
        return False

    def update(self, proc, col='pm3_id'):
        if self.select(proc, col):
            return self.db.safe_write(
                lambda: self.tbl.update(proc, where(col) == proc.dict()[col])
            )
        return False

    def find_id_or_name(self, id_or_name, hidden=False) -> ION:
        if id_or_name == 'all':
            # Tutti (nascosti esclusi)
            out = ION('special',
                      id_or_name,
                      [Process(**i) for i in self.tbl.all() if not hidden_proc(i['pm3_name'])]
                      )
            return out

        elif id_or_name == 'ALL':
            # Proprio tutti (compresi i nascosti)
            out = ION('special', id_or_name, [Process(**i) for i in self.tbl.all()])
            return out

        elif id_or_name == 'hidden_only':
            # Solo i nascosti (nascosti esclusi)
            out = ION('special',
                      id_or_name,
                      [Process(**i) for i in self.tbl.all() if hidden_proc(i['pm3_name'])]
                      )
            return out

        elif id_or_name == 'autorun_only':
            # Tutti gli autorun (compresi i sospesi)
            out = ION('special',
                      id_or_name,
                      [Process(**i) for i in self.tbl.all() if i['autorun'] is True])
            return out
        elif id_or_name == 'autorun_enabled':
            # Gruppo di autorun non sospesi
            out = ION('special',
                      id_or_name,
                      [Process(**i) for i in self.tbl.all() if i['autorun'] is True and i['autorun_exclude'] is False])
            return out

        try:
            id_or_name = int(id_or_name)
        except ValueError:
            if self.check_exist(id_or_name, col='pm3_name'):
                p_data = self.tbl.get(where('pm3_name') == id_or_name)
                out = ION('pm3_name', id_or_name, [Process(**p_data), ])
            else:
                out = ION('pm3_name', id_or_name, [])

        else:
            if self.check_exist(id_or_name, col='pm3_id'):
                p_data = self.tbl.get(where('pm3_id') == id_or_name)
                out = ION('pm3_id', id_or_name, [Process(**p_data), ])
            else:
                out = ION('pm3_id', id_or_name, [])
        return out
