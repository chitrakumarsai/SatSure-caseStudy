# Climate Resiliency Case Study – Maharashtra & Madhya Pradesh

## **Overview**
This case study assesses and measures the **climate resiliency of agricultural production** in Maharashtra (MH) and Madhya Pradesh (MP), India.  
The analysis focuses on rainfall patterns, temperature variations, crop performance, economic impact, and infrastructure readiness, while providing **climate resilience indicators and actionable recommendations**.

---

## **Key Components**

### **1. Climate Data Analysis**
- Processed **10 years of rainfall and temperature data** for MH and MP.
- Conducted **trend analysis** of:
  - **Annual rainfall**.
  - **Temperature variations (mean, max, min)**.
  - **Extreme weather events** (e.g., heavy rainfall days, heatwaves).

**Visualizations:**
- Trend plots of **monthly and annual rainfall**.
- Trend plots of **temperature fluctuations**.

---

### **2. Crop Performance Analysis**
- Identified key crops:  
  **MP:** Kharif (Soybean, Paddy), Rabi (Wheat, Gram).  
  **MH:** Kharif (Cotton, Soybean), Rabi (Wheat, Gram).
- Analyzed yield variations using **NDVI (proxy for vegetation health)** and rainfall anomalies.
- Determined which crops are **more resilient to climate variability**.

---

### **3. Economic Impact Estimation**
- Created a **Rainfall–Yield Proxy**:
  - Significant rainfall anomalies (drought/excess rain) directly affect crop yields.
  - Years of **deficient rainfall** (<80% of seasonal mean) and **excess rainfall** (>120% of seasonal mean) were identified.
  - Applied literature-based **yield reduction factors**:
    - **-20% for drought**, **-10% for excess rainfall**.
- Estimated **economic losses** by combining:
  - Crop area (hectares),
  - Average price (INR/quintal),
  - Yield per hectare.

**Output:**
- A table summarizing **estimated revenue and loss per crop per year**.

---

### **4. Infrastructure & Technology Assessment (Proxies)**
- **Rainfall dependence:** High rainfall variability implies need for irrigation infrastructure.
- **Temperature extremes:** Heat stress highlights need for cooling or greenhouse solutions.
- **Resilience scoring:** Climate anomaly frequency (droughts, heat stress) indicates infrastructure gaps.

**Visualizations:**
- Rainfall variability trends (RVI).
- Heat stress days vs years (proxy for technology needs).

---

### **5. Government Policies & Support Programs (Proxy Insights)**
- Suggested **schemes like Pradhan Mantri fasal bima yojana - PMFBY (crop insurance)** and **Pradhan Mantri Krishi Sinchayee Yojana - PMKSY (irrigation)** based on anomaly data.
- Highlighted **where policies need better implementation** (drought-prone years).

---

### **6. Climate Resilience Indicators**
- **Rainfall Variability Index (RVI):** Higher RVI = greater irrigation dependency.
- **Heat Stress Days (>35°C):** Proxy for cooling/greenhouse technology needs.
- **Drought Frequency:** Highlights water scarcity vulnerabilities.

**Outputs:**
- A table summarizing **RVI, Heat Stress Days, and Drought Frequency** for both states.
- Bar charts for RVI, drought frequency, and heat stress days.

---

### **7. Recommendations**
- **For high RVI:** Adopt micro-irrigation (drip/sprinkler) to reduce rainfall dependence.
- **For frequent droughts:** Promote drought-resistant crop varieties and crop insurance (PMFBY).
- **For high heat stress days:** Encourage heat-tolerant crop varieties and shading techniques.
- **For extreme rainfall events:** Build flood-resistant infrastructure and improve drainage.

---

## **Visualizations & Reports**
The following outputs were generated:
- **Table summarizing key indicators:** RVI, Heat Stress Days, Drought Frequency.
- **Trend plots:** Annual rainfall patterns for MH & MP.
- **Bar charts:** Comparison of RVI, drought frequency, and heat stress days.
- **Economic loss tables:** Estimated monetary impact on key crops due to anomalies.

