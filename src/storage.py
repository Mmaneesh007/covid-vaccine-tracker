# src/storage.py
import sqlalchemy as sa
import pandas as pd
import os

# Database path
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "vax_tracker.db")
DB_URL = f"sqlite:///{DB_PATH}"

os.makedirs(DB_DIR, exist_ok=True)

def save_df_to_db(df, table_name="countries_vaccinations"):
    """
    Save DataFrame to SQLite database.
    
    Args:
        df (pd.DataFrame): Data to save
        table_name (str): Name of the table to create/replace
    """
    engine = sa.create_engine(DB_URL)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Saved {len(df):,} records to {DB_URL} (table: {table_name})")

def get_latest_by_country(limit=100):
    """
    Query the latest vaccination statistics per country.
    
    Args:
        limit (int): Maximum number of countries to return
    
    Returns:
        pd.DataFrame: Latest stats per country, ordered by vaccination percentage
    """
    engine = sa.create_engine(DB_URL)
    
    query = """
    WITH latest_dates AS (
        SELECT location, MAX(date) as max_date
        FROM countries_vaccinations
        WHERE total_vaccinations IS NOT NULL
        GROUP BY location
    )
    SELECT t1.*
    FROM countries_vaccinations t1
    JOIN latest_dates t2 ON t1.location = t2.location AND t1.date = t2.max_date
    ORDER BY t1.pct_vaccinated DESC
    LIMIT :limit
    """
    
    return pd.read_sql_query(query, engine, params={"limit": limit})

def get_country_timeseries(country_name):
    """
    Get complete time series data for a specific country.
    
    Args:
        country_name (str): Name of the country
    
    Returns:
        pd.DataFrame: Time series data for the country
    """
    engine = sa.create_engine(DB_URL)
    
    query = """
    SELECT *
    FROM countries_vaccinations
    WHERE location = :country
    ORDER BY date
    """
    
    return pd.read_sql_query(query, engine, params={"country": country_name}, 
                             parse_dates=["date"])

def get_all_countries():
    """
    Get a list of all unique countries in the database.
    
    Returns:
        list: List of country names
    """
    engine = sa.create_engine(DB_URL)
    query = "SELECT DISTINCT location FROM countries_vaccinations ORDER BY location"
    df = pd.read_sql_query(query, engine)
    return df["location"].tolist()

if __name__ == "__main__":
    # Test database operations
    from etl import load_data
    from clean import clean_vax
    
    print("Loading and cleaning data...")
    df = load_data()
    df_clean = clean_vax(df)
    
    print("\nSaving to database...")
    save_df_to_db(df_clean)
    
    print("\nQuerying latest stats...")
    latest = get_latest_by_country(limit=10)
    print(latest)
