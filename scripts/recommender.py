import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

# Resolve DB path relative to this script's location (scripts/ -> project root)
_PROJECT_ROOT = Path(__file__).parent.parent
db_path = str(_PROJECT_ROOT / "data" / "db" / "bluestock_mf.db")

if not Path(db_path).exists() or Path(db_path).stat().st_size == 0:
    raise FileNotFoundError(
        f"Database not found or empty at: {db_path}\n"
        "Run: python scripts/rebuild_db.py"
    )


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