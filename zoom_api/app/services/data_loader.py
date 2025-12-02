import os
import glob
import pandas as pd
import logging
from datetime import datetime
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class ZoomDataLoader:
    _instance = None
    _data = None
    _last_loaded = None
    _last_checked = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ZoomDataLoader, cls).__new__(cls)
        return cls._instance

    def _get_csv_files(self):
        path = settings.CSV_FOLDER_PATH
        # Support both directory with csvs and single csv file
        if os.path.isfile(path):
            return [path]
        return glob.glob(os.path.join(path, "*.csv"))

    def _needs_reload(self):
        if self._data is None:
            return True
        
        # Check for changes every 60 seconds max to avoid hitting disk too often
        now = datetime.now()
        if self._last_checked and (now - self._last_checked).total_seconds() < 60:
            return False
        
        self._last_checked = now
        
        files = self._get_csv_files()
        if not files:
            return False
            
        # Check if any file has been modified since last load
        max_mtime = max(os.path.getmtime(f) for f in files)
        last_load_timestamp = self._last_loaded.timestamp() if self._last_loaded else 0
        
        return max_mtime > last_load_timestamp

    def load_data(self):
        files = self._get_csv_files()
        if not files:
            logger.warning(f"No CSV files found in {settings.CSV_FOLDER_PATH}")
            self._data = pd.DataFrame()
            self._last_loaded = datetime.now()
            return

        dfs = []
        for f in files:
            try:
                # Read CSV, assuming standard Zoom format
                # We might need to adjust encoding or separator based on actual files
                df = pd.read_csv(f)
                dfs.append(df)
            except Exception as e:
                logger.error(f"Error reading file {f}: {e}")
        
        if dfs:
            self._data = pd.concat(dfs, ignore_index=True)
            # Basic preprocessing
            # Convert date columns if they exist
            date_cols = ['Start Time', 'End Time']
            for col in date_cols:
                if col in self._data.columns:
                    self._data[col] = pd.to_datetime(self._data[col], errors='coerce')
            
            logger.info(f"Loaded {len(self._data)} rows from {len(files)} files.")
        else:
            self._data = pd.DataFrame()
            
        self._last_loaded = datetime.now()

    def get_data(self) -> pd.DataFrame:
        if self._needs_reload():
            logger.info("Reloading data...")
            self.load_data()
        return self._data

    def get_last_updated(self):
        return self._last_loaded

# Global instance
data_loader = ZoomDataLoader()
