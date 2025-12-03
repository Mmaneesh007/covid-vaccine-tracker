"""
Vaccination data endpoints
Provides access to country-level vaccination statistics
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.api.models import VaccinationStats, CountryListResponse, TimeSeriesData, TimeSeriesPoint
from src.storage import get_all_countries, get_latest_by_country, get_country_timeseries, get_country_latest
from app.api.cache import cached

router = APIRouter()


@router.get("/global", response_model=VaccinationStats)
@cached(ttl=3600)
async def get_global_stats():
    """
    Get global vaccination statistics
    """
    try:
        # For now, we'll aggregate data from all countries
        # In a real app, this might come from a pre-calculated source
        countries = get_all_countries()
        total_vax = 0
        people_vax = 0
        fully_vax = 0
        
        for country in countries:
            data = get_country_latest(country)
            if data is not None and not data.empty:
                stats = data.to_dict()
                total_vax += int(stats.get('total_vaccinations', 0) or 0)
                people_vax += int(stats.get('people_vaccinated', 0) or 0)
                fully_vax += int(stats.get('people_fully_vaccinated', 0) or 0)
        
        return VaccinationStats(
            country="Global",
            total_vaccinations=total_vax,
            people_vaccinated=people_vax,
            people_fully_vaccinated=fully_vax,
            daily_vaccinations=None,
            total_vaccinations_per_hundred=None,
            people_vaccinated_per_hundred=None,
            people_fully_vaccinated_per_hundred=None,
            date=datetime.now().strftime("%Y-%m-%d")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch global stats: {str(e)}")


@router.get("/top", response_model=List[VaccinationStats])
@cached(ttl=3600)
async def get_top_countries(
    limit: int = Query(10, description="Number of countries to return", ge=1, le=50),
    metric: str = Query("total_vaccinations", description="Metric to sort by")
):
    """
    Get top performing countries based on vaccination metrics
    """
    try:
        countries = get_all_countries()
        all_stats = []
        
        for country in countries:
            data = get_country_latest(country)
            if data is not None and not data.empty:
                stats = data.to_dict()
                val = stats.get(metric, 0)
                if val:
                    all_stats.append({
                        "country": country,
                        "value": float(val),
                        "stats": stats
                    })
        
        # Sort by value descending
        all_stats.sort(key=lambda x: x["value"], reverse=True)
        
        # Take top N
        top_stats = all_stats[:limit]
        
        result = []
        for item in top_stats:
            stats = item["stats"]
            result.append(VaccinationStats(
                country=item["country"],
                total_vaccinations=int(stats.get('total_vaccinations', 0)) if stats.get('total_vaccinations') else None,
                people_vaccinated=int(stats.get('people_vaccinated', 0)) if stats.get('people_vaccinated') else None,
                people_fully_vaccinated=int(stats.get('people_fully_vaccinated', 0)) if stats.get('people_fully_vaccinated') else None,
                daily_vaccinations=int(stats.get('daily_vaccinations', 0)) if stats.get('daily_vaccinations') else None,
                total_vaccinations_per_hundred=float(stats.get('total_vaccinations_per_hundred', 0)) if stats.get('total_vaccinations_per_hundred') else None,
                people_vaccinated_per_hundred=float(stats.get('people_vaccinated_per_hundred', 0)) if stats.get('people_vaccinated_per_hundred') else None,
                people_fully_vaccinated_per_hundred=float(stats.get('people_fully_vaccinated_per_hundred', 0)) if stats.get('people_fully_vaccinated_per_hundred') else None,
                date=str(stats.get('date', ''))
            ))
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top countries: {str(e)}")


@router.get("/countries", response_model=CountryListResponse)
@cached(ttl=3600)  # Cache for 1 hour
async def list_countries():
    """
    Get list of all available countries
    
    Returns a list of country names for which vaccination data is available.
    """
    try:
        countries = get_all_countries()
        return {
            "countries": sorted(countries),
            "total_count": len(countries)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch countries: {str(e)}")


@router.get("/countries/{country_name}", response_model=VaccinationStats)
@cached(ttl=1800)  # Cache for 30 minutes
async def get_country_stats(
    country_name: str = Path(..., description="Name of the country (e.g., 'India', 'United States')")
):
    """
    Get latest vaccination statistics for a specific country
    
    Returns the most recent vaccination data including:
    - Total vaccinations administered
    - Number of people vaccinated (at least one dose)
    - Number of fully vaccinated people
    - Daily vaccination rate
    - Per capita metrics
    """
    try:
        data = get_country_latest(country_name)
        
        if data is None or data.empty:
            raise HTTPException(status_code=404, detail=f"Country '{country_name}' not found")
        
        # Convert to dict (data is a Series)
        stats = data.to_dict()
        
        return VaccinationStats(
            country=country_name,
            total_vaccinations=int(stats.get('total_vaccinations', 0)) if stats.get('total_vaccinations') else None,
            people_vaccinated=int(stats.get('people_vaccinated', 0)) if stats.get('people_vaccinated') else None,
            people_fully_vaccinated=int(stats.get('people_fully_vaccinated', 0)) if stats.get('people_fully_vaccinated') else None,
            daily_vaccinations=int(stats.get('daily_vaccinations', 0)) if stats.get('daily_vaccinations') else None,
            total_vaccinations_per_hundred=float(stats.get('total_vaccinations_per_hundred', 0)) if stats.get('total_vaccinations_per_hundred') else None,
            people_vaccinated_per_hundred=float(stats.get('people_vaccinated_per_hundred', 0)) if stats.get('people_vaccinated_per_hundred') else None,
            people_fully_vaccinated_per_hundred=float(stats.get('people_fully_vaccinated_per_hundred', 0)) if stats.get('people_fully_vaccinated_per_hundred') else None,
            date=str(stats.get('date', ''))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")


@router.get("/countries/{country_name}/timeseries", response_model=TimeSeriesData)
async def get_country_timeseries_data(
    country_name: str = Path(..., description="Name of the country"),
    metric: str = Query("total_vaccinations", description="Metric to retrieve (e.g., 'total_vaccinations', 'people_vaccinated')"),
    limit: Optional[int] = Query(None, description="Limit number of recent data points", ge=1, le=1000)
):
    """
    Get historical time series data for a country
    
    Returns daily vaccination data over time for the specified metric.
    
    Available metrics:
    - total_vaccinations
    - people_vaccinated
    - people_fully_vaccinated
    - daily_vaccinations
    - total_vaccinations_per_hundred
    - people_vaccinated_per_hundred
    - people_fully_vaccinated_per_hundred
    """
    try:
        df = get_country_timeseries(country_name)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No time series data for '{country_name}'")
        
        # Check if metric exists
        if metric not in df.columns:
            available_metrics = [col for col in df.columns if col != 'date']
            raise HTTPException(
                status_code=400, 
                detail=f"Metric '{metric}' not found. Available metrics: {', '.join(available_metrics)}"
            )
        
        # Apply limit if specified
        if limit:
            df = df.tail(limit)
        
        # Convert to list of TimeSeriesPoint
        data_points = []
        for _, row in df.iterrows():
            data_points.append(
                TimeSeriesPoint(
                    date=str(row['date']),
                    value=float(row[metric]) if row[metric] and not pd.isna(row[metric]) else None
                )
            )
        
        return TimeSeriesData(
            country=country_name,
            metric=metric,
            data=data_points
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch time series: {str(e)}")


# Import pandas for isna check
import pandas as pd
