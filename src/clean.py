# src/clean.py
import pandas as pd

def clean_vax(df):
    """
    Clean and transform vaccination data.
    
    Performs the following transformations:
    - Filters to essential columns
    - Ensures numeric types for vaccination metrics
    - Fills missing daily_vaccinations by differencing total_vaccinations
    - Computes 7-day rolling averages per country
    - Calculates percentage of population vaccinated
    
    Args:
        df (pd.DataFrame): Raw vaccination data
    
    Returns:
        pd.DataFrame: Cleaned and transformed vaccination data
    """
    # Define required columns
    cols = [
        "location", "date", "total_vaccinations", "people_vaccinated",
        "people_fully_vaccinated", "daily_vaccinations", "population",
        "new_cases_smoothed", "new_deaths_smoothed", 
        "new_cases_smoothed_per_million", "new_deaths_smoothed_per_million"
    ]
    
    # Add missing columns as NA if they don't exist
    for c in cols:
        if c not in df.columns:
            df[c] = pd.NA
    
    # Filter to required columns and copy to avoid SettingWithCopyWarning
    df = df[cols].copy()
    
    # Sort by location and date for proper time series operations
    df = df.sort_values(["location", "date"])
    
    # Convert vaccination and case/death columns to numeric
    numeric_cols = [
        "total_vaccinations", "people_vaccinated", 
        "people_fully_vaccinated", "daily_vaccinations",
        "new_cases_smoothed", "new_deaths_smoothed",
        "new_cases_smoothed_per_million", "new_deaths_smoothed_per_million"
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    
    # Ensure population is numeric
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    
    def fill_group(g):
        """Process each country group separately"""
        # Fill missing daily_vaccinations by differencing total_vaccinations
        if g["daily_vaccinations"].isna().any():
            daily_diff = g["total_vaccinations"].diff().fillna(0)
            # Only use positive differences (sometimes data corrections cause negatives)
            daily_diff = daily_diff.clip(lower=0)
            g["daily_vaccinations"] = g["daily_vaccinations"].fillna(daily_diff)
        
        # Ensure daily_vaccinations is non-negative
        g["daily_vaccinations"] = g["daily_vaccinations"].clip(lower=0)
        
        # Compute 7-day rolling average
        g["daily_vaccinations_7d"] = g["daily_vaccinations"].rolling(
            window=7, min_periods=1
        ).mean()
        
        # Calculate percentage of population vaccinated
        if g["population"].notna().any():
            pop = g["population"].ffill().bfill().iloc[0]
            g["pct_vaccinated"] = (g["people_vaccinated"] / pop) * 100
            g["pct_fully_vaccinated"] = (g["people_fully_vaccinated"] / pop) * 100
        else:
            g["pct_vaccinated"] = pd.NA
            g["pct_fully_vaccinated"] = pd.NA
        
        return g
    
    # Apply transformations per country
    df = df.groupby("location", group_keys=False).apply(fill_group)
    
    print(f"Cleaned data: {len(df):,} records across {df['location'].nunique()} locations")
    
    return df

if __name__ == "__main__":
    from etl import load_data
    df = load_data()
    df_clean = clean_vax(df)
    print("\nCleaned data info:")
    print(df_clean.info())
    print("\nSample cleaned data:")
    print(df_clean.head(10))
