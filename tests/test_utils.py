import pytest
import numpy as np
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import format_metric

class TestUtils:
    """Test utility functions"""
    
    def test_format_metric_basic(self):
        """Test basic formatting"""
        assert format_metric(1000000, 1e6, "M") == "1.00M"
        assert format_metric(1500, 1e3, "K", 1) == "1.5K"
        assert format_metric(0.5, 1, "%") == "0.50%"
    
    def test_format_metric_numpy_types(self):
        """Test formatting with numpy types"""
        assert format_metric(np.int64(1000000), 1e6, "M") == "1.00M"
        assert format_metric(np.float64(1000000.0), 1e6, "M") == "1.00M"
        assert format_metric(np.int32(1000), 1e3, "K") == "1.00K"
    
    def test_format_metric_edge_cases(self):
        """Test edge cases"""
        assert format_metric(None) == "N/A"
        assert format_metric(pd.NA) == "N/A"
        assert format_metric(np.nan) == "N/A"
        assert format_metric("invalid") == "N/A"
