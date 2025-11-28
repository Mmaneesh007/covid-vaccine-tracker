import pandas as pd
import numpy as np

def format_metric(x, divisor=1, suffix="", decimals=2):
    """
    Format a metric for display.
    
    Args:
        x: The value to format (int, float, or numpy number)
        divisor (float): Value to divide by (e.g., 1e6 for millions)
        suffix (str): Suffix to append (e.g., "M")
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted string or "N/A"
    """
    if pd.isna(x):
        return "N/A"
    
    # Robust check for numeric types including numpy types
    if isinstance(x, (int, float, np.number)):
        try:
            val = float(x) / divisor
            return f"{val:.{decimals}f}{suffix}"
        except (ValueError, TypeError):
            return "N/A"
            
    return "N/A"