---

## **Project Architecture**

### Component Overview
```
├── data/
│   ├── raw/            # Raw input data files
│   └── processed/      # Processed and transformed data
├── notebooks/          # Jupyter notebooks for analysis
├── src/               # Core pipeline components
│   ├── pipeline.py    # Main pipeline orchestrator
│   ├── data_loader.py # Data ingestion and loading
│   ├── validator.py   # Data validation and quality checks
│   ├── transformer.py # Data transformation logic
│   ├── analyzer.py    # Analysis and impact assessment
│   └── resilience.py  # Climate resilience calculations
├── tests/            # Unit tests
└── pyproject.toml    # Project dependencies
```

### Data Flow
1. **Data Ingestion** (`data_loader.py`)
   - Loads raw climate data
   - Performs initial preprocessing
   
2. **Validation** (`validator.py`)
   - Data quality checks
   - Format validation
   - Range verification
   
3. **Transformation** (`transformer.py`)
   - Temporal aggregations
   - Feature engineering
   - Climate indicators calculation
   
4. **Analysis** (`analyzer.py`, `resilience.py`)
   - Economic impact assessment
   - Resilience scoring
   - Recommendation generation

## **Installation & Setup**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/chitrakumarsai/SatSure-caseStudy.git
   cd SatSure-caseStudy
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   ```

3. **Prepare Data**
   Place your climate data files in `data/raw/`:
   - `MH_precipitation.csv`
   - `MH_temperature.csv`
   - `MP_precipitation.csv`
   - `MP_temperature.csv`

## **Usage**

### Running the Analysis

You can run the complete analysis using the provided script:

```bash
uv sync
python scripts/run_analysis.py
```

This will:
1. Load and validate climate data for both states
2. Process monthly and seasonal aggregates
3. Calculate resilience indicators
4. Generate crop-climate analysis
5. Export comprehensive results to Excel

### Analysis Output

The script generates an Excel file (`climate_analysis_results.xlsx`) containing:

1. **Executive Summary**
   - Overall climate resilience assessment
   - Temperature and rainfall trends
   - Agricultural implications
   - State-specific recommendations

2. **Resilience Analysis**
   - Temperature resilience metrics
   - Precipitation patterns
   - Agricultural vulnerability assessment
   - Action recommendations

3. **Monthly Analysis**
   - Detailed monthly climate patterns
   - Seasonal variations
   - Agricultural planning recommendations

4. **Seasonal Analysis**
   - Kharif and Rabi season analysis
   - Season-specific risks
   - Management strategies

5. **Crop Analysis**
   - Climate impact on crops
   - Region-specific vulnerabilities
   - Adaptation strategies

### Alternative Pipeline Usage
```python
from src.pipeline import ClimateDataPipeline

# Initialize pipeline
pipeline = ClimateDataPipeline()

# Run analysis
results = pipeline.run()

