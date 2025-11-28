import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "data/vax_tracker.db"

if os.path.exists(DB_PATH):
    print(f"Database found at {DB_PATH}")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    try:
        df = pd.read_sql("SELECT * FROM countries_vaccinations LIMIT 5", engine)
        print("Columns in database:")
        print(df.columns.tolist())
        
        if 'new_deaths_smoothed_per_million' in df.columns:
            print("\nColumn 'new_deaths_smoothed_per_million' EXISTS.")
        else:
            print("\nColumn 'new_deaths_smoothed_per_million' is MISSING.")
            
    except Exception as e:
        print(f"Error reading database: {e}")
else:
    print("Database not found.")
