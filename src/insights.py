import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_country_insight(df, country):
    """
    Generate AI-powered natural language insights for a specific country.
    
    Args:
        df (pd.DataFrame): Full vaccination dataframe
        country (str): Country name
    
    Returns:
        str: Natural language summary of trends and projections
    """
    # Filter data for the country
    country_data = df[df['location'] == country].sort_values('date')
    
    if len(country_data) == 0:
        return f"No data available for {country}."
    
    # Get latest data
    latest = country_data.iloc[-1]
    latest_date = latest['date']
    
    # Calculate trends
    insights = []
    
    # 1. Daily vaccination rate
    daily_vax = latest.get('daily_vaccinations_7d', 0)
    if pd.notna(daily_vax) and daily_vax > 0:
        if daily_vax >= 1_000_000:
            insights.append(f"**{country}** is vaccinating **{daily_vax/1_000_000:.1f}M** people daily")
        elif daily_vax >= 1_000:
            insights.append(f"**{country}** is vaccinating **{daily_vax/1_000:.0f}K** people daily")
        else:
            insights.append(f"**{country}** is vaccinating **{daily_vax:.0f}** people daily")
    
    # 2. Week-over-week change
    if len(country_data) >= 7:
        week_ago_data = country_data[country_data['date'] == latest_date - timedelta(days=7)]
        if not week_ago_data.empty:
            week_ago_vax = week_ago_data.iloc[0].get('daily_vaccinations_7d', 0)
            if pd.notna(week_ago_vax) and week_ago_vax > 0 and pd.notna(daily_vax):
                change_pct = ((daily_vax - week_ago_vax) / week_ago_vax) * 100
                if abs(change_pct) > 5:  # Only mention if significant
                    direction = "up" if change_pct > 0 else "down"
                    insights.append(f"{direction} **{abs(change_pct):.0f}%** from last week")
    
    # 3. Current coverage
    pct_vaccinated = latest.get('pct_vaccinated', 0)
    if pd.notna(pct_vaccinated):
        insights.append(f"Currently at **{pct_vaccinated:.1f}%** coverage")
    
    # 4. Project to target (70% is common benchmark)
    target = 70.0
    if pd.notna(pct_vaccinated) and pd.notna(daily_vax) and daily_vax > 0:
        population = latest.get('population', 0)
        if pd.notna(population) and population > 0:
            people_vaccinated = (pct_vaccinated / 100) * population
            people_needed = (target / 100) * population - people_vaccinated
            
            if people_needed > 0:
                days_to_target = people_needed / daily_vax
                if days_to_target <= 365:  # Only show if within a year
                    target_date = latest_date + timedelta(days=days_to_target)
                    insights.append(f"Projected to reach **{target:.0f}%** by **{target_date.strftime('%b %Y')}**")
    
    # Combine all insights
    if insights:
        return ". ".join(insights) + "."
    else:
        return f"Tracking vaccination progress for {country}."


def generate_global_insight(df):
    """
    Generate a global summary insight across all countries.
    
    Args:
        df (pd.DataFrame): Full vaccination dataframe
    
    Returns:
        str: Natural language global summary
    """
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]
    
    # Total vaccinations globally
    total_vax = latest_data['total_vaccinations'].sum()
    total_pop = latest_data['population'].sum()
    
    insights = []
    
    if pd.notna(total_vax) and total_vax > 0:
        insights.append(f"**{total_vax/1e9:.1f}B** doses administered globally")
    
    if pd.notna(total_pop) and total_pop > 0:
        global_coverage = (latest_data['people_vaccinated'].sum() / total_pop) * 100
        if pd.notna(global_coverage):
            insights.append(f"**{global_coverage:.1f}%** of the world has received at least one dose")
    
    # Top performer
    top_country = latest_data.nlargest(1, 'pct_vaccinated')
    if not top_country.empty:
        leader = top_country.iloc[0]
        insights.append(f"**{leader['location']}** leads at **{leader['pct_vaccinated']:.1f}%** coverage")
    
    if insights:
        return ". ".join(insights) + "."
    else:
        return "Global vaccination data is being tracked."
