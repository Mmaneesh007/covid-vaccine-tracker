import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go

DB_PATH = "data/vax_tracker.db"

def test_impact_analysis():
    print("Testing Impact Analysis logic...")
    
    # Simulate the app logic
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM countries_vaccinations WHERE location = 'India'", engine, parse_dates=["date"])
    
    print(f"Total rows: {len(df)}")
    
    country_impact_data = df.copy()
    
    # Ensure column exists
    if 'new_deaths_smoothed_per_million' not in country_impact_data.columns:
        country_impact_data['new_deaths_smoothed_per_million'] = pd.NA
    
    # Check if data is missing (all NaNs) and try to calculate
    if country_impact_data['new_deaths_smoothed_per_million'].isna().all():
        if 'new_deaths_smoothed' in country_impact_data.columns and 'population' in country_impact_data.columns:
            country_impact_data['new_deaths_smoothed_per_million'] = (
                country_impact_data['new_deaths_smoothed'] / country_impact_data['population'] * 1_000_000
            )
            print("Calculated deaths per million from raw data.")
    
    # Filter to valid data
    required_cols = ['pct_vaccinated', 'new_deaths_smoothed_per_million']
    valid_data = country_impact_data.dropna(subset=required_cols)
    
    print(f"Rows with both metrics: {len(valid_data)}")
    
    if len(valid_data) == 0:
        print("ERROR: No overlapping data!")
    else:
        print("SUCCESS: Chart can be created!")
        
        # Try to create the figure
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=valid_data['date'],
                y=valid_data['pct_vaccinated'],
                name='Vaccination Rate (%)',
                mode='lines',
                line=dict(color='#667eea', width=3),
                yaxis='y1'
            ))
            fig.add_trace(go.Scatter(
                x=valid_data['date'],
                y=valid_data['new_deaths_smoothed_per_million'],
                name='Daily Deaths (per million)',
                mode='lines',
                line=dict(color='#e3342f', width=2),
                yaxis='y2',
                opacity=0.8
            ))
            
            print("Figure created successfully!")
            print(f"Date range: {valid_data['date'].min()} to {valid_data['date'].max()}")
        except Exception as e:
            print(f"Figure creation failed: {e}")

if __name__ == "__main__":
    test_impact_analysis()
