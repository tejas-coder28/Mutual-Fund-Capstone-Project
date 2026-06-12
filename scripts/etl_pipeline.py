"""
etl_pipeline.py
---------------
End-to-end ETL pipeline: ingests raw data, cleans it, and loads it into the SQLite DB.

Usage:
  python scripts/etl_pipeline.py            # Full pipeline (needs data/raw/*.csv)
  python scripts/etl_pipeline.py --rebuild  # Rebuild DB from existing processed CSVs
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR  = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
RAW_DIR      = PROJECT_ROOT / "data" / "raw"


def run_step(script_name: str):
    print(f"\n{'='*50}")
    print(f"Running: {script_name}")
    print('='*50)
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name)],
        check=True
    )


def has_raw_data() -> bool:
    return len(list(RAW_DIR.glob("*.csv"))) > 0


if __name__ == "__main__":
    rebuild_only = "--rebuild" in sys.argv

    if rebuild_only or not has_raw_data():
        if not rebuild_only:
            print("[INFO] data/raw/ is empty. Falling back to rebuilding DB from processed CSVs.")
        run_step("rebuild_db.py")
    else:
        run_step("data_ingestion.py")
        run_step("data_cleaning_and_loading.py")

    print("\n[DONE] ETL pipeline completed successfully.")
