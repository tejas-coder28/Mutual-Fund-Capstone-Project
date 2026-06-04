import os
import glob
import pandas as pd

def check_data_quality():
    raw_dir = "data/raw"
    
    all_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    datasets = [f for f in all_files if "_live_raw" not in f]
    
    if not datasets:
        print("No CSV files found in data/raw/. Make sure files are copied over.")
        return
    
    loaded_data = {}
    
    print("--- Dataset Structural Profiles ---")
    for file_path in datasets:
        file_name = os.path.basename(file_path).replace(".csv", "")
        df = pd.read_csv(file_path)
        loaded_data[file_name] = df
        
        print(f"\nDataset: {file_name}")
        print(f"Shape: {df.shape}")
        print("Data Types:")
        print(df.dtypes)
        print("Preview:")
        print(df.head(2))
        
        null_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()
        if null_count > 0 or duplicate_count > 0:
            print(f"--> Notice: Found {null_count} missing values and {duplicate_count} duplicates.")
        else:
            print("--> Structure looks clean.")
            
    master_key = [k for k in loaded_data.keys() if "fund_master" in k]
    nav_key = [k for k in loaded_data.keys() if "nav_history" in k]
    
    if master_key and nav_key:
        validate_amfi_codes(loaded_data[master_key[0]], loaded_data[nav_key[0]])

def validate_amfi_codes(master_df, nav_df):
    print("\n--- Running Referential Integrity Check ---")
    
    master_df.columns = master_df.columns.str.lower().str.strip().str.replace(" ", "_")
    nav_df.columns = nav_df.columns.str.lower().str.strip().str.replace(" ", "_")
    
    if "category" in master_df.columns:
        print(f"Unique Categories: {master_df['category'].nunique()}")
        print(master_df['category'].dropna().unique())
        
    if "scheme_code" in master_df.columns and "scheme_code" in nav_df.columns:
        master_codes = set(master_df["scheme_code"].dropna().unique())
        nav_codes = set(nav_df["scheme_code"].dropna().unique())
        
        unmatched = master_codes - nav_codes
        match_rate = (len(master_codes - unmatched) / len(master_codes)) * 100
        
        print(f"\nTotal schemes in master: {len(master_codes)}")
        print(f"Total unique schemes tracked in history: {len(nav_codes)}")
        print(f"Code mapping success rate: {match_rate:.2f}%")
        
        if unmatched:
            print(f"Warning: {len(unmatched)} scheme codes from the master list are missing from history.")
            processed_dir = "data/processed"
            os.makedirs(processed_dir, exist_ok=True)
            
            orphan_df = pd.DataFrame(list(unmatched), columns=["missing_scheme_code"])
            orphan_df.to_csv(os.path.join(processed_dir, "orphan_codes.csv"), index=False)
            print("Orphan scheme codes exported to data/processed/orphan_codes.csv")

if __name__ == "__main__":
    check_data_quality()