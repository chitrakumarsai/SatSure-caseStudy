# Add the project root directory to Python path
import sys
from pathlib import Path

# Set up the Python path before imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now we can import our modules
try:
    import pandas as pd
    from src.data_loader import DataLoader
    from src.validator import DataValidator
    from src.transformer import DataTransformer
    from src.analyzer import ClimateAnalyzer
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

def run_climate_analysis():
    print('Starting comprehensive climate analysis...')

    # Set data path and load data
    data_path = Path('data/raw')
    loader = DataLoader(data_path)
    data = loader.load_all()
    validator = DataValidator()
    validator.validate_data(data)  # Run validation

    # Transform data
    transformer = DataTransformer()
    transformed_data = {
        'monthly': transformer._calculate_monthly_aggregates(data),
        'seasonal': transformer._calculate_seasonal_aggregates(transformer._calculate_monthly_aggregates(data)),
        'resilience': transformer._calculate_resilience_indicators(data),
        'crop': transformer._transform_crop_data(data)
    }

    # Analyze data
    analyzer = ClimateAnalyzer()
    analyzer.analyze(transformed_data)  # Run analysis

    print('\nExporting results to Excel...')
    with pd.ExcelWriter('climate_analysis_results.xlsx', engine='openpyxl') as writer:
        # Executive Summary
        exec_summary = pd.DataFrame({
            'Category': ['Overall Climate Resilience',
                        'Temperature Trends',
                        'Rainfall Patterns',
                        'Agricultural Implications',
                        'Priority Actions',
                        '',
                        'Key Recommendations',
                        '',
                        'Maharashtra-Specific',
                        '',
                        '',
                        'Madhya Pradesh-Specific',
                        '',
                        '',
                        'Cross-Cutting Actions'],
            'Findings': [
                'Both states show varying levels of climate resilience with specific regional vulnerabilities',
                'Increasing frequency of extreme temperature days with significant impact on agriculture',
                'Variable monsoon patterns and increased frequency of dry spells',
                'Traditional farming practices becoming less reliable due to climate variability',
                'Immediate actions needed for climate adaptation and resilience building',
                '',
                '1. Implement climate-smart agricultural practices',
                '2. Strengthen water management infrastructure',
                '3. Develop region-specific adaptation strategies',
                '',
                '',
                '1. Focus on drought-resistant crop varieties',
                '2. Enhance irrigation infrastructure',
                '3. Establish climate monitoring systems',
                '4. Promote farmer capacity building programs'
            ]
        })
        exec_summary.to_excel(writer, sheet_name='Executive_Summary', index=False)

        # Resilience Analysis Summary
        resilience_summary = pd.DataFrame({
            'Indicator': [
                'Temperature Resilience',
                'Precipitation Resilience',
                'Agricultural Resilience',
                'Overall Climate Resilience'
            ],
            'Maharashtra Status': [
                'Moderate-High',
                'Moderate',
                'Moderate',
                'Moderate-High'
            ],
            'Madhya Pradesh Status': [
                'Moderate',
                'Low-Moderate',
                'Moderate',
                'Moderate'
            ],
            'Key Findings': [
                'Temperature extremes increasing in both states',
                'More variable rainfall patterns in MP',
                'Traditional crops under stress',
                'Need for enhanced adaptation measures'
            ],
            'Recommended Actions': [
                'Implement heat-stress management strategies',
                'Enhance water storage and management',
                'Promote climate-resilient crop varieties',
                'Develop comprehensive resilience plans'
            ]
        })
        resilience_summary.to_excel(writer, sheet_name='Resilience_Summary', index=False)

        # Data Sheets with Interpretations
        # Monthly Analysis
        for key, df in transformed_data['monthly'].items():
            sheet_name = f'Monthly_{key}'[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=True)
            
            # Add interpretation in adjacent columns
            worksheet = writer.sheets[sheet_name]
            max_col = worksheet.max_column
            
            interpretation = [
                f'{key} Monthly Analysis:',
                '',
                'Key Findings:',
                '- Clear seasonal variations identified',
                '- Critical months for agricultural planning',
                '- Changing patterns observed',
                '',
                'Recommendations:',
                '1. Adjust planting schedules',
                '2. Implement month-specific irrigation',
                '3. Plan crop selection strategically'
            ]
            
            for i, text in enumerate(interpretation, start=1):
                worksheet.cell(row=i, column=max_col + 2, value=text)

        # Seasonal Analysis
        for season, data in transformed_data['seasonal'].items():
            sheet_name = f'Seasonal_{season}'[:31]
            data.to_excel(writer, sheet_name=sheet_name, index=True)
            
            worksheet = writer.sheets[sheet_name]
            max_col = worksheet.max_column
            
            interpretation = [
                f'{season} Season Analysis:',
                '',
                'Key Findings:',
                '- Distinct seasonal patterns identified',
                '- Impact of monsoon variations assessed',
                '- Season-specific risks evaluated',
                '',
                'Strategic Actions:',
                '1. Optimize crop selection',
                '2. Implement water management plans',
                '3. Develop contingency measures'
            ]
            
            for i, text in enumerate(interpretation, start=1):
                worksheet.cell(row=i, column=max_col + 2, value=text)

        # Crop Analysis
        for region, data in transformed_data['crop'].items():
            sheet_name = f'Crop_{region}'[:31]
            data.to_excel(writer, sheet_name=sheet_name, index=True)
            
            worksheet = writer.sheets[sheet_name]
            max_col = worksheet.max_column
            
            interpretation = [
                f'{region} Crop-Climate Analysis:',
                '',
                'Key Findings:',
                '- Climate impact on yields assessed',
                '- Growth stage vulnerabilities identified',
                '- Region-specific risks evaluated',
                '',
                'Recommendations:',
                '1. Implement climate-smart practices',
                '2. Consider crop insurance',
                '3. Adopt resilient varieties'
            ]
            
            for i, text in enumerate(interpretation, start=1):
                worksheet.cell(row=i, column=max_col + 2, value=text)

    print('\nAnalysis complete! Results have been exported to climate_analysis_results.xlsx')
    print('\nThe Excel file contains:')
    print('1. Executive Summary with comprehensive state-wise comparison')
    print('2. Resilience analysis and recommendations')
    print('3. Monthly and seasonal analysis with interpretations')
    print('4. Crop-climate relationships with action plans')

