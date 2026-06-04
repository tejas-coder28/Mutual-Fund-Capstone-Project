import os
import requests
import pandas as pd

def fetch_live_nav():
    schemes = {
        "125497": "HDFC_Top_100_Direct",
        "119551": "SBI_Bluechip",
        "120503": "ICICI_Bluechip",
        "118632": "Nippon_Large_Cap",
        "119092": "Axis_Bluechip",
        "120841": "Kotak_Bluechip"
    }
    
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    for code, name in schemes.items():
        print(f"Fetching data for {name} ({code})...")
        url = f"https://api.mfapi.in/mf/{code}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                json_data = response.json()
                nav_data = json_data.get("data", [])
                
                if not nav_data:
                    print(f"No data array returned for {name}")
                    continue
                
                df = pd.DataFrame(nav_data)
                df["scheme_code"] = code
                df["scheme_name"] = json_data.get("meta", {}).get("scheme_name", name)
                
                csv_path = os.path.join(output_dir, f"{name}_live_raw.csv")
                df.to_csv(csv_path, index=False)
                print(f"Saved {len(df)} records to {csv_path}")
            else:
                print(f"Failed to get data for {name}. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"An error occurred while downloading {name}: {e}")

if __name__ == "__main__":
    fetch_live_nav()