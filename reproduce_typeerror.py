import pandas as pd
import sys
import os
from sqlalchemy import create_engine

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath('.'))

from src.storage import DB_PATH

def reproduce_typeerror():
    print("Reproducing TypeError...")
    if os.path.exists(DB_PATH):
        engine = create_engine(f"sqlite:///{DB_PATH}")
        df = pd.read_sql("SELECT * FROM countries_vaccinations", engine, parse_dates=["date"])
        
        latest_date = df['date'].max()
        latest_by_country = df[df['date'] == latest_date].copy()
        
        print(f"Latest date: {latest_date}")
        print(f"Records for latest date: {len(latest_by_country)}")
        print("Dtypes before conversion:")
        print(latest_by_country.dtypes)

        # Ensure numeric types for sorting and formatting
        numeric_cols = ['pct_vaccinated', 'pct_fully_vaccinated', 'total_vaccinations', 'daily_vaccinations_7d']
        for col in numeric_cols:
            # Simulate what happens in the app
            latest_by_country[col] = pd.to_numeric(latest_by_country[col], errors='coerce')

        if not latest_by_country.empty:
            try:
                top_countries = latest_by_country.nlargest(10, 'pct_vaccinated')[
                    ['location', 'pct_vaccinated', 'pct_fully_vaccinated', 'total_vaccinations', 'daily_vaccinations_7d']
                ].copy()
                
                top_countries.columns = ['Country', 'Vaccinated (%)', 'Fully Vaccinated (%)', 
                                          'Total Doses', '7-Day Avg Daily']
                
                print("Top countries selected. Now formatting...")
                
                # Format numbers safely - THIS IS WHERE THE ERROR IS SUSPECTED
                print("Formatting 'Total Doses'...")
                top_countries['Total Doses'] = top_countries['Total Doses'].apply(
                    lambda x: f"{x / 1e6:.2f}M" if pd.notna(x) and isinstance(x, (int, float)) else "N/A"
                )
                print("Success 'Total Doses'")

                print("Formatting '7-Day Avg Daily'...")
                top_countries['7-Day Avg Daily'] = top_countries['7-Day Avg Daily'].apply(
                    lambda x: f"{x / 1e3:.1f}K" if pd.notna(x) and isinstance(x, (int, float)) else "N/A"
                )
                print("Success '7-Day Avg Daily'")

                print("Formatting 'Vaccinated (%)'...")
                top_countries['Vaccinated (%)'] = top_countries['Vaccinated (%)'].apply(
                    lambda x: f"{x:.2f}%" if pd.notna(x) and isinstance(x, (int, float)) else "N/A"
                )
                print("Success 'Vaccinated (%)'")

                print("Formatting 'Fully Vaccinated (%)'...")
                top_countries['Fully Vaccinated (%)'] = top_countries['Fully Vaccinated (%)'].apply(
                    lambda x: f"{x:.2f}%" if pd.notna(x) and isinstance(x, (int, float)) else "N/A"
                )
                print("Success 'Fully Vaccinated (%)'")
                
                print("All formatting successful!")
                print(top_countries)
                
            except Exception as e:
                print(f"CAUGHT EXCEPTION: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("No data for latest date")

    else:
        print("DB not found")

if __name__ == "__main__":
    reproduce_typeerror()
