"""
Data validation module for climate data.
"""
import pandas as pd
import numpy as np

class DataValidator:
    def __init__(self):
        self.quality_reports = {}
        self.thresholds = {
            'rainfall_max': 150,  # mm per day
            'temp_min': -5,      # °C
            'temp_max': 50,      # °C
            'rainfall_95th': 95,  # 95th percentile for extreme events
            'dry_spell': 15      # days for dry spell
        }
    
    def validate_data(self, data: dict) -> dict:
        """Validate all datasets and return quality reports"""
        for key, df in data.items():
            self.quality_reports[key] = self._validate_dataframe(df, key)
        return self.quality_reports
    
    def _validate_dataframe(self, df: pd.DataFrame, name: str) -> dict:
        """Validate individual dataframe and return detailed report"""
        report = {
            'dataset_name': name,
            'total_records': len(df),
            'date_range': f"{df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}",
            'checks': {},
            'statistics': {},
            'anomalies': {},
            'validation_status': 'PASSED'
        }
        
        # Basic Data Quality Checks
        report['checks']['missing_values'] = self._check_missing_values(df)
        report['checks']['date_continuity'] = self._check_date_continuity(df)
        report['checks']['value_ranges'] = self._check_value_ranges(df)
        report['checks']['data_types'] = self._check_data_types(df)
        
        # Statistical Analysis
        report['statistics'] = self._calculate_statistics(df)
        
        # Anomaly Detection
        report['anomalies'] = self._detect_anomalies(df)
        
        # Overall Status
        if any(not check['status'] for check in report['checks'].values()):
            report['validation_status'] = 'FAILED'
        
        return report
    
    def _check_missing_values(self, df: pd.DataFrame) -> dict:
        """Check for missing values"""
        missing = df.isnull().sum().to_dict()
        return {
            'status': not any(missing.values()),
            'details': missing
        }
    
    def _check_date_continuity(self, df: pd.DataFrame) -> dict:
        """Check for date continuity"""
        date_range = df['date'].max() - df['date'].min()
        expected_days = date_range.days + 1
        actual_days = len(df)
        
        return {
            'status': expected_days == actual_days,
            'details': {
                'expected_days': expected_days,
                'actual_days': actual_days,
                'missing_days': expected_days - actual_days
            }
        }
    
    def _check_value_ranges(self, df: pd.DataFrame) -> dict:
        """Check value ranges"""
        checks = {}
        
        if 'rainfall_mm' in df.columns:
            rainfall_valid = ((df['rainfall_mm'] >= 0) & 
                            (df['rainfall_mm'] <= self.thresholds['rainfall_max'])).all()
            checks['rainfall'] = {
                'status': rainfall_valid,
                'details': {
                    'min': df['rainfall_mm'].min(),
                    'max': df['rainfall_mm'].max(),
                    'invalid_count': (~((df['rainfall_mm'] >= 0) & 
                                     (df['rainfall_mm'] <= self.thresholds['rainfall_max']))).sum()
                }
            }
        
        if 'mean' in df.columns:
            temp_valid = ((df['mean'] >= self.thresholds['temp_min']) & 
                         (df['mean'] <= self.thresholds['temp_max'])).all()
            checks['temperature'] = {
                'status': temp_valid,
                'details': {
                    'min': df['mean'].min(),
                    'max': df['mean'].max(),
                    'invalid_count': (~((df['mean'] >= self.thresholds['temp_min']) & 
                                     (df['mean'] <= self.thresholds['temp_max']))).sum()
                }
            }
        
        return checks
    
    def _check_data_types(self, df: pd.DataFrame) -> dict:
        """Check data types"""
        return {
            'status': pd.api.types.is_datetime64_any_dtype(df['date']),
            'details': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
    
    def _calculate_statistics(self, df: pd.DataFrame) -> dict:
        """Calculate basic statistics"""
        stats = {}
        
        if 'rainfall_mm' in df.columns:
            stats['rainfall'] = {
                'mean': df['rainfall_mm'].mean(),
                'std': df['rainfall_mm'].std(),
                'median': df['rainfall_mm'].median(),
                'q95': df['rainfall_mm'].quantile(0.95)
            }
        
        if 'mean' in df.columns:
            stats['temperature'] = {
                'mean': df['mean'].mean(),
                'std': df['mean'].std(),
                'median': df['mean'].median(),
                'extreme_days': (df['mean'] > 35).sum()
            }
            
        return stats
    
    def _detect_anomalies(self, df: pd.DataFrame) -> dict:
        """Detect anomalies in the data"""
        anomalies = {}
        
        if 'rainfall_mm' in df.columns:
            # Extreme rainfall events
            threshold = df['rainfall_mm'].quantile(0.95)
            extreme_events = df[df['rainfall_mm'] > threshold]
            
            # Dry spells
            dry_spells = self._find_dry_spells(df)
            
            anomalies['rainfall'] = {
                'extreme_events': {
                    'count': len(extreme_events),
                    'threshold': threshold,
                    'dates': extreme_events['date'].tolist()
                },
                'dry_spells': {
                    'count': len(dry_spells),
                    'max_duration': max(dry_spells) if dry_spells else 0,
                    'spells': dry_spells
                }
            }
        
        if 'mean' in df.columns:
            # Heat stress days
            heat_stress = df[df['mean'] > 35]
            cold_stress = df[df['mean'] < 15]
            
            anomalies['temperature'] = {
                'heat_stress_days': {
                    'count': len(heat_stress),
                    'dates': heat_stress['date'].tolist()
                },
                'cold_stress_days': {
                    'count': len(cold_stress),
                    'dates': cold_stress['date'].tolist()
                }
            }
            
        return anomalies
    
    def _find_dry_spells(self, df: pd.DataFrame) -> list:
        """Find dry spells (consecutive days with no/minimal rainfall)"""
        dry_days = df['rainfall_mm'] < 1
        spell_lengths = []
        current_spell = 0
        
        for is_dry in dry_days:
            if is_dry:
                current_spell += 1
            elif current_spell >= self.thresholds['dry_spell']:
                spell_lengths.append(current_spell)
                current_spell = 0
            else:
                current_spell = 0
                
        if current_spell >= self.thresholds['dry_spell']:
            spell_lengths.append(current_spell)
            
        return spell_lengths
