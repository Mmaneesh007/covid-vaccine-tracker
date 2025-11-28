# tests/test_etl.py
"""
Unit and integration tests for COVID-19 Vaccine Tracker ETL pipeline
"""
import pytest
import pandas as pd
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etl import download_csv, load_data, CSV_PATH
from src.clean import clean_vax
from src.storage import save_df_to_db, get_latest_by_country, get_country_timeseries, DB_PATH
from src.forecast import fit_prophet_for_country, forecast_country_with_history


class TestETL:
    """Test data extraction and loading"""
    
    def test_download_csv(self):
        """Test CSV download functionality"""
        csv_path = download_csv()
        assert os.path.exists(csv_path), "CSV file should be downloaded"
        assert csv_path == CSV_PATH, "Should return correct path"
    
    def test_load_data(self):
        """Test data loading into DataFrame"""
        df = load_data()
        
        # Check DataFrame structure
        assert isinstance(df, pd.DataFrame), "Should return DataFrame"
        assert len(df) > 0, "DataFrame should not be empty"
        
        # Check required columns
        required_cols = ['location', 'date']
        for col in required_cols:
            assert col in df.columns, f"DataFrame should have '{col}' column"
        
        # Check date parsing
        assert pd.api.types.is_datetime64_any_dtype(df['date']), "Date column should be datetime"
    
    def test_load_data_caching(self):
        """Test that caching works (second call should be faster)"""
        import time
        
        # First call
        start1 = time.time()
        df1 = load_data()
        time1 = time.time() - start1
        
        # Second call (should use cache)
        start2 = time.time()
        df2 = load_data()
        time2 = time.time() - start2
        
        assert df1.equals(df2), "Cached data should match original"


class TestCleaning:
    """Test data cleaning and transformation"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample vaccination data for testing"""
        return pd.DataFrame({
            'location': ['TestCountry'] * 10,
            'date': pd.date_range('2024-01-01', periods=10),
            'total_vaccinations': [100, 200, 350, 500, 700, 900, 1100, 1300, 1500, 1700],
            'people_vaccinated': [80, 150, 250, 350, 480, 620, 770, 920, 1070, 1220],
            'people_fully_vaccinated': [50, 100, 180, 270, 370, 480, 600, 720, 840, 960],
            'daily_vaccinations': [None, 100, 150, 150, 200, 200, 200, 200, 200, 200],
            'population': [10000] * 10
        })
    
    def test_clean_vax_basic(self, sample_data):
        """Test basic cleaning functionality"""
        df_clean = clean_vax(sample_data)
        
        # Should not be empty
        assert len(df_clean) > 0, "Cleaned data should not be empty"
        
        # Should have required columns
        assert 'location' in df_clean.columns
        assert 'date' in df_clean.columns
        assert 'daily_vaccinations' in df_clean.columns
    
    def test_clean_vax_rolling_average(self, sample_data):
        """Test 7-day rolling average calculation"""
        df_clean = clean_vax(sample_data)
        
        # Should have rolling average column
        assert 'daily_vaccinations_7d' in df_clean.columns
        
        # Rolling average should be numeric
        assert pd.api.types.is_numeric_dtype(df_clean['daily_vaccinations_7d'])
    
    def test_clean_vax_percentage_calculation(self, sample_data):
        """Test percentage vaccinated calculation"""
        df_clean = clean_vax(sample_data)
        
        # Should have percentage columns
        assert 'pct_vaccinated' in df_clean.columns
        assert 'pct_fully_vaccinated' in df_clean.columns
        
        # Percentages should be between 0 and 100
        valid_pct = df_clean['pct_vaccinated'].dropna()
        if len(valid_pct) > 0:
            assert (valid_pct >= 0).all() and (valid_pct <= 100).all()
    
    def test_clean_vax_missing_daily(self):
        """Test handling of missing daily_vaccinations"""
        # Create data with missing daily vaccinations
        df = pd.DataFrame({
            'location': ['TestCountry'] * 5,
            'date': pd.date_range('2024-01-01', periods=5),
            'total_vaccinations': [100, 200, 350, 500, 700],
            'people_vaccinated': [80, 150, 250, 350, 480],
            'people_fully_vaccinated': [50, 100, 180, 270, 370],
            'daily_vaccinations': [None, None, None, None, None],
            'population': [10000] * 5
        })
        
        df_clean = clean_vax(df)
        
        # Should fill daily vaccinations by differencing
        assert df_clean['daily_vaccinations'].notna().any()


