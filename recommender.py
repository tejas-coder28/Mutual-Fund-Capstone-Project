import os
import sqlite3
import numpy as np
import pandas as pd

db_path = None
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".db") and os.path.getsize(os.path.join(root, file)) > 0:
            db_path = os.path.join(root, file)
            break

if db_path is None:
    for root, dirs, files in os.walk(r"C:\Users\Tejas\Desktop\mf_project"):
        for file in files:
            if file.endswith(".db") and os.path.getsize(os.path.join(root, file)) > 0:
                db_path = os.path.join(root, file)
                break

conn = sqlite3.connect(db_path)

df_funds = pd.read_sql_query("SELECT * FROM dim_fund;", conn)

risk_col = next((c for c in df_funds.columns if "risk" in c.lower()), None)

if not risk_col:
    risk_col = df_funds.columns[-1]

def get_recommendations(target_grade):
    filtered_funds = df_funds[df_funds[risk_col].astype(str).str.lower() == str(target_grade).lower()]
    
    if filtered_funds.empty:
        print(f"No funds found matching risk profile: {target_grade}")
        print(f"Available options in {risk_col}: {df_funds[risk_col].unique()}")
        return filtered_funds
        
    print(filtered_funds)
    return filtered_funds

user_input = "High" 
get_recommendations(user_input)