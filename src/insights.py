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


# ----------------------------
# Data quality & freshness utils
# ----------------------------
def compute_freshness_metrics(df: pd.DataFrame, now: pd.Timestamp | None = None):
    """
    Compute dataset freshness based on the most recent date in the DataFrame.

    Returns dict with:
      - last_updated (Timestamp)
      - staleness_hours (float)
      - staleness_label (fresh|ok|stale|unknown)
      - countries_missing_recent (int)
      - total_countries (int)
    """
    if df.empty or 'date' not in df.columns:
        return {
            'last_updated': None,
            'staleness_hours': None,
            'staleness_label': 'unknown',
            'countries_missing_recent': 0,
            'total_countries': 0,
        }

    last_updated = pd.to_datetime(df['date'], errors='coerce').max()
    # Normalize tz handling: operate on tz-naive UTC for consistent arithmetic
    last_updated = pd.Timestamp(last_updated)
    if last_updated.tzinfo is not None:
        last_updated = last_updated.tz_convert('UTC').tz_localize(None)

    if now is None:
        now = pd.Timestamp.utcnow()
    now = pd.Timestamp(now)
    if now.tzinfo is not None:
        now = now.tz_convert('UTC').tz_localize(None)

    staleness_hours = float((now - last_updated).total_seconds() / 3600.0)

    if staleness_hours <= 24:
        staleness_label = 'fresh'
    elif staleness_hours <= 72:
        staleness_label = 'ok'
    else:
        staleness_label = 'stale'

    total_countries = int(df['location'].nunique()) if 'location' in df.columns else 0
    if total_countries == 0:
        countries_missing_recent = 0
    else:
        latest_mask = pd.to_datetime(df['date'], errors='coerce') == last_updated
        recent_countries = set(df.loc[latest_mask, 'location'].unique()) if 'location' in df.columns else set()
        all_countries = set(df['location'].unique()) if 'location' in df.columns else set()
        countries_missing_recent = len(all_countries - recent_countries)

    return {
        'last_updated': last_updated,
        'staleness_hours': staleness_hours,
        'staleness_label': staleness_label,
        'countries_missing_recent': countries_missing_recent,
        'total_countries': total_countries,
    }


def compute_completeness_metrics(df: pd.DataFrame):
    """
    Compute missingness ratios for key columns.

    Returns dict with:
      - missing_rate: dict[column -> float(0..1)]
      - rows: total rows evaluated
    """
    if df.empty:
        return {'missing_rate': {}, 'rows': 0}

    key_cols = [
        'total_vaccinations',
        'people_vaccinated',
        'people_fully_vaccinated',
        'daily_vaccinations',
    ]
    present_cols = [c for c in key_cols if c in df.columns]
    rows = len(df)
    missing_rate = {}
    for c in present_cols:
        missing = int(df[c].isna().sum())
        missing_rate[c] = missing / rows if rows else 0.0

    return {'missing_rate': missing_rate, 'rows': rows}


def detect_anomalies(df: pd.DataFrame, window: int = 7, z_thresh: float = 3.5):
    """
    Simple anomaly detection on daily_vaccinations using rolling z-score per country.

    Returns dict with:
      - total_anomalies
      - anomalies_last_7d
      - examples: list of dicts {location, date, value, z}
    """
    if df.empty or 'daily_vaccinations' not in df.columns or 'location' not in df.columns:
        return {'total_anomalies': 0, 'anomalies_last_7d': 0, 'examples': []}

    dfx = df[['location', 'date', 'daily_vaccinations']].dropna().copy()
    dfx['date'] = pd.to_datetime(dfx['date'], errors='coerce')
    dfx = dfx.sort_values(['location', 'date'])

    results = []
    for loc, g in dfx.groupby('location'):
        g = g.copy()
        roll = g['daily_vaccinations'].rolling(window, min_periods=max(3, window // 2))
        # Use prior-window statistics to avoid current point influencing its own z-score
        g['roll_mean'] = roll.mean().shift(1)
        g['roll_std'] = roll.std(ddof=0).shift(1)
        g['z'] = (g['daily_vaccinations'] - g['roll_mean']) / g['roll_std'].replace(0, np.nan)
        g['is_anomaly'] = g['z'].abs() > z_thresh
        if g['is_anomaly'].any():
            flagged = g[g['is_anomaly']]
            for _, row in flagged.iterrows():
                results.append({
                    'location': loc,
                    'date': row['date'],
                    'value': float(row['daily_vaccinations']),
                    'z': float(row['z']) if pd.notna(row['z']) else np.inf,
                })

    total = len(results)
    if not dfx.empty:
        last7_cut = dfx['date'].max() - pd.Timedelta(days=7)
        anomalies_last_7d = sum(1 for r in results if r['date'] >= last7_cut)
    else:
        anomalies_last_7d = 0
    examples = sorted(results, key=lambda r: abs(r['z']), reverse=True)[:5]

    return {
        'total_anomalies': total,
        'anomalies_last_7d': anomalies_last_7d,
        'examples': examples,
    }


def get_data_quality_summary(df: pd.DataFrame):
    """
    Aggregate freshness, completeness, and anomalies into a single summary.
    Returns a dict suitable for UI.
    """
    fresh = compute_freshness_metrics(df)
    comp = compute_completeness_metrics(df)
    anom = detect_anomalies(df)

    status = 'good'
    if fresh.get('staleness_label') == 'stale' or anom.get('anomalies_last_7d', 0) > 0:
        status = 'warning'
    avg_missing = 0.0
    if comp['missing_rate']:
        avg_missing = float(np.mean(list(comp['missing_rate'].values())))
    if avg_missing > 0.2 and fresh.get('staleness_label') != 'fresh':
        status = 'critical'

    return {
        'freshness': fresh,
        'completeness': comp,
        'anomalies': anom,
        'status': status,
    }


def format_quality_badge_text(summary: dict) -> str:
    """Create a compact badge text for Streamlit display or logs."""
    fresh = summary.get('freshness', {})
    comp = summary.get('completeness', {})
    anom = summary.get('anomalies', {})

    label_map = {'fresh': 'Fresh', 'ok': 'OK', 'stale': 'Stale', 'unknown': 'Unknown'}
    staleness = label_map.get(fresh.get('staleness_label'), 'Unknown')
    rates = list(comp.get('missing_rate', {}).values())
    avg_missing = float(np.mean(rates) * 100.0) if rates else 0.0
    anomalies = int(anom.get('anomalies_last_7d', 0))

    return f"Data: {staleness} • Missing: {avg_missing:.1f}% • Anomalies (7d): {anomalies}"