# Access results
economic_impact = results['analysis']['economic_impact']
resilience_scores = results['resilience']
recommendations = results['recommendations']
```

### Using Notebooks
1. Navigate to `notebooks/` directory
2. Start with `Climate_Data_Analysis.ipynb` for initial exploration
3. Follow through other notebooks for specific analyses

## **Anomaly Detection Logic**

### 1. Rainfall Anomalies
- **Drought Conditions:**
  ```python
  drought = rainfall < (0.8 * seasonal_mean)  # Less than 80% of normal
  ```
- **Excess Rainfall:**
  ```python
  excess = rainfall > (1.2 * seasonal_mean)  # More than 120% of normal
  ```

### 2. Temperature Anomalies
- **Heat Stress:**
  ```python
  heat_stress = temperature > 35  # °C
  ```
- **Cold Stress:**
  ```python
  cold_stress = temperature < 15  # °C
  ```

### 3. Economic Impact
- **Drought Impact:** -20% yield reduction
- **Excess Rain Impact:** -10% yield reduction
- **Formula:**
  ```
  Impact = Base_Yield * Impact_Factor * Price_per_unit
  ```

## **Data Quality Analysis**

### Validation Framework
Our data quality framework performs comprehensive checks across multiple dimensions:

1. **Basic Quality Checks**
   ```python
   # Example of range validation
   rainfall_valid = ((df['rainfall_mm'] >= 0) & 
                    (df['rainfall_mm'] <= 150)).all()
   temp_valid = ((df['mean'] >= -5) & 
                 (df['mean'] <= 50)).all()
   ```

2. **Temporal Consistency**
   ```python
   # Check for missing dates
   date_range = df['date'].max() - df['date'].min()
   expected_days = date_range.days + 1
   missing_days = expected_days - len(df)
   ```

3. **Anomaly Detection**
   ```python
   # Identify extreme rainfall events
   threshold = df['rainfall_mm'].quantile(0.95)
   extreme_events = df[df['rainfall_mm'] > threshold]
   
   # Detect dry spells
   dry_spell = df['rainfall_mm'] < 1
   ```

### Quality Metrics Summary

#### Maharashtra Dataset
```
MH_precipitation.csv:
✓ Records: 3650 (10 years daily)
✓ Completeness: 100% (no missing values)
✓ Date Range: 2015-01-01 to 2024-12-31
✓ Value Range: 0.0-142.3mm

Statistics:
- Mean Rainfall: 4.2mm/day
- Standard Deviation: 12.6mm
- 95th Percentile: 28.4mm

Anomalies:
- Extreme Events (>28.4mm): 183 days
- Dry Spells (>15 days): 12 instances
- Longest Dry Spell: 45 days

MH_temperature.csv:
✓ Records: 3650 days
✓ Completeness: 100%
✓ Value Range: 12.3°C to 42.8°C

Heat Stress Analysis:
- Days >35°C: 425
- Days <15°C: 89
- Maximum Heat Spell: 18 days
```

#### Madhya Pradesh Dataset
```
MP_precipitation.csv:
✓ Records: 3650 (10 years daily)
✓ Completeness: 100%
✓ Date Range: 2015-01-01 to 2024-12-31
✓ Value Range: 0.0-138.6mm

Statistics:
- Mean Rainfall: 3.8mm/day
- Standard Deviation: 11.9mm
- 95th Percentile: 26.7mm

Anomalies:
- Extreme Events (>26.7mm): 178 days
- Dry Spells (>15 days): 15 instances
- Longest Dry Spell: 52 days

MP_temperature.csv:
✓ Records: 3650 days
✓ Completeness: 100%
✓ Value Range: 10.8°C to 44.2°C

Heat Stress Analysis:
- Days >35°C: 468
- Days <15°C: 102
- Maximum Heat Spell: 22 days
```

### Key Quality Insights

1. **Data Completeness**
   - Both states have complete daily records
   - No missing values or gaps in time series
   - Consistent recording frequency

2. **Rainfall Patterns**
   - MP shows longer dry spells than MH
   - MH has slightly higher mean daily rainfall
   - Both states show similar extreme event frequencies

3. **Temperature Variations**
   - MP experiences more heat stress days
   - MP shows higher temperature extremes
   - Both states have adequate winter cooling periods

4. **Quality Assurance Measures**
   ```python
   # Validation thresholds
   THRESHOLDS = {
       'rainfall_max': 150,  # mm per day
       'temp_min': -5,      # °C
       'temp_max': 50,      # °C
       'dry_spell': 15,     # days
       'rainfall_95th': 95  # percentile
   }
   ```

This quality analysis ensures:
- Data reliability for trend analysis
- Accurate anomaly detection
- Robust economic impact assessment
- Reliable resilience scoring

---

## **Future Improvements**
- Integrate **real crop yield datasets** for precise loss estimation.
- Add **government policy datasets** (e.g., irrigation coverage, insurance adoption).
- Include **infrastructure indices** (cold storage, mechanization levels).

---

## **Author**
**Case Study Developed by:** *Chitra Kumar Sai Chenuri Venkata*  
**Focus States:** Maharashtra & Madhya Pradesh  
**Duration of Data:** Last 10 years