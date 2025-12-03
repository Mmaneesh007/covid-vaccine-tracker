"""
Forecasting endpoints
Provides ML-based vaccination trend predictions
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.api.models import ForecastResponse, ForecastPoint
from src.storage import get_country_timeseries
from src.forecast import fit_prophet_for_country
from app.api.cache import cached

router = APIRouter()


@router.get("/forecast/{country_name}", response_model=ForecastResponse)
@cached(ttl=7200)  # Cache for 2 hours (forecasts don't change frequently)
async def get_forecast(
    country_name: str = Path(..., description="Name of the country to forecast"),
    days: int = Query(30, description="Number of days to forecast into the future", ge=1, le=180),
    metric: str = Query("total_vaccinations", description="Metric to forecast")
):
    """
    Generate ML-based forecast for vaccination trends
    
    Uses Facebook Prophet to predict future vaccination numbers based on historical data.
    
    **Parameters:**
    - **country_name**: Country to generate forecast for
    - **days**: Number of days to predict (1-180)
    - **metric**: Which metric to forecast (default: total_vaccinations)
    
    **Returns:**
    - Forecasted values with confidence intervals (upper/lower bounds)
    """
    try:
        # Get historical data
        df = get_country_timeseries(country_name)
        
        if df is None or df.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No historical data available for '{country_name}'"
            )
        
        # Check if metric exists
        if metric not in df.columns:
            available_metrics = [col for col in df.columns if col != 'date']
            raise HTTPException(
                status_code=400,
                detail=f"Metric '{metric}' not found. Available: {', '.join(available_metrics)}"
            )
        
        # Generate forecast
        forecast_df = fit_prophet_for_country(df, column=metric, periods=days)
        
        if forecast_df is None or forecast_df.empty:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate forecast for '{country_name}'"
            )
        
        # Convert forecast to response format
        forecast_points = []
        for _, row in forecast_df.iterrows():
            forecast_points.append(
                ForecastPoint(
                    date=row['ds'].strftime('%Y-%m-%d'),
                    predicted_value=float(row['yhat']),
                    lower_bound=float(row['yhat_lower']) if 'yhat_lower' in row else None,
                    upper_bound=float(row['yhat_upper']) if 'yhat_upper' in row else None
                )
            )
        
        return ForecastResponse(
            country=country_name,
            metric=metric,
            forecast_days=days,
            forecast=forecast_points
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast generation failed: {str(e)}"
        )
