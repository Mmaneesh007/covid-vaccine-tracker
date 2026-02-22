# src/etl.py
import os
import time
import pandas as pd
import requests
import logging

# Setup logger BEFORE any code that uses it
logger = logging.getLogger(__name__)

# Import new data source manager (with fallback if not available)
try:
    from src.data_sources import get_data_source_manager, DATA_SOURCE_OWID
    MULTI_SOURCE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Multi-source data not available: {e}. Using legacy OWID-only mode.")
    MULTI_SOURCE_AVAILABLE = False
    DATA_SOURCE_OWID = "OWID"  # Fallback constant

# Legacy OWID URL (kept for backward compatibility)
OWID_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "owid-covid-data.csv")
MAX_AGE = 2 * 3600  # Reduced from 24 hours to 2 hours for fresher data

os.makedirs(DATA_DIR, exist_ok=True)

def download_csv():
    """
    Download the OWID vaccination CSV file (legacy method).
    Uses caching: skips download if file exists and is less than 2 hours old.
    
    Returns:
        str: Path to the downloaded CSV file
    """
    if os.path.exists(CSV_PATH) and (time.time() - os.path.getmtime(CSV_PATH)) < MAX_AGE:
        logger.info("Using cached CSV")
        return CSV_PATH
    
    logger.info(f"Downloading vaccination data from {OWID_URL}...")
    r = requests.get(OWID_URL, timeout=30)
    r.raise_for_status()
    
    with open(CSV_PATH, "wb") as f:
        f.write(r.content)
    
    logger.info(f"Downloaded CSV to {CSV_PATH}")
    return CSV_PATH

def load_data(use_multi_source: bool = True, source_preference: str = None):
    """
    Load vaccination data from multiple sources with automatic fallback.
    
    Args:
        use_multi_source: If True, use new multi-source system. If False, use legacy OWID-only.
        source_preference: Preferred source (DATA_SOURCE_OWID, DATA_SOURCE_CDC, etc.)
    
    Returns:
        pd.DataFrame: Vaccination data with parsed date column and 'data_source' column
    """
    if use_multi_source and MULTI_SOURCE_AVAILABLE:
        try:
            manager = get_data_source_manager()
            result = manager.get_data_with_source_info(source_preference=source_preference)
            df = result['data']
            
            logger.info(f"Loaded {len(df):,} records from {result['source']}")
            if result['fallback_used']:
                logger.warning("Fallback source was used - primary source may be unavailable")
            
            # Ensure 'date' is datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Log data source info
            if 'data_source' in df.columns:
                sources = df['data_source'].value_counts()
                logger.info(f"Data sources: {sources.to_dict()}")
            
            return df
            
        except Exception as e:
            logger.error(f"Multi-source fetch failed: {e}")
            logger.info("Falling back to legacy OWID-only method...")
            # Fall through to legacy method
    elif use_multi_source and not MULTI_SOURCE_AVAILABLE:
        logger.info("Multi-source requested but not available, using legacy OWID-only method...")
        # Fall through to legacy method
    
    # Legacy method: OWID only
    download_csv()
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    
    # Add data_source column for consistency
    if 'data_source' not in df.columns:
        df['data_source'] = DATA_SOURCE_OWID
    
    logger.info(f"Loaded {len(df):,} records (legacy method)")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    return df

if __name__ == "__main__":
    df = load_data()
    print(f"\nDataset summary:")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Countries: {df['location'].nunique()}")
