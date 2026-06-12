"""
rebuild_db.py
-------------
Rebuilds the SQLite database from the already-cleaned processed CSVs.
Run this when data/raw/ is empty but data/processed/ already has clean data.
"""

import os
import sqlite3
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

PROJECT_ROOT  = Path(__file__).parent.parent   # scripts/ -> mf_project/
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH       = PROJECT_ROOT / "data" / "db" / "bluestock_mf.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Table name → clean CSV filename mapping
TABLE_MAP = {
    "dim_fund":         "01_fund_master_clean.csv",
    "fact_nav":         "02_nav_history_clean.csv",
    "fact_aum":         "03_aum_by_fund_house_clean.csv",
    "fact_sip":         "04_monthly_sip_inflows_clean.csv",
    "fact_cat_inflows": "05_category_inflows_clean.csv",
    "fact_folio":       "06_industry_folio_count_clean.csv",
    "fact_performance": "07_scheme_performance_clean.csv",
    "fact_transactions":"08_investor_transactions_clean.csv",
    "fact_holdings":    "09_portfolio_holdings_clean.csv",
    "fact_benchmark":   "10_benchmark_indices_clean.csv",
    "dim_date":         "dim_date.csv",
}

def rebuild():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    print(f"Rebuilding DB at: {DB_PATH}\n")

    loaded = []
    for table, csv_name in TABLE_MAP.items():
        csv_path = PROCESSED_DIR / csv_name
        if not csv_path.exists():
            print(f"  [SKIP] {csv_name} not found")
            continue
        df = pd.read_csv(csv_path)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"  [OK]   {table:20s} <- {csv_name}  ({len(df):,} rows)")
        loaded.append(table)

    # Row count verification
    conn = sqlite3.connect(str(DB_PATH))
    cur  = conn.cursor()
    print("\n--- Row Count Verification ---")
    for table in loaded:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table:20s}: {cur.fetchone()[0]:,} rows")
    conn.close()
    print(f"\n[DONE] DB rebuilt successfully: {DB_PATH}")

if __name__ == "__main__":
    rebuild()
