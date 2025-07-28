"""
Climate resilience analysis module.
"""
import pandas as pd
import numpy as np

class ResilienceAnalyzer:
    def __init__(self):
        self.thresholds = {
            'drought_threshold': 0.8,  # 80% of normal rainfall
            'excess_threshold': 1.2,   # 120% of normal rainfall
            'temp_stress_high': 35,    # °C
            'temp_stress_low': 15,     # °C
            'min_rainfall': 5,         # mm/day
        }
    
    def calculate_resilience_score(self, rainfall: pd.Series, temperature: pd.Series) -> float:
        """Calculate overall climate resilience score"""
        rain_score = self._rainfall_resilience(rainfall)
        temp_score = self._temperature_resilience(temperature)
        return (rain_score + temp_score) / 2
    
    def _rainfall_resilience(self, rainfall: pd.Series) -> float:
        """Calculate rainfall-based resilience score"""
        mean_rain = rainfall.mean()
        
        # Calculate various indicators
        variability = rainfall.std() / mean_rain
        drought_freq = (rainfall < (self.thresholds['drought_threshold'] * mean_rain)).mean()
        excess_freq = (rainfall > (self.thresholds['excess_threshold'] * mean_rain)).mean()
        
        # Convert to 0-100 score
        score = 100
        score -= (variability * 50)  # Higher variability reduces score
        score -= (drought_freq * 100)  # Droughts heavily impact score
        score -= (excess_freq * 75)  # Excess rain impacts score less than drought
        
        return max(0, min(100, score))
    
    def _temperature_resilience(self, temperature: pd.Series) -> float:
        """Calculate temperature-based resilience score"""
        # Calculate stress days
        high_stress = (temperature > self.thresholds['temp_stress_high']).mean()
        low_stress = (temperature < self.thresholds['temp_stress_low']).mean()
        
        # Convert to 0-100 score
        score = 100
        score -= (high_stress * 100)  # High temperature stress
        score -= (low_stress * 75)   # Low temperature stress
        
        return max(0, min(100, score))
    
    def get_adaptation_strategies(self, resilience_score: float) -> list:
        """Generate adaptation strategies based on resilience score"""
        strategies = []
        
        if resilience_score < 30:
            strategies.extend([
                "Implement comprehensive drought management plan",
                "Invest in climate-resistant crop varieties",
                "Develop water storage infrastructure"
            ])
        elif resilience_score < 60:
            strategies.extend([
                "Improve irrigation efficiency",
                "Implement soil moisture conservation",
                "Diversify crop portfolio"
            ])
        else:
            strategies.extend([
                "Maintain current resilience measures",
                "Monitor climate patterns",
                "Plan for future climate scenarios"
            ])
        
        return strategies
