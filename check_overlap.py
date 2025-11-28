import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "data/vax_tracker.db"

def check_india_overlap():
    if os.path.exists(DB_PATH):
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        query = """
        SELECT 
            date,
            pct_vaccinated,
            new_deaths_smoothed_per_million,
            new_deaths_smoothed,
            population,
            people_vaccinated
        FROM countries_vaccinations 
        WHERE location = 'India'
        ORDER BY date
        """
        
        try:
            df = pd.read_sql(query, engine)
            print(f"Total rows for India: {len(df)}")
            
            # Check non-null counts
            print("\nNon-null counts:")
            print(df.count())
            
            # Check overlap
            overlap = df.dropna(subset=['pct_vaccinated', 'new_deaths_smoothed_per_million'])
            print(f"\nRows with BOTH pct_vaccinated and new_deaths_smoothed_per_million: {len(overlap)}")
            
            if len(overlap) == 0:
                print("NO OVERLAP! Let's check if we can construct it.")
                
                # Check if we have raw components for death rate
                df['calculated_death_rate'] = (df['new_deaths_smoothed'] / df['population']) * 1_000_000
                
                # Check overlap with calculated rate
                overlap_calc = df.dropna(subset=['pct_vaccinated', 'calculated_death_rate'])
                print(f"Rows with pct_vaccinated and CALCULATED death rate: {len(overlap_calc)}")
                
                if len(overlap_calc) > 0:
                    print("We can fix this by calculating the death rate!")
                else:
                    print("Still no overlap. Let's look at why pct_vaccinated is missing.")
                    print(df[['date', 'people_vaccinated', 'population', 'pct_vaccinated']].tail(10))

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Database not found")

if __name__ == "__main__":
    check_india_overlap()
