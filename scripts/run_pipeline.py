# #!/usr/bin/env python3
# """
# Test script to run the climate analysis pipeline
# """
# import os
# import sys
# from pathlib import Path

# # Add project root to Python path
# project_root = Path(__file__).parent.parent
# sys.path.append(str(project_root))

# from src.pipeline import ClimateDataPipeline

# def main():
#     """Run the pipeline and display results"""
#     try:
#         print("Initializing pipeline...")
#         pipeline = ClimateDataPipeline()
        
#         print("\nRunning pipeline...")
#         results = pipeline.run(verbose=True)
        
#         print("\nPipeline Results:")
#         print("-" * 50)
        
#         # Display validation results
#         print("\nValidation Summary:")
#         for dataset, report in results['validation_reports'].items():
#             print(f"\n{dataset}:")
#             print(f"Status: {report['validation_status']}")
#             print(f"Records: {report['total_records']}")
#             print(f"Date Range: {report['date_range']}")
            
#             # Show any anomalies
#             if 'anomalies' in report:
#                 print("\nAnomalies detected:")
#                 for type_, anomaly in report['anomalies'].items():
#                     print(f"{type_}: {anomaly}")
        
#         print("\nPipeline completed successfully!")
        
#     except Exception as e:
#         print(f"\nERROR: Pipeline execution failed!")
#         print(f"Reason: {str(e)}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()
