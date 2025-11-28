# src/etl.py
import os
import time
import pandas as pd
import requests

OWID_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "owid-covid-data.csv")
MAX_AGE = 24 * 3600  # seconds (24 hours)

os.makedirs(DATA_DIR, exist_ok=True)

def download_csv():
    """
    Download the OWID vaccination CSV file.
    Uses caching: skips download if file exists and is less than 24 hours old.
    
    Returns:
        str: Path to the downloaded CSV file
    """
    if os.path.exists(CSV_PATH) and (time.time() - os.path.getmtime(CSV_PATH)) < MAX_AGE:
        print("Using cached CSV")
        return CSV_PATH
    
    print(f"Downloading vaccination data from {OWID_URL}...")
    r = requests.get(OWID_URL, timeout=30)
    r.raise_for_status()
    
    with open(CSV_PATH, "wb") as f:
        f.write(r.content)
    
    print(f"Downloaded CSV to {CSV_PATH}")
    return CSV_PATH

def load_data():
    """
    Download (if needed) and load vaccination data into pandas DataFrame.
    
    Returns:
        pd.DataFrame: Vaccination data with parsed date column
    """
    download_csv()
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    
    print(f"Loaded {len(df):,} records")
    print("Columns:", df.columns.tolist())
    print("\nSample data:")
    print(df.head(3).to_string(index=False))
    
    return df

if __name__ == "__main__":
    df = load_data()
    print(f"\nDataset summary:")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Countries: {df['location'].nunique()}")
