#!/usr/bin/env python
# run_all.py
"""
End-to-end automation script for COVID-19 Vaccine Tracker ETL pipeline.
Downloads latest data, cleans it, and stores in SQLite database.
"""
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.etl import load_data
from src.clean import clean_vax
from src.storage import save_df_to_db, get_latest_by_country

def main():
    """Execute complete ETL pipeline"""
    print("=" * 70)
    print("COVID-19 Vaccine Tracker - ETL Pipeline")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Step 1: Download/Load Data
        print("Step 1: Downloading vaccination data...")
        print("-" * 70)
        df_raw = load_data()
        print(f"[+] Loaded {len(df_raw):,} raw records")
        print()
        
        # Step 2: Clean and Transform
        print("Step 2: Cleaning and transforming data...")
        print("-" * 70)
        df_clean = clean_vax(df_raw)
        print(f"[+] Cleaned data: {len(df_clean):,} records")
        print()
        
        # Step 3: Save to Database
        print("Step 3: Saving to database...")
        print("-" * 70)
        save_df_to_db(df_clean)
        print("[+] Data saved successfully")
        print()
        
        # Step 4: Summary Statistics
        print("Step 4: Summary Statistics")
        print("=" * 70)
        
        print(f"Date Range: {df_clean['date'].min()} to {df_clean['date'].max()}")
        print(f"Countries/Regions: {df_clean['location'].nunique()}")
        print(f"Total Records: {len(df_clean):,}")
        print()
        
        # Get latest stats for top countries
        print("Top 10 Countries by Vaccination Coverage:")
        print("-" * 70)
        latest = get_latest_by_country(limit=10)
        
        for idx, row in latest.iterrows():
            pct = row['pct_vaccinated'] if not pd.isna(row['pct_vaccinated']) else 0
            total = row['total_vaccinations'] if not pd.isna(row['total_vaccinations']) else 0
            print(f"{idx+1:2d}. {row['location']:25s} - {pct:5.2f}% ({total/1e6:8.2f}M doses)")
        
        print()
        print("=" * 70)
        print("[+] ETL Pipeline completed successfully!")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  • Run dashboard: streamlit run app/streamlit_app.py")
        print("  • Run tests: pytest tests/ -v")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("[!] ERROR: ETL Pipeline failed!")
        print("=" * 70)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return 1

if __name__ == "__main__":
    import pandas as pd  # Import here for the main block
    exit_code = main()
    sys.exit(exit_code)
