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