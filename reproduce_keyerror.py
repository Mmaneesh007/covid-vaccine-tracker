import pandas as pd
import sys
import os
from sqlalchemy import create_engine

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath('.'))

from src.storage import DB_PATH

def reproduce_keyerror():
    print("Reproducing KeyError...")
    if os.path.exists(DB_PATH):
        engine = create_engine(f"sqlite:///{DB_PATH}")
        df = pd.read_sql("SELECT * FROM countries_vaccinations", engine, parse_dates=["date"])
        print(f"Loaded {len(df)} records")
        print("Columns:", df.columns.tolist())
        
        if 'new_deaths_smoothed_per_million' not in df.columns:
            print("CRITICAL: 'new_deaths_smoothed_per_million' missing from DF!")
            return

        # Simulate selection
        selected_countries = ['India', 'United States']
        country_data = df[df['location'].isin(selected_countries)].copy()
        print(f"Country data columns: {country_data.columns.tolist()}")
        
        impact_country = 'India'
        country_impact_data = country_data[country_data['location'] == impact_country].copy()
        print(f"Impact data columns: {country_impact_data.columns.tolist()}")
        
        try:
            val = country_impact_data['new_deaths_smoothed_per_million']
            print("Successfully accessed 'new_deaths_smoothed_per_million'")
            print(val.head())
        except KeyError as e:
            print(f"Caught KeyError: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}")

    else:
        print("DB not found")

if __name__ == "__main__":
    reproduce_keyerror()
