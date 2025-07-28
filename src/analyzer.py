"""
Climate data analysis module.
"""
import pandas as pd
import numpy as np

class ClimateAnalyzer:
    def __init__(self):
        self.crop_info = {
            "Soybean": {"area": 3000000, "price": 4000, "yield": 10},
            "Cotton":  {"area": 2500000, "price": 6000, "yield": 8},
            "Wheat":   {"area": 2000000, "price": 2500, "yield": 25},
            "Gram":    {"area": 1500000, "price": 5000, "yield": 8},
            "Paddy":   {"area": 1800000, "price": 2200, "yield": 20},
        }
        
    def analyze(self, data: dict) -> dict:
        """Perform climate data analysis"""
        results = {}
        
        # Classify seasons
        results['classification'] = self._classify_seasons(data['seasonal'])
        
        # Economic impact
        results['economic_impact'] = self._calculate_economic_impact(results['classification'])
        
        # Climate resilience analysis
        results['resilience'] = self._analyze_resilience(data['resilience'])
        
        # Infrastructure vulnerability
        results['infrastructure'] = self._assess_infrastructure(data)
        
        # Crop yield predictions
        results['crop_analysis'] = self._analyze_crops(data['crop'])
        
        # Recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
        
    def _analyze_resilience(self, resilience_data: dict) -> dict:
        """Analyze climate resilience indicators"""
        analysis = {}
        
        # Calculate resilience scores (0-100)
        for region in ['mh', 'mp']:
            score = 100
            
            # Rainfall variability penalty (higher variability = lower score)
            var_penalty = resilience_data[f'{region}_precip_variability'] * 50
            score -= var_penalty
            
            # Drought frequency penalty
            drought_penalty = resilience_data[f'{region}_precip_drought_frequency'] * 100
            score -= drought_penalty
            
            # Temperature anomaly penalty
            temp_penalty = resilience_data[f'{region}_temp_temp_anomaly'] * 10
            score -= temp_penalty
            
            analysis[f'{region}_resilience_score'] = max(0, min(100, score))
            
        return analysis
        
    def _assess_infrastructure(self, data: dict) -> dict:
        """Assess infrastructure vulnerability"""
        assessment = {}
        
        for region in ['mh', 'mp']:
            # Analyze extreme weather patterns
            precip_data = data['monthly'][f'{region}_precip_monthly']
            temp_data = data['monthly'][f'{region}_temp_monthly']
            
            # Count extreme rainfall events (>95th percentile)
            extreme_rain_threshold = precip_data.quantile(0.95)
            extreme_rain_freq = (precip_data > extreme_rain_threshold).mean()
            
            # Count extreme temperature events
            extreme_temp_threshold = temp_data.quantile(0.95)
            extreme_temp_freq = (temp_data > extreme_temp_threshold).mean()
            
            # Infrastructure risk score (0-100)
            risk_score = (extreme_rain_freq * 50) + (extreme_temp_freq * 50)
            
            assessment[f'{region}_infrastructure_risk'] = min(100, risk_score * 100)
            
        return assessment
        
    def _analyze_crops(self, crop_data: dict) -> dict:
        """Analyze crop vulnerability and potential yields"""
        analysis = {}
        
        for region_season, data in crop_data.items():
            # Calculate optimal growing conditions
            optimal_temp = (data['mean'] >= 20) & (data['mean'] <= 30)
            adequate_rain = data['rainfall_mm'] >= 5  # daily minimum
            
            # Calculate stress days
            stress_days = (~optimal_temp) | (~adequate_rain)
            stress_percentage = stress_days.mean() * 100
            
            analysis[f'{region_season}_stress'] = stress_percentage
            
        return analysis
        
    def _generate_recommendations(self, results: dict) -> dict:
        """Generate region-specific recommendations"""
        recommendations = {}
        
        for region in ['mh', 'mp']:
            region_recs = []
            
            # Climate resilience recommendations
            resilience_score = results['resilience'][f'{region}_resilience_score']
            if resilience_score < 50:
                region_recs.append("Implement drought-resistant crop varieties")
                region_recs.append("Develop water conservation infrastructure")
            
            # Infrastructure recommendations
            infra_risk = results['infrastructure'][f'{region}_infrastructure_risk']
            if infra_risk > 70:
                region_recs.append("Strengthen weather monitoring systems")
                region_recs.append("Improve drainage infrastructure")
            
            # Crop-specific recommendations
            kharif_stress = results['crop_analysis'][f'{region}_kharif_stress']
            if kharif_stress > 30:
                region_recs.append("Consider shifting kharif sowing dates")
                region_recs.append("Implement soil moisture conservation practices")
            
            recommendations[region] = region_recs
            
        return recommendations
    
    def _classify_seasons(self, seasonal_data: dict) -> dict:
        """Classify seasons based on rainfall patterns"""
        classification = {}
        for key, series in seasonal_data.items():
            mean_rain = series.mean()
            classification[key] = series.apply(
                lambda x: "Drought" if x < 0.8 * mean_rain 
                else ("Excess Rain" if x > 1.2 * mean_rain else "Normal")
            )
        return classification
    
    def _calculate_economic_impact(self, classification: dict) -> pd.DataFrame:
        """Calculate economic impact based on seasonal classification"""
        impact_map = {"Drought": -20, "Excess Rain": -10, "Normal": 0}
        
        loss_data = []
        for region_key, status_series in classification.items():
            region = "Maharashtra" if "mh" in region_key else "Madhya Pradesh"
            season = "Kharif" if "kharif" in region_key else "Rabi"
            
            for year, status in status_series.items():
                for crop, vals in self.crop_info.items():
                    yield_loss_pct = impact_map[status]
                    base_yield = vals['area'] * vals['yield']
                    base_revenue = base_yield * vals['price']
                    estimated_loss = (yield_loss_pct / 100) * base_revenue
                    
                    loss_data.append([
                        region, year, season, crop, status,
                        base_yield, base_revenue, estimated_loss
                    ])
        
        return pd.DataFrame(
            loss_data,
            columns=['Region', 'Year', 'Season', 'Crop', 'Status',
                    'Base_Yield(qtl)', 'Base_Revenue(INR)',
                    'Estimated_Loss(INR)']
        )
    
    def _calculate_climate_indicators(self, monthly_data: dict) -> dict:
        """Calculate climate resilience indicators"""
        indicators = {}
        
        for key, series in monthly_data.items():
            indicators[f"{key}_variability"] = series.std() / series.mean()  # CV
            indicators[f"{key}_trend"] = np.polyfit(
                np.arange(len(series)), series.values, 1)[0]  # Linear trend
        
        return indicators
