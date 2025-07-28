"""
Data validation module for climate data.
"""
import pandas as pd
import numpy as np

class DataValidator:
    def validate_data(self, data: dict) -> bool:
        """Validate all datasets"""
        for key, df in data.items():
            self._validate_dataframe(df, key)
        return True
    
    def _validate_dataframe(self, df: pd.DataFrame, name: str):
        """Validate individual dataframe"""
        # Check for missing values
        if df.isnull().any().any():
            raise ValueError(f"Missing values found in {name}")
        
        # Check date range
        date_range = df['date'].max() - df['date'].min()
        if date_range.days < 365:
            raise ValueError(f"Insufficient date range in {name}")
        
        # Check data types
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            raise ValueError(f"Invalid date format in {name}")
        
        # Validate value ranges
        if 'rainfall_mm' in df.columns:
            if (df['rainfall_mm'] < 0).any():
                raise ValueError(f"Negative rainfall values found in {name}")
        
        if 'mean' in df.columns:  # Temperature
            if ((df['mean'] < -20) | (df['mean'] > 50)).any():
                raise ValueError(f"Temperature values out of range in {name}")
        
        return True
