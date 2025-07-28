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

## **How to Use**
1. Load rainfall and temperature datasets:
   - `MH_precipitation.csv`, `MH_temperature.csv`,
   - `MP_precipitation.csv`, `MP_temperature.csv`.
2. Run analysis scripts to:
   - Generate climate trends.
   - Compute resilience indicators.
   - Estimate economic losses.
3. Review generated plots and tables for actionable insights.

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