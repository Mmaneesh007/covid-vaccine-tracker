import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath('.'))

from src.storage import DB_PATH
from sqlalchemy import create_engine

def reproduce():
    if os.path.exists(DB_PATH):
        print(f"Database found at {DB_PATH}")
        engine = create_engine(f"sqlite:///{DB_PATH}")
        df = pd.read_sql("SELECT * FROM countries_vaccinations", engine, parse_dates=["date"])
        print(f"Loaded {len(df)} records")
        
        # Simulate logic from streamlit_app.py
        latest_date = df['date'].max()
        print(f"Latest date: {latest_date}")
        
        latest_by_country = df[df['date'] == latest_date].copy()
        print(f"Records for latest date: {len(latest_by_country)}")
        
        print("Dtypes before conversion:")
        print(latest_by_country.dtypes)

        print("Converting pct_vaccinated to numeric...")
        latest_by_country['pct_vaccinated'] = pd.to_numeric(latest_by_country['pct_vaccinated'], errors='coerce')
        
        print("Attempting nlargest...")
        try:
            top_countries = latest_by_country.nlargest(10, 'pct_vaccinated')[
                ['location', 'pct_vaccinated', 'pct_fully_vaccinated', 'total_vaccinations', 'daily_vaccinations_7d']
            ].copy()
            print("Success nlargest!")
            print(top_countries)
            
            top_countries.columns = ['Country', 'Vaccinated (%)', 'Fully Vaccinated (%)', 
                                      'Total Doses', '7-Day Avg Daily']
            
            print("Attempting formatting...")
            # Format numbers
            top_countries['Total Doses'] = top_countries['Total Doses'].apply(
                lambda x: f"{x / 1e6:.2f}M" if pd.notna(x) else "N/A"
            )
            print("Formatted Total Doses")
            
            top_countries['7-Day Avg Daily'] = top_countries['7-Day Avg Daily'].apply(
                lambda x: f"{x / 1e3:.1f}K" if pd.notna(x) else "N/A"
            )
            print("Formatted 7-Day Avg Daily")

            top_countries['Vaccinated (%)'] = top_countries['Vaccinated (%)'].apply(
                lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A"
            )
            print("Formatted Vaccinated (%)")

            top_countries['Fully Vaccinated (%)'] = top_countries['Fully Vaccinated (%)'].apply(
                lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A"
            )
            print("Formatted Fully Vaccinated (%)")
            
            print("All operations successful")
            
        except Exception as e:
            print(f"Caught expected error: {e}")
            import traceback
            traceback.print_exc()

    else:
        print("Database not found. Please run ETL first.")

if __name__ == "__main__":
    reproduce()
