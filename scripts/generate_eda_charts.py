import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_eda_pipeline():
    db_path = "data/db/bluestock_mf.db"
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}!")
        return
        
    conn = sqlite3.connect(db_path)
    sns.set_theme(style="whitegrid")
    
    df_aum = pd.read_sql_query("SELECT * FROM fact_aum", conn)
    if not df_aum.empty:
        plt.figure(figsize=(12, 6))
        
        x_col = "quarter" if "quarter" in df_aum.columns else (df_aum.columns[0] if len(df_aum.columns) > 0 else None)
        y_col = "aum_crores" if "aum_crores" in df_aum.columns else (df_aum.columns[1] if len(df_aum.columns) > 1 else None)
        hue_col = "fund_house" if "fund_house" in df_aum.columns else None
        
        if x_col and y_col:
            sns.barplot(data=df_aum, x=x_col, y=y_col, hue=hue_col)
            plt.title("AUM Growth Comparison Across Fund Houses", fontsize=12, pad=15)
            plt.xlabel(x_col.replace("_", " ").title())
            plt.ylabel(y_col.replace("_", " ").title())
            plt.xticks(rotation=45)
            if hue_col:
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(f"{reports_dir}/01_aum_growth.png", dpi=150)
        plt.close()

    query_heatmap = """
        SELECT d.month, f.category, SUM(t.amount) as net_inflow
        FROM fact_transactions t
        JOIN dim_fund f ON t.scheme_code = f.scheme_code
        JOIN dim_date d ON t.transaction_date = d.date_key
        GROUP BY d.month, f.category
    """
    df_heat = pd.read_sql_query(query_heatmap, conn)
    if not df_heat.empty:
        pivot_heat = df_heat.pivot(index="category", columns="month", values="net_inflow").fillna(0)
        plt.figure(figsize=(12, 6))
        sns.heatmap(pivot_heat, cmap="YlGnBu", annot=False)
        plt.title("Category Wise Monthly Net Inflow Intensity Heatmap", fontsize=12, pad=15)
        plt.tight_layout()
        plt.savefig(f"{reports_dir}/02_category_heatmap.png", dpi=150)
        plt.close()

    query_geo = "SELECT state, SUM(amount) as total_sip FROM fact_transactions WHERE state IS NOT NULL GROUP BY state"
    df_geo = pd.read_sql_query(query_geo, conn)
    if not df_geo.empty:
        df_geo = df_geo.sort_values(by="total_sip", ascending=False).head(15)
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_geo, x="total_sip", y="state", palette="viridis")
        plt.title("Geographic Breakdown of Total Investment Volume by State", fontsize=12)
        plt.xlabel("Total Investment Amount (₹)")
        plt.tight_layout()
        plt.savefig(f"{reports_dir}/03_geographic_distribution.png", dpi=150)
        plt.close()

    query_corr = "SELECT date, scheme_code, nav FROM fact_nav"
    df_nav_raw = pd.read_sql_query(query_corr, conn)
    if not df_nav_raw.empty:
        pivot_corr = df_nav_raw.pivot(index="date", columns="scheme_code", values="nav").pct_change().dropna()
        top_10_funds = pivot_corr.columns[:10]
        corr_matrix = pivot_corr[top_10_funds].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True)
        plt.title("Pairwise Daily Returns Correlation Matrix (10 Selected Funds)", fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{reports_dir}/04_correlation_matrix.png", dpi=150)
        plt.close()

    conn.close()
    print("All structural report charts exported into your /reports/ folder successfully!")

if __name__ == "__main__":
    run_eda_pipeline()