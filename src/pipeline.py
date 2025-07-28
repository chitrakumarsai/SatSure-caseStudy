"""
Core pipeline implementation for climate data analysis.
"""
from pathlib import Path
import json
import pandas as pd
from .data_loader import DataLoader
from .transformer import DataTransformer
from .analyzer import ClimateAnalyzer
from .validator import DataValidator
from .resilience import ResilienceAnalyzer

class ClimateDataPipeline:
    def __init__(self, data_path: Path = None, output_path: Path = None):
        self.data_path = data_path or Path("data/raw")
        self.output_path = output_path or Path("data/processed")
        self.loader = DataLoader(self.data_path)
        self.transformer = DataTransformer()
        self.analyzer = ClimateAnalyzer()
        self.validator = DataValidator()
        self.resilience = ResilienceAnalyzer()
        
    def run(self, save_results: bool = True):
        """Execute the complete pipeline"""
        results = {}
        
        # Load data
        raw_data = self.loader.load_all()
        
        # Validate
        self.validator.validate_data(raw_data)
        
        # Transform
        processed_data = self.transformer.transform(raw_data)
        if save_results:
            self._save_processed_data(processed_data)
        
        # Analyze
        analysis_results = self.analyzer.analyze(processed_data)
        
        # Calculate resilience scores
        resilience_scores = self._calculate_resilience(processed_data)
        
        # Combine all results
        results = {
            'analysis': analysis_results,
            'resilience': resilience_scores,
            'recommendations': self._generate_final_recommendations(analysis_results, resilience_scores)
        }
        
        if save_results:
            self._save_results(results)
        
        return results
    
    def _calculate_resilience(self, processed_data: dict) -> dict:
        """Calculate resilience scores for each region"""
        scores = {}
        for region in ['mh', 'mp']:
            rainfall = processed_data['monthly'][f'{region}_precip_monthly']
            temperature = processed_data['monthly'][f'{region}_temp_monthly']
            
            score = self.resilience.calculate_resilience_score(rainfall, temperature)
            strategies = self.resilience.get_adaptation_strategies(score)
            
            scores[region] = {
                'score': score,
                'adaptation_strategies': strategies
            }
        return scores
    
    def _generate_final_recommendations(self, analysis: dict, resilience: dict) -> dict:
        """Generate comprehensive recommendations"""
        recommendations = {}
        
        for region in ['mh', 'mp']:
            region_recs = {
                'climate_adaptation': resilience[region]['adaptation_strategies'],
                'economic_measures': self._get_economic_recommendations(analysis['economic_impact'], region),
                'infrastructure': self._get_infrastructure_recommendations(analysis['infrastructure'], region),
                'crop_management': self._get_crop_recommendations(analysis['crop_analysis'], region)
            }
            recommendations[region] = region_recs
            
        return recommendations
    
    def _save_processed_data(self, data: dict):
        """Save processed data to files"""
        output_dir = self.output_path
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save monthly data
        for key, series in data['monthly'].items():
            series.to_csv(output_dir / f"{key}_monthly.csv")
        
        # Save seasonal data
        for key, series in data['seasonal'].items():
            series.to_csv(output_dir / f"{key}_seasonal.csv")
    
    def _save_results(self, results: dict):
        """Save analysis results"""
        output_dir = self.output_path
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save results as JSON
        with open(output_dir / "analysis_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    def _get_economic_recommendations(self, economic_data: dict, region: str) -> list:
        """Generate economic recommendations"""
        recs = []
        impact_data = [d for d in economic_data if d['Region'].lower() == region]
        
        if any(d['Estimated_Loss'] < -1000000 for d in impact_data):
            recs.extend([
                "Implement crop insurance schemes",
                "Develop alternative income sources",
                "Establish market linkages for crop diversification"
            ])
        return recs
    
    def _get_infrastructure_recommendations(self, infra_data: dict, region: str) -> list:
        """Generate infrastructure recommendations"""
        recs = []
        risk_score = infra_data.get(f'{region}_infrastructure_risk', 0)
        
        if risk_score > 70:
            recs.extend([
                "Upgrade irrigation infrastructure",
                "Improve water storage facilities",
                "Enhance weather monitoring systems"
            ])
        return recs
    
    def _get_crop_recommendations(self, crop_data: dict, region: str) -> list:
        """Generate crop-specific recommendations"""
        recs = []
        stress_level = crop_data.get(f'{region}_kharif_stress', 0)
        
        if stress_level > 30:
            recs.extend([
                "Introduce drought-resistant varieties",
                "Adjust planting calendar",
                "Implement soil moisture conservation"
            ])
        return recs
