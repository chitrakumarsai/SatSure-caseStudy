"""
Data validation module for climate data.
"""
import pandas as pd
import numpy as np

class DataValidator:
    def __init__(self):
        self.quality_reports = {}
        self.thresholds = {
            'rainfall_max': 500,  # mm per day (increased for extreme events)
            'temp_min': -10,     # °C (lowered for winter extremes)
            'temp_max': 55,      # °C (increased for summer extremes)
            'rainfall_95th': 95, # 95th percentile for extreme events
            'dry_spell': 15,     # days for dry spell
            'missing_threshold': 0.2  # Allow up to 20% missing values
        }
    
    def validate_data(self, data: dict) -> dict:
        """Validate all datasets and return quality reports"""
        try:
            if not data:
                raise ValueError("No data provided for validation")
                
            for key, df in data.items():
                print(f"\nValidating {key}...")
                
                # Make a copy to avoid modifying original data
                df_copy = df.copy()
                
                # Initial validation
                report = self._validate_dataframe(df_copy, key)
                
                # Handle missing values if any
                missing_values = df_copy.isnull().sum()
                if missing_values.any():
                    print(f"Found missing values in {key}:")
                    for col, count in missing_values.items():
                        if count > 0:
                            print(f"  - {col}: {count} missing values")
                            
                    print("Attempting interpolation...")
                    
                    if 'rainfall_mm' in df_copy.columns:
                        df_copy['rainfall_mm'] = df_copy['rainfall_mm'].interpolate(method='linear')
                        df_copy['rainfall_mm'] = df_copy['rainfall_mm'].fillna(method='bfill').fillna(method='ffill')
                        
                    if 'mean' in df_copy.columns:
                        df_copy['mean'] = df_copy['mean'].interpolate(method='linear')
                        df_copy['mean'] = df_copy['mean'].fillna(method='bfill').fillna(method='ffill')
                    
                    # Re-validate after interpolation
                    report = self._validate_dataframe(df_copy, key)
                    
                self.quality_reports[key] = report
                print(f"Validation completed for {key}: {report['validation_status']}")
                
                # Update the original dataframe with cleaned data
                data[key] = df_copy
                
            return self.quality_reports
            
        except Exception as e:
            raise RuntimeError(f"Error during data validation: {str(e)}")
    
    def _validate_dataframe(self, df: pd.DataFrame, name: str) -> dict:
        """Validate individual dataframe and return detailed report"""
        try:
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
            missing_check = self._check_missing_values(df)
            date_check = self._check_date_continuity(df)
            range_check = self._check_value_ranges(df)
            type_check = self._check_data_types(df)
            
            report['checks'] = {
                'missing_values': missing_check,
                'date_continuity': date_check,
                'value_ranges': range_check,
                'data_types': type_check
            }
            
            # Statistical Analysis
            report['statistics'] = self._calculate_statistics(df)
            
            # Anomaly Detection
            report['anomalies'] = self._detect_anomalies(df)
            
            # Overall Status
            failed_checks = []
            if not missing_check['status']:
                failed_checks.append('missing_values')
            if not date_check['status']:
                failed_checks.append('date_continuity')
            if range_check and any(not v['status'] for v in range_check.values()):
                failed_checks.append('value_ranges')
            if not type_check['status']:
                failed_checks.append('data_types')
                
            if failed_checks:
                report['validation_status'] = 'FAILED'
                report['failed_checks'] = failed_checks
            
            return report
            
        except Exception as e:
            print(f"Error validating {name}: {str(e)}")
            return {
                'dataset_name': name,
                'validation_status': 'ERROR',
                'error_message': str(e)
            }
    
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
        
    def export_to_excel(self, output_path: str = "climate_analysis_results.xlsx"):
        """Export validation and analysis results to Excel file with multiple sheets"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Summary sheet
                summary_data = []
                for key, report in self.quality_reports.items():
                    summary_data.append({
                        'Dataset': key,
                        'Status': report['validation_status'],
                        'Total Records': report['total_records'],
                        'Date Range': report['date_range'],
                        'Failed Checks': ', '.join(report.get('failed_checks', []))
                    })
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Statistics sheet
                stats_data = []
                for key, report in self.quality_reports.items():
                    stats = report['statistics']
                    if 'rainfall' in stats:
                        stats_data.append({
                            'Dataset': key,
                            'Type': 'Rainfall',
                            'Mean': stats['rainfall']['mean'],
                            'Std Dev': stats['rainfall']['std'],
                            'Median': stats['rainfall']['median'],
                            '95th Percentile': stats['rainfall']['q95']
                        })
                    if 'temperature' in stats:
                        stats_data.append({
                            'Dataset': key,
                            'Type': 'Temperature',
                            'Mean': stats['temperature']['mean'],
                            'Std Dev': stats['temperature']['std'],
                            'Median': stats['temperature']['median'],
                            'Extreme Days': stats['temperature']['extreme_days']
                        })
                pd.DataFrame(stats_data).to_excel(writer, sheet_name='Statistics', index=False)
                
                # Anomalies sheet
                anomalies_data = []
                for key, report in self.quality_reports.items():
                    anomalies = report['anomalies']
                    if 'rainfall' in anomalies:
                        anomalies_data.append({
                            'Dataset': key,
                            'Type': 'Rainfall',
                            'Extreme Events Count': anomalies['rainfall']['extreme_events']['count'],
                            'Extreme Events Threshold': anomalies['rainfall']['extreme_events']['threshold'],
                            'Dry Spells Count': anomalies['rainfall']['dry_spells']['count'],
                            'Max Dry Spell Duration': anomalies['rainfall']['dry_spells']['max_duration']
                        })
                    if 'temperature' in anomalies:
                        anomalies_data.append({
                            'Dataset': key,
                            'Type': 'Temperature',
                            'Heat Stress Days': anomalies['temperature']['heat_stress_days']['count'],
                            'Cold Stress Days': anomalies['temperature']['cold_stress_days']['count']
                        })
                pd.DataFrame(anomalies_data).to_excel(writer, sheet_name='Anomalies', index=False)
                
                # Data Quality Checks sheet
                checks_data = []
                for key, report in self.quality_reports.items():
                    checks = report['checks']
                    checks_data.append({
                        'Dataset': key,
                        'Missing Values Status': checks['missing_values']['status'],
                        'Date Continuity Status': checks['date_continuity']['status'],
                        'Data Types Status': checks['data_types']['status'],
                        'Expected Days': checks['date_continuity']['details']['expected_days'],
                        'Actual Days': checks['date_continuity']['details']['actual_days']
                    })
                pd.DataFrame(checks_data).to_excel(writer, sheet_name='Data Quality', index=False)
                
            print(f"\nResults exported successfully to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting results to Excel: {str(e)}")
            return False
