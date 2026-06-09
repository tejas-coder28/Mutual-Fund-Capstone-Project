# Bluestock Mutual Fund & Portfolio Analytics Platform

An end-to-end data analytics platform comprising an ETL pipeline, exploratory data analysis (EDA), and an interactive 4-page Power BI business intelligence dashboard analyzing asset management data, fund performance, investor demographics, and underlying equity portfolio holdings.

## 📂 Project Architecture & Repository Structure

The project workspace is structured to separate the data pipeline, analytical notebooks, database scripts, and reporting layers cleanly:

*   **`dashboard/`**: Holds core dashboard configurations and presentation assets.
*   **`data/`**: Local repository for raw and cleaned structured datasets.
*   **`notebooks/`**: Interactive Jupyter notebooks containing exploratory analyses and algorithmic evaluations:
    *   `03_eda_analysis.ipynb`: Data distribution profiling, handling missing values, and early structural data verification.
    *   `04_performance_analytics.ipynb`: Computational calculation of alpha, beta, and benchmark comparison statistics.
*   **`reports/`**: Documentation and static export summaries generated during data modeling.
*   **`scripts/`**: Automation modules handling the extraction, loading, and structural staging of source files.
*   **`sql/`**: Relational query definitions tracking schema migration scripts and key table joins.
*   **`bluestock_mf_dashboard.pbix`**: The fully compiled, interactive Power BI production dashboard application.
*   **`data_dictionary.md`**: Definitive data schema documentation mapping variable types and relational keys.
*   **`requirements.txt`**: Standard python package dependencies for running the notebooks environment cleanly.

---

## 📊 Dashboard Visual Framework

The production dashboard compiles complex data models into four user-focused analytical pages:

### 1. Industry Overview
* Tracking macro scale KPIs including Total Assets Under Management (AUM), systemic capital inflows, and high-level structural metrics.
* Comprehensive asset allocation profiling across Equity, Debt, and Hybrid financial funds.

### 2. Fund Performance Analytics
* **Risk vs. Return Matrix**: A dynamic scatter chart plotting calculated risk metrics against performance indicators to easily identify top-tier fund groupings.
* **NAV Historical Tracking**: Multi-axis time-series visualization comparing historical Net Asset Value trends alongside benchmark indices (e.g., NIFTY50) to verify fund alpha.

### 3. Investor Behavior & Demographics
* **Demographic Distributions**: Tracking unique, individual investor volumes using non-additive distinct counts segmented by age bracket generations.
* **Geographic Volumetrics**: Treemap layouts mapping regional financial flows between Tier-30 and Beyond-30 market sectors.
* **Payment Modalities**: Tracking market share splits between alternative transactions methods (UPI, Net Banking, Mandates, Cheques).

### 4. Underlying Portfolio Deep-Dive
* Interactive equity holding exploration utilizing an ergonomic tile-based slicer layout.
* Allows instantaneous cross-filtering to expose specific underlying company stocks (e.g., Reliance, Infosys, HDFC Bank) across all active mutual funds, displaying actual proportional asset weights.

---

## 🛠️ Technical Stack & Implementation Details
*   **Database Management & EDA**: Python (`pandas`, `numpy`), SQLite for handling operational database configurations.
*   **Analytical Frameworks**: `scipy.stats` for modeling statistical distribution arrays; interactive visualization mapping using `plotly`.
*   **Business Intelligence Platform**: Power BI Desktop.
*   **Data Modeling**: Advanced Star Schema architecture connecting dimensional definitions with historical transaction logs.
*   **Functional Expressions**: Advanced DAX queries for non-additive metrics (`Distinct Count` configurations) and dynamic weight sorting.