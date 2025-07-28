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
        try:
            data = {}
            # Load Maharashtra data
            mh_precip = self._load_csv('MH_precipitation.csv')
            mh_temp = self._load_csv('MH_temperature.csv')
            # Load Madhya Pradesh data
            mp_precip = self._load_csv('MP_precipitation.csv')
            mp_temp = self._load_csv('MP_temperature.csv')
            
            # Store with consistent keys
            data = {
                'maharashtra_precipitation': mh_precip,
                'maharashtra_temperature': mh_temp,
                'madhya_pradesh_precipitation': mp_precip,
                'madhya_pradesh_temperature': mp_temp
            }
            
            print("Data loaded successfully:")
            for key, df in data.items():
                print(f"{key}: {len(df)} records")
            
            return data
            
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")
    
    def _load_csv(self, filename: str) -> pd.DataFrame:
        """Load and basic preprocessing of CSV files"""
        try:
            file_path = self.data_path / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {filename}")
                
            # Read CSV with specific data types
            df = pd.read_csv(file_path)
            
            # Convert date column
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception as e:
                raise ValueError(f"Error converting date column in {filename}: {str(e)}")
            
            # Convert numeric columns based on file type
            if 'precipitation' in filename:
                df['rainfall_mm'] = pd.to_numeric(df['rainfall_mm'], errors='coerce')
            elif 'temperature' in filename:
                df['mean'] = pd.to_numeric(df['mean'], errors='coerce')
                
            # Check for missing values after conversion
            missing = df.isnull().sum()
            if missing.any():
                print(f"Warning: Found {missing.sum()} missing values in {filename}")
                
            return df
            
        except Exception as e:
            raise RuntimeError(f"Error loading {filename}: {str(e)}")
