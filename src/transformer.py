"""
Data transformation module for climate analysis.
"""
import pandas as pd

class DataTransformer:
    def transform(self, data: dict) -> dict:
        """Transform raw data into analysis-ready format"""
        if not data or not isinstance(data, dict):
            raise ValueError("Invalid data format. Expected non-empty dictionary.")
            
        transformed = {}
        
        try:
            print("Starting monthly aggregates...")
            transformed['monthly'] = self._calculate_monthly_aggregates(data)
            print("Monthly aggregates keys:", transformed['monthly'].keys())
            
            print("Starting seasonal aggregates...")
            transformed['seasonal'] = self._calculate_seasonal_aggregates(data)
            print("Seasonal aggregates keys:", transformed['seasonal'].keys())
            
            print("Starting resilience calculations...")
            transformed['resilience'] = self._calculate_resilience_indicators(data)
            print("Resilience indicators keys:", transformed['resilience'].keys())
            
            print("Starting crop transformations...")
            transformed['crop'] = self._transform_crop_data(data)
            print("Crop data keys:", transformed['crop'].keys())
            print("Crop data content:", [f"{k}: {len(v)} rows" for k, v in transformed['crop'].items()])
            
            print("All transformations completed successfully")
            
        except Exception as e:
            raise RuntimeError(f"Error during data transformation: {str(e)}")
            
        return transformed
        
    def _calculate_resilience_indicators(self, data: dict) -> dict:
        """Calculate climate resilience indicators"""
        indicators = {}
        
        region_mapping = {
            'maharashtra': 'mh',
            'madhya_pradesh': 'mp'
        }

        for key, df in data.items():
            print(f"Processing resilience for key: {key}")
            if 'precipitation' in key:
                # Fix to handle multi-word regions
                region = key[:key.find('_precipitation')]
                print(f"Extracted region: {region}")
                short_region = region_mapping[region]
                
                # Calculate rainfall variability
                monthly_stats = df.groupby(pd.Grouper(key='date', freq='ME'))['rainfall_mm'].agg(['mean', 'std'])
                rain_var = (monthly_stats['std'] / monthly_stats['mean']).mean()
                indicators[f"{short_region}_precip_variability"] = float(rain_var)
                
                # Calculate drought frequency
                seasonal = self._calculate_seasonal_aggregates({key: df})
                first_key = list(seasonal.keys())[0]
                mean_rain = seasonal[first_key].mean()
                drought_freq = (seasonal[first_key] < 0.8 * mean_rain).mean()
                indicators[f"{short_region}_precip_drought_frequency"] = float(drought_freq)
            
            elif 'temperature' in key:
                # Fix to handle multi-word regions
                region = key[:key.find('_temperature')]
                print(f"Extracted region: {region}")
                short_region = region_mapping[region]
                
                # Calculate temperature anomalies
                monthly_means = df.groupby(pd.Grouper(key='date', freq='ME'))['mean'].mean()
                baseline = monthly_means.mean()
                temp_anomaly = abs(monthly_means - baseline).mean()
                indicators[f"{short_region}_temp_anomaly"] = float(temp_anomaly)
        
        return indicators
        
    def _transform_crop_data(self, data: dict) -> dict:
        """Transform data for crop analysis"""
        crop_data = {}
        
        # Combine rainfall and temperature data for growing seasons
        region_mapping = {
            'mh': 'maharashtra',
            'mp': 'madhya_pradesh'
        }
        for region_short, region_full in region_mapping.items():
            precip_df = data[f'{region_full}_precipitation']
            temp_df = data[f'{region_full}_temperature']
            
            print(f"Merging data for {region_full}")
            merged = pd.merge(
                precip_df, 
                temp_df[['date', 'mean']], 
                on='date', 
                suffixes=('_rain', '_temp')
            )
            print(f"Columns after merge: {merged.columns}")
            
            # Calculate growing season conditions
            merged['month'] = merged['date'].dt.month
            
            # Kharif season (June-October)
            kharif = merged[merged['month'].isin([6,7,8,9,10])]
            
            # Rabi season (November-March)
            rabi = merged[merged['month'].isin([11,12,1,2,3])]
            
            print(f"Adding crop data for region: {region_full}")
            crop_data[f'{region_full}_kharif'] = kharif
            crop_data[f'{region_full}_rabi'] = rabi
        
        return crop_data
    
    def _calculate_monthly_aggregates(self, data: dict) -> dict:
        """Calculate monthly aggregates for each dataset"""
        monthly = {}
        try:
            for key, df in data.items():
                # Ensure date is datetime
                if not pd.api.types.is_datetime64_any_dtype(df['date']):
                    df['date'] = pd.to_datetime(df['date'])
                    
                print(f"Processing monthly data for key: {key}")
                if 'precipitation' in key:
                    monthly_series = df.groupby(
                        pd.Grouper(key='date', freq='ME'))['rainfall_mm'].mean()
                    monthly[f"{key}_monthly"] = monthly_series.to_frame().reset_index()
                elif 'temperature' in key:
                    monthly_series = df.groupby(
                        pd.Grouper(key='date', freq='ME'))['mean'].mean()
                    monthly[f"{key}_monthly"] = monthly_series.to_frame().reset_index()
        except Exception as e:
            raise ValueError(f"Error in monthly aggregation: {str(e)}")
        return monthly
    
    def _calculate_seasonal_aggregates(self, data: dict) -> dict:
        """Calculate seasonal aggregates for rainfall analysis"""
        seasonal = {}
        for key, df in data.items():
            if 'precipitation' in key:
                df = df.copy()
                df['month'] = df['date'].dt.month
                df['year'] = df['date'].dt.year
                
                # Kharif season (June-October)
                kharif = df[df['month'].isin([6,7,8,9,10])].groupby('year')['rainfall_mm'].mean()
                
                # Rabi season (November-March)
                rabi = df[df['month'].isin([11,12,1,2,3])].groupby('year')['rainfall_mm'].mean()
                
                region = key.split('_')[0]
                region_short = 'mh' if region == 'maharashtra' else 'mp'
                seasonal[f"{region_short}_kharif"] = kharif
                seasonal[f"{region_short}_rabi"] = rabi
        
        return seasonal
