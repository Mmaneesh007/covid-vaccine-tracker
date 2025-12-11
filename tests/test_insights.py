import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.insights import (
    compute_freshness_metrics,
    compute_completeness_metrics,
    detect_anomalies,
    get_data_quality_summary,
    format_quality_badge_text,
)


def make_df(days=10, countries=("A", "B")):
    base = pd.Timestamp("2024-01-01")
    rows = []
    for c in countries:
        for i in range(days):
            rows.append({
                "location": c,
                "date": base + pd.Timedelta(days=i),
                "total_vaccinations": 1000 + i,
                "people_vaccinated": 800 + i,
                "people_fully_vaccinated": 600 + i,
                "daily_vaccinations": 100 + (0 if i == 0 else i),
            })
    return pd.DataFrame(rows)


def test_freshness_metrics_basic():
    df = make_df(days=5)
    now = pd.Timestamp("2024-01-07T00:00:00Z")
    m = compute_freshness_metrics(df, now=now)
    assert m["last_updated"] == pd.Timestamp("2024-01-05")
    assert m["staleness_label"] in {"fresh", "ok", "stale"}
    assert m["total_countries"] == 2
    assert m["countries_missing_recent"] == 0


def test_completeness_metrics_missingness():
    df = make_df(days=3)
    df.loc[0, "people_vaccinated"] = np.nan
    stats = compute_completeness_metrics(df)
    assert "people_vaccinated" in stats["missing_rate"]
    assert 0.0 <= stats["missing_rate"]["people_vaccinated"] <= 1.0


def test_detect_anomalies_zscore():
    df = make_df(days=30)
    # Inject a spike
    df.loc[(df["location"] == "A") & (df["date"] == pd.Timestamp("2024-01-20")), "daily_vaccinations"] = 10000
    res = detect_anomalies(df, window=7, z_thresh=3.0)
    assert res["total_anomalies"] >= 1
    assert isinstance(res["examples"], list)


def test_quality_summary_and_badge():
    df = make_df(days=10)
    summary = get_data_quality_summary(df)
    assert summary["freshness"]["total_countries"] == 2
    badge = format_quality_badge_text(summary)
    assert isinstance(badge, str)
    assert "Data:" in badge
