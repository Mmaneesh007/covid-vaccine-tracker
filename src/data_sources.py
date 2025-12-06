"""
Multi-source data integration for vaccination data.
Supports OWID (primary), CDC (secondary), and future sources.
"""
import pandas as pd
import requests
import time
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

# Data source constants
DATA_SOURCE_OWID = "OWID"
DATA_SOURCE_CDC = "CDC"
DATA_SOURCE_WHO = "WHO"

# Cache directory for API responses
CACHE_DIR = "data/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Request timeout and retry settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds


class DataSourceError(Exception):
    """Custom exception for data source errors"""
    pass


class DataSource:
    """Base class for data sources"""
    
    def __init__(self, name: str, cache_ttl: int = 3600):
        """
        Initialize data source.
        
        Args:
            name: Name of the data source
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.name = name
        self.cache_ttl = cache_ttl
        self.last_fetch_time = None
        self.last_fetch_data = None
    
    def fetch(self, **kwargs) -> pd.DataFrame:
        """
        Fetch data from source. Must be implemented by subclasses.
        
        Returns:
            pd.DataFrame: Vaccination data
        """
        raise NotImplementedError("Subclasses must implement fetch()")
    
    def is_available(self) -> bool:
        """
        Check if data source is available.
        
        Returns:
            bool: True if available, False otherwise
        """
        try:
            # Quick health check
            test_data = self.fetch(limit=1)
            return test_data is not None and not test_data.empty
        except Exception as e:
            logger.warning(f"{self.name} health check failed: {e}")
            return False
    
    def _make_request(self, url: str, params: Optional[Dict] = None, 
                     headers: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: Request URL
            params: Query parameters
            headers: Request headers
            
        Returns:
            requests.Response: HTTP response
            
        Raises:
            DataSourceError: If request fails after retries
        """
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url, 
                    params=params, 
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                    time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
                else:
                    raise DataSourceError(f"Failed to fetch from {self.name}: {e}")
    
    def _validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate fetched data.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if df is None or df.empty:
            return False
        
        # Check for required columns
        required_cols = ['location', 'date']
        if not all(col in df.columns for col in required_cols):
            logger.error(f"{self.name}: Missing required columns. Got: {df.columns.tolist()}")
            return False
        
        # Check for impossible values
        if 'total_vaccinations' in df.columns:
            if (df['total_vaccinations'] < 0).any():
                logger.warning(f"{self.name}: Found negative vaccination numbers")
                return False
            if (df['total_vaccinations'] > 20_000_000_000).any():
                logger.warning(f"{self.name}: Found impossibly high vaccination numbers")
                return False
        
        return True


class OWIDSource(DataSource):
    """Our World in Data data source (primary)"""
    
    def __init__(self):
        super().__init__(DATA_SOURCE_OWID, cache_ttl=7200)  # 2 hours
        self.url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    
    def fetch(self, **kwargs) -> pd.DataFrame:
        """Fetch data from OWID"""
        try:
            logger.info(f"Fetching data from {self.name}...")
            response = self._make_request(self.url)
            
            # Read CSV from response
            from io import StringIO
            df = pd.read_csv(StringIO(response.text), parse_dates=["date"])
            
            # Rename 'location' column if it exists (OWID uses 'location')
            if 'location' not in df.columns and 'country' in df.columns:
                df['location'] = df['country']
            
            logger.info(f"{self.name}: Fetched {len(df):,} records")
            
            if not self._validate_data(df):
                raise DataSourceError(f"{self.name}: Data validation failed")
            
            return df
            
        except Exception as e:
            logger.error(f"{self.name} fetch error: {e}")
            raise DataSourceError(f"Failed to fetch from {self.name}: {e}")


