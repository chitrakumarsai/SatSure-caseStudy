"""
Data transformation module for climate analysis.
"""
import pandas as pd

class DataTransformer:
    def transform(self, data: dict) -> dict:
        """Transform raw data into analysis-ready format"""
        transformed = {}
        
        # Monthly aggregates
        transformed['monthly'] = self._calculate_monthly_aggregates(data)
        
        # Seasonal aggregates
        transformed['seasonal'] = self._calculate_seasonal_aggregates(data)
        
        # Climate resilience indicators
        transformed['resilience'] = self._calculate_resilience_indicators(data)
        
        # Crop specific transformations
        transformed['crop'] = self._transform_crop_data(data)
        
        return transformed
        
    def _calculate_resilience_indicators(self, data: dict) -> dict:
        """Calculate climate resilience indicators"""
        indicators = {}
        
        for key, df in data.items():
            if 'precip' in key:
                # Calculate rainfall variability
                monthly = df.groupby(pd.Grouper(key='date', freq='ME'))['rainfall_mm']
                indicators[f"{key}_variability"] = monthly.std() / monthly.mean()
                
                # Calculate drought frequency
                seasonal = self._calculate_seasonal_aggregates({key: df})
                mean_rain = list(seasonal.values())[0].mean()
                drought_freq = (list(seasonal.values())[0] < 0.8 * mean_rain).mean()
                indicators[f"{key}_drought_frequency"] = drought_freq
            
            elif 'temp' in key:
                # Calculate temperature anomalies
                monthly = df.groupby(pd.Grouper(key='date', freq='ME'))['mean']
                baseline = monthly.mean()
                indicators[f"{key}_temp_anomaly"] = (monthly - baseline).abs().mean()
        
        return indicators
        
    def _transform_crop_data(self, data: dict) -> dict:
        """Transform data for crop analysis"""
        crop_data = {}
        
        # Combine rainfall and temperature data for growing seasons
        for region in ['mh', 'mp']:
            precip_df = data[f'{region}_precip']
            temp_df = data[f'{region}_temp']
            
            # Merge temperature and precipitation data
            merged = pd.merge(
                precip_df, 
                temp_df[['date', 'mean']], 
                on='date', 
                suffixes=('_rain', '_temp')
            )
            
            # Calculate growing season conditions
            merged['month'] = merged['date'].dt.month
            
            # Kharif season (June-October)
            kharif = merged[merged['month'].isin([6,7,8,9,10])]
            
            # Rabi season (November-March)
            rabi = merged[merged['month'].isin([11,12,1,2,3])]
            
            crop_data[f'{region}_kharif'] = kharif
            crop_data[f'{region}_rabi'] = rabi
        
        return crop_data
    
    def _calculate_monthly_aggregates(self, data: dict) -> dict:
        """Calculate monthly aggregates for each dataset"""
        monthly = {}
        for key, df in data.items():
            if 'precip' in key:
                monthly[f"{key}_monthly"] = df.groupby(
                    pd.Grouper(key='date', freq='ME'))['rainfall_mm'].mean()
            elif 'temp' in key:
                monthly[f"{key}_monthly"] = df.groupby(
                    pd.Grouper(key='date', freq='ME'))['mean'].mean()
        return monthly
    
    def _calculate_seasonal_aggregates(self, data: dict) -> dict:
        """Calculate seasonal aggregates for rainfall analysis"""
        seasonal = {}
        for key, df in data.items():
            if 'precip' in key:
                df = df.copy()
                df['month'] = df['date'].dt.month
                df['year'] = df['date'].dt.year
                
                # Kharif season (June-October)
                kharif = df[df['month'].isin([6,7,8,9,10])].groupby('year')['rainfall_mm'].mean()
                
                # Rabi season (November-March)
                rabi = df[df['month'].isin([11,12,1,2,3])].groupby('year')['rainfall_mm'].mean()
                
                seasonal[f"{key}_kharif"] = kharif
                seasonal[f"{key}_rabi"] = rabi
        
        return seasonal