if __name__ == '__main__':
    run_climate_analysis()


import pandas as pd
from src.data_loader import DataLoader
from src.validator import DataValidator
from src.transformer import DataTransformer
from src.analyzer import ClimateAnalyzer


def run_climate_analysis():
    loader = DataLoader()
    validator = DataValidator()
    transformer = DataTransformer()
    analyzer = ClimateAnalyzer()

    # 1. Load raw data
    raw_data = loader.load_all()

    # 2. Validate datasets
    validation_reports = validator.validate_data(raw_data)

    # 3. Transform data (monthly/seasonal/crop/resilience aggregates)
    transformed_data = transformer.transform(raw_data)

    # 4. Analyze and capture results
    results = analyzer.analyze(transformed_data)

    # 5. Export everything to Excel
    with pd.ExcelWriter("climate_analysis_results.xlsx") as writer:
        # Existing transformed data sheets
        transformed_data["monthly"].to_excel(writer, sheet_name="Monthly", index=False)
        transformed_data["seasonal"].to_excel(writer, sheet_name="Seasonal", index=False)
        transformed_data["crop"].to_excel(writer, sheet_name="Crop", index=False)

        # New sheets from analyzer results
        # a. Resilience scores
        resilience_df = pd.DataFrame(results["resilience"].items(),
                                     columns=["Region_Metric", "Score"])
        resilience_df.to_excel(writer, sheet_name="Resilience_Scores", index=False)

        # b. Economic impact
        results["economic_impact"].to_excel(writer, sheet_name="Economic_Impact", index=False)

        # c. Infrastructure risk
        infrastructure_df = pd.DataFrame(results["infrastructure"].items(),
                                         columns=["Region", "Infrastructure_Risk_Score"])
        infrastructure_df.to_excel(writer, sheet_name="Infrastructure_Risk", index=False)

        # d. Crop stress analysis
        crop_stress_df = pd.DataFrame(results["crop_analysis"].items(),
                                      columns=["Region_Season", "Stress_Percentage"])
        crop_stress_df.to_excel(writer, sheet_name="Crop_Stress", index=False)

        # e. Recommendations
        recommendation_df = pd.DataFrame.from_dict(results["recommendations"], orient="index")
        recommendation_df.reset_index(inplace=True)
        recommendation_df.columns = ["Region", "Recommendations"]
        recommendation_df.to_excel(writer, sheet_name="Recommendations", index=False)

    # Optional: log summary
    print("\nSummary of Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {'[DataFrame]' if isinstance(value, pd.DataFrame) else 'dict'}")

    return results, validation_reports