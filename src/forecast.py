# src/forecast.py
from prophet import Prophet
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

def fit_prophet_for_country(df_country, column="daily_vaccinations", periods=30):
    """
    Train a Prophet model for a country's vaccination time series and generate forecasts.
    
    Args:
        df_country (pd.DataFrame): DataFrame with 'date' and vaccination column for one country
        column (str): Column name to forecast (e.g., 'daily_vaccinations', 'people_vaccinated')
        periods (int): Number of days to forecast into the future
    
    Returns:
        pd.DataFrame: Forecast with columns: ds (date), yhat (prediction), 
                     yhat_lower, yhat_upper (confidence bounds)
    """
    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    ts = df_country[["date", column]].rename(columns={"date": "ds", column: "y"})
    
    # Fill NaN values with 0 (Prophet doesn't handle NaN well)
    ts = ts.fillna(0)
    
    # Remove any duplicate dates
    ts = ts.drop_duplicates(subset=["ds"])
    
    # Initialize and fit Prophet model
    # Disable daily seasonality for vaccination data (weekly patterns more relevant)
    m = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05  # Controls flexibility (lower = less flexible)
    )
    
    m.fit(ts)
    
    # Create future dataframe for predictions
    future = m.make_future_dataframe(periods=periods)
    
    # Generate predictions
    forecast = m.predict(future)
    
    # Return relevant columns
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

def forecast_country_with_history(df_country, column="daily_vaccinations", periods=30):
    """
    Generate forecast and combine with historical data.
    
    Args:
        df_country (pd.DataFrame): Historical data
        column (str): Column to forecast
        periods (int): Days to forecast
    
    Returns:
        tuple: (historical_df, forecast_df)
    """
    # Get forecast
    forecast = fit_prophet_for_country(df_country, column, periods)
    
    # Split historical and future
    max_date = df_country["date"].max()
    historical = forecast[forecast["ds"] <= max_date].copy()
    future = forecast[forecast["ds"] > max_date].copy()
    
    # Merge historical predictions with actuals
    historical = historical.merge(
        df_country[["date", column]].rename(columns={"date": "ds", column: "actual"}),
        on="ds",
        how="left"
    )
    
    return historical, future

if __name__ == "__main__":
    from etl import load_data
    from clean import clean_vax
    
    print("Loading data...")
    df = load_data()
    df_clean = clean_vax(df)
    
    # Test forecasting for India
    country = "India"
    print(f"\nGenerating forecast for {country}...")
    country_data = df_clean[df_clean["location"] == country].copy()
    
    if len(country_data) > 0:
        forecast = fit_prophet_for_country(country_data, "daily_vaccinations", periods=30)
        print(f"\nForecast (last 5 days):")
        print(forecast.tail())
        
        print(f"\nForecast summary:")
        print(f"  Date range: {forecast['ds'].min()} to {forecast['ds'].max()}")
        print(f"  Mean prediction: {forecast['yhat'].mean():,.0f} daily vaccinations")
    else:
        print(f"No data found for {country}")
