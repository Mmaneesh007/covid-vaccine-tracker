import os
import pandas as pd
from src.etl import load_data, CSV_PATH
from src.clean import clean_vax
from src.storage import save_df_to_db, DB_PATH
from sqlalchemy import create_engine

def fix_missing_data():
    print("Fixing missing data...")
    
    # 1. Force delete cached CSV to ensure fresh data
    if os.path.exists(CSV_PATH):
        print(f"Removing cached CSV: {CSV_PATH}")
        os.remove(CSV_PATH)
    
    # 2. Load data
    print("Loading fresh data...")
    df = load_data()
    
    # Check if column exists in raw data
    col = "new_deaths_smoothed_per_million"
    if col in df.columns:
        print(f"Column '{col}' found in raw CSV.")
    else:
        print(f"Column '{col}' NOT found in raw CSV. It will be added by clean_vax.")
        
    # 3. Clean data
    print("Cleaning data...")
    df_clean = clean_vax(df)
    
    # Check if column exists in cleaned data
    if col in df_clean.columns:
        print(f"Column '{col}' found in cleaned DataFrame.")
        print(f"Non-null count: {df_clean[col].count()}")
    else:
        print(f"CRITICAL: Column '{col}' missing from cleaned DataFrame!")
        return
        
    # 4. Save to DB
    print("Saving to database...")
    save_df_to_db(df_clean)
    
    # 5. Verify DB
    print("Verifying database...")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    try:
        df_db = pd.read_sql(f"SELECT {col} FROM countries_vaccinations LIMIT 5", engine)
        print("Column successfully queried from DB!")
        print(df_db.head())
    except Exception as e:
        print(f"DB Verification Failed: {e}")

if __name__ == "__main__":
    fix_missing_data()