class CDCSource(DataSource):
    """CDC data source (secondary, US-focused)"""
    
    def __init__(self):
        super().__init__(DATA_SOURCE_CDC, cache_ttl=3600)  # 1 hour
        # CDC COVID-19 Vaccination Data API endpoint
        # Note: CDC primarily has US state-level data, not global
        self.base_url = "https://data.cdc.gov/resource"
        self.vaccination_endpoint = f"{self.base_url}/unsk-b7fc.json"  # COVID-19 Vaccinations
    
    def fetch(self, country: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Fetch data from CDC.
        
        Note: CDC primarily provides US state-level data.
        For global data, this will return US data only.
        
        Args:
            country: Country name (ignored for CDC, always returns US data)
            
        Returns:
            pd.DataFrame: Vaccination data (US states)
        """
        try:
            logger.info(f"Fetching data from {self.name}...")
            
            # CDC API parameters
            params = {
                '$limit': 50000,  # Get all records
                '$order': 'date DESC'  # Most recent first
            }
            
            # Add date filter to get recent data (last 2 years)
            two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
            params['$where'] = f"date >= '{two_years_ago}'"
            
            response = self._make_request(self.vaccination_endpoint, params=params)
            data = response.json()
            
            if not data:
                logger.warning(f"{self.name}: No data returned")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Normalize CDC data to match OWID format
            df = self._normalize_cdc_data(df)
            
            logger.info(f"{self.name}: Fetched {len(df):,} records")
            
            if not self._validate_data(df):
                raise DataSourceError(f"{self.name}: Data validation failed")
            
            return df
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"{self.name}: Endpoint not found, may need to update URL")
            raise DataSourceError(f"CDC API error: {e}")
        except Exception as e:
            logger.error(f"{self.name} fetch error: {e}")
            raise DataSourceError(f"Failed to fetch from {self.name}: {e}")
    
    def _normalize_cdc_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize CDC data format to match OWID format.
        
        CDC columns may vary, so we map them to standard format.
        """
        # Create normalized DataFrame
        normalized = pd.DataFrame()
        
        # Map date
        if 'date' in df.columns:
            normalized['date'] = pd.to_datetime(df['date'], errors='coerce')
        elif 'administered_date' in df.columns:
            normalized['date'] = pd.to_datetime(df['administered_date'], errors='coerce')
        
        # Map location (CDC has state-level data, aggregate to "United States")
        normalized['location'] = 'United States'
        normalized['data_source'] = DATA_SOURCE_CDC
        
        # Map vaccination metrics
        # CDC column names may vary, try common variations
        if 'total_doses_administered' in df.columns:
            normalized['total_vaccinations'] = pd.to_numeric(
                df['total_doses_administered'], errors='coerce'
            )
        elif 'administered_dose1' in df.columns and 'administered_dose2' in df.columns:
            # Sum doses if separate columns
            normalized['total_vaccinations'] = (
                pd.to_numeric(df['administered_dose1'], errors='coerce').fillna(0) +
                pd.to_numeric(df['administered_dose2'], errors='coerce').fillna(0)
            )
        
        if 'administered_dose1' in df.columns:
            normalized['people_vaccinated'] = pd.to_numeric(
                df['administered_dose1'], errors='coerce'
            )
        
        if 'administered_dose2' in df.columns:
            normalized['people_fully_vaccinated'] = pd.to_numeric(
                df['administered_dose2'], errors='coerce'
            )
        
        # Calculate daily vaccinations if not present
        if 'total_vaccinations' in normalized.columns:
            normalized = normalized.sort_values('date')
            normalized['daily_vaccinations'] = normalized['total_vaccinations'].diff().fillna(0).clip(lower=0)
        
        # Remove rows with invalid dates
        normalized = normalized.dropna(subset=['date'])
        
        # Aggregate by date (in case of multiple records per date)
        if not normalized.empty:
            agg_dict = {
                'location': 'first',
                'data_source': 'first',
                'total_vaccinations': 'max',
                'people_vaccinated': 'max',
                'people_fully_vaccinated': 'max',
                'daily_vaccinations': 'sum'
            }
            normalized = normalized.groupby('date').agg(agg_dict).reset_index()
        
        return normalized


class DataSourceManager:
    """Manages multiple data sources with fallback logic"""
    
    def __init__(self):
        self.sources = {
            DATA_SOURCE_OWID: OWIDSource(),
            DATA_SOURCE_CDC: CDCSource(),
        }
        self.primary_source = DATA_SOURCE_OWID
        self.fallback_sources = [DATA_SOURCE_CDC]
    
    def get_data(self, source_preference: Optional[str] = None, 
                 use_fallback: bool = True) -> pd.DataFrame:
        """
        Get data from preferred source with automatic fallback.
        
        Args:
            source_preference: Preferred source name (None = use primary)
            use_fallback: Whether to use fallback sources if primary fails
            
        Returns:
            pd.DataFrame: Vaccination data
            
        Raises:
            DataSourceError: If all sources fail
        """
        # Determine source order
        if source_preference and source_preference in self.sources:
            sources_to_try = [source_preference]
            if use_fallback:
                sources_to_try.extend([s for s in self.fallback_sources if s != source_preference])
        else:
            sources_to_try = [self.primary_source]
            if use_fallback:
                sources_to_try.extend(self.fallback_sources)
        
        last_error = None
        
        for source_name in sources_to_try:
            source = self.sources[source_name]
            try:
                logger.info(f"Attempting to fetch from {source_name}...")
                df = source.fetch()
                
                if df is not None and not df.empty:
                    # Add data source column
                    if 'data_source' not in df.columns:
                        df['data_source'] = source_name
                    
                    logger.info(f"Successfully fetched {len(df):,} records from {source_name}")
                    return df
                else:
                    logger.warning(f"{source_name} returned empty data")
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to fetch from {source_name}: {e}")
                continue
        
        # All sources failed
        raise DataSourceError(
            f"All data sources failed. Last error: {last_error}"
        )
    
    def get_available_sources(self) -> List[str]:
        """Get list of available data sources"""
        available = []
        for name, source in self.sources.items():
            try:
                if source.is_available():
                    available.append(name)
            except:
                pass
        return available
    
    def get_data_with_source_info(self, source_preference: Optional[str] = None) -> Dict:
        """
        Get data with source information.
        
        Returns:
            dict: {
                'data': pd.DataFrame,
                'source': str,
                'timestamp': str,
                'fallback_used': bool
            }
        """
        source_used = None
        fallback_used = False
        
        # Try primary source first
        try:
            if source_preference and source_preference in self.sources:
                source_used = source_preference
            else:
                source_used = self.primary_source
            
            df = self.sources[source_used].fetch()
            if df is not None and not df.empty:
                if 'data_source' not in df.columns:
                    df['data_source'] = source_used
        except Exception as e:
            logger.warning(f"Primary source {source_used} failed: {e}")
            fallback_used = True
            df = self.get_data(use_fallback=True)
            # Determine which source was actually used
            if 'data_source' in df.columns:
                source_used = df['data_source'].iloc[0] if not df.empty else None
        
        return {
            'data': df,
            'source': source_used or 'unknown',
            'timestamp': datetime.now().isoformat(),
            'fallback_used': fallback_used
        }


# Global instance
_data_source_manager = None

def get_data_source_manager() -> DataSourceManager:
    """Get global data source manager instance"""
    global _data_source_manager
    if _data_source_manager is None:
        _data_source_manager = DataSourceManager()
    return _data_source_manager


if __name__ == "__main__":
    # Test data sources
    logging.basicConfig(level=logging.INFO)
    
    manager = get_data_source_manager()
    
    print("Testing data sources...")
    print(f"Available sources: {manager.get_available_sources()}")
    
    print("\nFetching data from primary source (OWID)...")
    try:
        df = manager.get_data()
        print(f"✓ Successfully fetched {len(df):,} records")
        print(f"  Columns: {df.columns.tolist()}")
        print(f"  Countries: {df['location'].nunique() if 'location' in df.columns else 'N/A'}")
        if 'data_source' in df.columns:
            print(f"  Data source: {df['data_source'].unique()}")
    except Exception as e:
        print(f"✗ Failed: {e}")

