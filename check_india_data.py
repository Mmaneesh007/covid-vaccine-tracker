import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "data/vax_tracker.db"

if os.path.exists(DB_PATH):
    engine = create_engine(f"sqlite:///{DB_PATH}")
    query = "SELECT date, new_deaths_smoothed_per_million, new_deaths_smoothed FROM countries_vaccinations WHERE location = 'India' ORDER BY date DESC LIMIT 10"
    try:
        df = pd.read_sql(query, engine)
        print("Data for India:")
        print(df)
        
        print("\nNull count:")
        print(df.isnull().sum())
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Database not found")