class TestStorage:
    """Test database operations"""
    
    @pytest.fixture
    def sample_clean_data(self):
        """Create sample cleaned data"""
        return pd.DataFrame({
            'location': ['Country1'] * 5 + ['Country2'] * 5,
            'date': list(pd.date_range('2024-01-01', periods=5)) * 2,
            'total_vaccinations': [100, 200, 300, 400, 500] * 2,
            'people_vaccinated': [80, 160, 240, 320, 400] * 2,
            'people_fully_vaccinated': [50, 100, 150, 200, 250] * 2,
            'daily_vaccinations': [100, 100, 100, 100, 100] * 2,
            'daily_vaccinations_7d': [100, 100, 100, 100, 100] * 2,
            'pct_vaccinated': [1.0, 2.0, 3.0, 4.0, 5.0] * 2,
            'pct_fully_vaccinated': [0.5, 1.0, 1.5, 2.0, 2.5] * 2,
            'population': [10000] * 10
        })
    
    def test_save_df_to_db(self, sample_clean_data):
        """Test saving DataFrame to database"""
        save_df_to_db(sample_clean_data, table_name="test_vaccinations")
        
        # Check database file exists
        assert os.path.exists(DB_PATH), "Database file should exist"
    
    def test_get_latest_by_country(self, sample_clean_data):
        """Test querying latest stats by country"""
        # Save test data
        save_df_to_db(sample_clean_data)
        
        # Query latest
        latest = get_latest_by_country(limit=10)
        
        assert isinstance(latest, pd.DataFrame)
        assert len(latest) > 0
        
        # Should have unique countries
        assert latest['location'].nunique() == len(latest)
    
    def test_get_country_timeseries(self, sample_clean_data):
        """Test querying country time series"""
        # Save test data
        save_df_to_db(sample_clean_data)
        
        # Query time series
        ts = get_country_timeseries('Country1')
        
        assert isinstance(ts, pd.DataFrame)
        assert len(ts) > 0
        assert (ts['location'] == 'Country1').all()
        
        # Should be sorted by date
        assert ts['date'].is_monotonic_increasing


class TestForecasting:
    """Test time series forecasting"""
    
    @pytest.fixture
    def sample_country_data(self):
        """Create sample country time series data"""
        dates = pd.date_range('2024-01-01', periods=60)
        return pd.DataFrame({
            'location': ['TestCountry'] * 60,
            'date': dates,
            'daily_vaccinations': [1000 + i * 10 for i in range(60)]
        })
    
    def test_fit_prophet_for_country(self, sample_country_data):
        """Test Prophet model fitting and forecasting"""
        forecast = fit_prophet_for_country(
            sample_country_data,
            column='daily_vaccinations',
            periods=30
        )
        
        # Check forecast structure
        assert isinstance(forecast, pd.DataFrame)
        assert 'ds' in forecast.columns
        assert 'yhat' in forecast.columns
        assert 'yhat_lower' in forecast.columns
        assert 'yhat_upper' in forecast.columns
        
        # Check forecast length (historical + future)
        assert len(forecast) == 60 + 30
    
    def test_forecast_country_with_history(self, sample_country_data):
        """Test forecast with historical separation"""
        historical, future = forecast_country_with_history(
            sample_country_data,
            column='daily_vaccinations',
            periods=30
        )
        
        # Check both DataFrames are returned
        assert isinstance(historical, pd.DataFrame)
        assert isinstance(future, pd.DataFrame)
        
        # Historical should match original length
        assert len(historical) == 60
        
        # Future should match forecast period
        assert len(future) == 30
        
        # Historical should have actual values
        assert 'actual' in historical.columns


class TestIntegration:
    """Integration tests for complete pipeline"""
    
    def test_complete_pipeline(self):
        """Test complete ETL pipeline end-to-end"""
        # Load data
        df = load_data()
        assert len(df) > 0
        
        # Clean data
        df_clean = clean_vax(df)
        assert len(df_clean) > 0
        
        # Save to database
        save_df_to_db(df_clean)
        assert os.path.exists(DB_PATH)
        
        # Query data
        latest = get_latest_by_country(limit=5)
        assert len(latest) > 0
    
    def test_forecast_real_data(self):
        """Test forecasting with real data"""
        # Load and clean real data
        df = load_data()
        df_clean = clean_vax(df)
        
        # Get data for a country with sufficient history
        countries_with_data = df_clean.groupby('location').size()
        test_country = countries_with_data[countries_with_data > 30].index[0]
        
        country_data = df_clean[df_clean['location'] == test_country]
        
        # Generate forecast
        forecast = fit_prophet_for_country(
            country_data,
            column='daily_vaccinations',
            periods=7  # Short forecast for testing
        )
        
        assert len(forecast) > len(country_data)
        assert 'yhat' in forecast.columns


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (may be slow)"
    )


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
