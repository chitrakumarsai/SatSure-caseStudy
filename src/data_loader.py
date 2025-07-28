"""
Data loading and validation module.
"""
from pathlib import Path
import pandas as pd

class DataLoader:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        
    def load_all(self) -> dict:
        """Load all climate data files"""
        data = {}
        data['mh_precip'] = self._load_csv('MH_precipitation.csv')
        data['mh_temp'] = self._load_csv('MH_temperature.csv')
        data['mp_precip'] = self._load_csv('MP_precipitation.csv')
        data['mp_temp'] = self._load_csv('MP_temperature.csv')
        return data
    
    def _load_csv(self, filename: str) -> pd.DataFrame:
        """Load and basic preprocessing of CSV files"""
        file_path = self.data_path / filename
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
