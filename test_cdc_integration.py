"""
Test script for CDC API integration
Run this to verify the multi-source data integration works correctly.
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.data_sources import get_data_source_manager, DATA_SOURCE_OWID, DATA_SOURCE_CDC
from src.etl import load_data
from src.clean import clean_vax
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_data_sources():
    """Test individual data sources"""
    print("=" * 70)
    print("Testing Data Sources")
    print("=" * 70)
    
    manager = get_data_source_manager()
    
    # Test OWID
    print("\n[TEST 1] Testing OWID Source...")
    try:
        owid_source = manager.sources[DATA_SOURCE_OWID]
        df_owid = owid_source.fetch()
        print(f"✓ OWID: Successfully fetched {len(df_owid):,} records")
        print(f"  Columns: {df_owid.columns.tolist()[:5]}...")
        if 'location' in df_owid.columns:
            print(f"  Countries: {df_owid['location'].nunique()}")
    except Exception as e:
        print(f"✗ OWID: Failed - {e}")
    
    # Test CDC
    print("\n[TEST 2] Testing CDC Source...")
    try:
        cdc_source = manager.sources[DATA_SOURCE_CDC]
        df_cdc = cdc_source.fetch()
        print(f"✓ CDC: Successfully fetched {len(df_cdc):,} records")
        print(f"  Columns: {df_cdc.columns.tolist()[:5]}...")
        if 'location' in df_cdc.columns:
            print(f"  Locations: {df_cdc['location'].unique()}")
    except Exception as e:
        print(f"✗ CDC: Failed - {e}")
        print("  Note: CDC may not have global data, only US state-level")

def test_data_source_manager():
    """Test the data source manager with fallback"""
    print("\n" + "=" * 70)
    print("Testing Data Source Manager (with fallback)")
    print("=" * 70)
    
    manager = get_data_source_manager()
    
    # Test getting data with fallback
    print("\n[TEST 3] Getting data with automatic fallback...")
    try:
        result = manager.get_data_with_source_info()
        df = result['data']
        print(f"✓ Successfully fetched {len(df):,} records")
        print(f"  Source used: {result['source']}")
        print(f"  Fallback used: {result['fallback_used']}")
        print(f"  Timestamp: {result['timestamp']}")
        if 'data_source' in df.columns:
            sources = df['data_source'].value_counts()
            print(f"  Data sources in dataset: {sources.to_dict()}")
    except Exception as e:
        print(f"✗ Failed: {e}")

def test_etl_integration():
    """Test ETL integration with multi-source"""
    print("\n" + "=" * 70)
    print("Testing ETL Integration")
    print("=" * 70)
    
    print("\n[TEST 4] Loading data via ETL (multi-source enabled)...")
    try:
        df = load_data(use_multi_source=True)
        print(f"✓ Successfully loaded {len(df):,} records")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        if 'data_source' in df.columns:
            sources = df['data_source'].value_counts()
            print(f"  Data sources: {sources.to_dict()}")
        
        # Test cleaning
        print("\n[TEST 5] Cleaning data...")
        df_clean = clean_vax(df)
        print(f"✓ Cleaned {len(df_clean):,} records")
        print(f"  Columns: {df_clean.columns.tolist()}")
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()

def test_available_sources():
    """Test checking available sources"""
    print("\n" + "=" * 70)
    print("Testing Source Availability Check")
    print("=" * 70)
    
    manager = get_data_source_manager()
    available = manager.get_available_sources()
    print(f"\nAvailable sources: {available}")
    
    for source_name in available:
        source = manager.sources[source_name]
        print(f"  - {source_name}: {source.name} (cache TTL: {source.cache_ttl}s)")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CDC API Integration Test Suite")
    print("=" * 70)
    
    try:
        test_data_sources()
        test_data_source_manager()
        test_etl_integration()
        test_available_sources()
        
        print("\n" + "=" * 70)
        print("✓ All tests completed!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Check the results above")
        print("2. If CDC fails, it's OK - CDC primarily has US data")
        print("3. OWID should work as primary source")
        print("4. The system will automatically fallback if needed")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

