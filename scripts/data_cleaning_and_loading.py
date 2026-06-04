import os
import glob
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def clean_and_load_pipeline():
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    db_path = "data/db/bluestock_mf.db"
    engine = create_engine(f"sqlite:///{db_path}")
    
    raw_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    datasets = {os.path.basename(f).replace(".csv", ""): pd.read_csv(f) for f in raw_files if "_live_raw" not in f}
    
    for key in datasets.keys():
        datasets[key].columns = datasets[key].columns.str.lower().str.strip().str.replace(" ", "_")
        rename_dict = {}
        for col in datasets[key].columns:
            if col in ["amfi_code", "scheme_id", "fund_code"]:
                rename_dict[col] = "scheme_code"
            elif col in ["transaction_amount", "amount_inr", "investment_amount"]:
                rename_dict[col] = "amount"
            elif col in ["tx_date", "date_of_transaction"]:
                rename_dict[col] = "transaction_date"
            elif col in ["tx_type", "type_of_transaction"]:
                rename_dict[col] = "transaction_type"
        if rename_dict:
            datasets[key] = datasets[key].rename(columns=rename_dict)
            
    nav = datasets["02_nav_history"]
    nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
    nav = nav.dropna(subset=["date"])
    nav = nav.drop_duplicates(subset=["scheme_code", "date"])
    nav = nav[nav["nav"] > 0]
    
    nav_cleaned_list = []
    for code, group in nav.groupby("scheme_code"):
        group = group.set_index("date").sort_index()
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq="D")
        group = group.reindex(full_range)
        group["scheme_code"] = code
        group["nav"] = group["nav"].ffill()
        group = group.reset_index().rename(columns={"index": "date"})
        nav_cleaned_list.append(group)
        
    nav_clean = pd.concat(nav_cleaned_list, ignore_index=True)
    nav_clean.to_csv(os.path.join(processed_dir, "02_nav_history_clean.csv"), index=False)
    
    tx = datasets["08_investor_transactions"]
    tx_date_col = "transaction_date" if "transaction_date" in tx.columns else "date"
    tx[tx_date_col] = pd.to_datetime(tx[tx_date_col], errors="coerce")
    tx = tx.dropna(subset=[tx_date_col])
    
    if "transaction_type" in tx.columns:
        tx["transaction_type"] = tx["transaction_type"].str.strip().str.title()
        type_map = {"Sip": "SIP", "Lump Sum": "Lumpsum", "Lumpsum": "Lumpsum", "Redemption": "Redemption"}
        tx["transaction_type"] = tx["transaction_type"].map(type_map).fillna("Lumpsum")
        
    if "amount" in tx.columns:
        tx = tx[tx["amount"] > 0]
        
    if "kyc_status" in tx.columns:
        tx["kyc_status"] = tx["kyc_status"].str.strip().str.upper()
        tx["kyc_status"] = tx["kyc_status"].apply(lambda x: x if x in ["Y", "N", "PENDING"] else "N")
        
    tx.to_csv(os.path.join(processed_dir, "08_investor_transactions_clean.csv"), index=False)
    
    perf = datasets["07_scheme_performance"]
    for col in ["1_year_return", "3_year_return", "5_year_return"]:
        if col in perf.columns:
            perf[col] = pd.to_numeric(perf[col], errors="coerce").fillna(0.0)
    if "expense_ratio" in perf.columns:
        perf["expense_ratio"] = pd.to_numeric(perf["expense_ratio"], errors="coerce")
        perf = perf[(perf["expense_ratio"] >= 0.1) & (perf["expense_ratio"] <= 2.5)]
    perf.to_csv(os.path.join(processed_dir, "07_scheme_performance_clean.csv"), index=False)
    
    all_dates = pd.concat([nav_clean["date"], tx[tx_date_col]]).dropna().unique()
    date_df = pd.DataFrame({"date_key": all_dates})
    date_df["date_key"] = pd.to_datetime(date_df["date_key"])
    date_df = date_df.sort_values("date_key").reset_index(drop=True)
    date_df["day"] = date_df["date_key"].dt.day
    date_df["month"] = date_df["date_key"].dt.month
    date_df["year"] = date_df["date_key"].dt.year
    date_df["quarter"] = date_df["date_key"].dt.quarter
    date_df["weekday"] = date_df["date_key"].dt.day_name()
    date_df.to_csv(os.path.join(processed_dir, "dim_date.csv"), index=False)
    
    for name, df in datasets.items():
        if name not in ["02_nav_history", "08_investor_transactions", "07_scheme_performance"]:
            df.to_csv(os.path.join(processed_dir, f"{name}_clean.csv"), index=False)
            
    master_clean = datasets["01_fund_master"]
    aum_clean = datasets["03_aum_by_fund_house"]
    
    print("Loading datasets into SQLite relational schema...")
    master_clean.to_sql("dim_fund", engine, if_exists="replace", index=False)
    date_df.to_sql("dim_date", engine, if_exists="replace", index=False)
    nav_clean.to_sql("fact_nav", engine, if_exists="replace", index=False)
    tx.to_sql("fact_transactions", engine, if_exists="replace", index=False)
    perf.to_sql("fact_performance", engine, if_exists="replace", index=False)
    aum_clean.to_sql("fact_aum", engine, if_exists="replace", index=False)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("\n--- Row Count Verification ---")
    for table in ["dim_fund", "dim_date", "fact_nav", "fact_transactions", "fact_performance", "fact_aum"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Table {table}: {count} rows safely loaded.")
    conn.close()

if __name__ == "__main__":
    clean_and_load_pipeline()