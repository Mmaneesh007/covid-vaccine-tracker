import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "data/vax_tracker.db"

def check_india_coverage():
    if os.path.exists(DB_PATH):
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        # Check total count and non-null count for India
        query = """
        SELECT 
            COUNT(*) as total_rows,
            COUNT(new_deaths_smoothed_per_million) as non_null_deaths_per_million,
            COUNT(new_deaths_smoothed) as non_null_deaths,
            COUNT(population) as non_null_population
        FROM countries_vaccinations 
        WHERE location = 'India'
        """
        
        try:
            df = pd.read_sql(query, engine)
            print("Coverage for India:")
            print(df)
            
            # Check if we can calculate it
            if df['non_null_deaths_per_million'][0] == 0:
                print("\nColumn is empty! Checking if we can calculate it...")
                if df['non_null_deaths'][0] > 0 and df['non_null_population'][0] > 0:
                    print("Yes, we have raw deaths and population. We should calculate it in ETL.")
                else:
                    print("No, we are missing raw deaths or population.")
            else:
                print(f"\nColumn has {df['non_null_deaths_per_million'][0]} non-null values.")
                
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Database not found")

if __name__ == "__main__":
    check_india_coverage()
