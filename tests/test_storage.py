import os
import pandas as pd
import sqlalchemy as sa
import pytest

import src.storage as storage


@pytest.fixture(scope="function")
def patch_db(monkeypatch, tmp_path):
    """Patch the storage module to use a temporary SQLite database."""
    db_path = tmp_path / "test_vax_tracker.db"
    db_url = f"sqlite:///{db_path}"
    # Patch globals used by storage functions
    monkeypatch.setattr(storage, "DB_PATH", str(db_path), raising=False)
    monkeypatch.setattr(storage, "DB_URL", db_url, raising=False)
    yield str(db_path)


def make_sample_df():
    """Create a small sample dataset spanning two countries and two dates."""
    return pd.DataFrame(
        {
            "location": [
                "Testland",
                "Testland",
                "Mocktopia",
            ],
            "date": [
                "2023-01-01",
                "2023-01-02",
                "2023-01-01",
            ],
            "total_vaccinations": [1000, 1200, 500],
            "people_vaccinated": [800, 1000, 400],
            "people_fully_vaccinated": [600, 800, 300],
            "daily_vaccinations": [100, 200, 50],
            "daily_vaccinations_7d": [100, 150, 50],
            "pct_vaccinated": [8.0, 10.0, 4.0],
            "pct_fully_vaccinated": [6.0, 8.0, 3.0],
            "population": [10000, 10000, 8000],
        }
    )


def test_save_df_to_db_creates_file(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)  # default table: countries_vaccinations
    assert os.path.exists(patch_db)

    # Verify row exists for a sample country
    engine = sa.create_engine(storage.DB_URL)
    res = pd.read_sql_query(
        "SELECT COUNT(*) AS c FROM countries_vaccinations WHERE location='Testland'", engine
    )
    assert int(res.iloc[0]["c"]) == 2


def test_get_latest_by_country(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)

    latest = storage.get_latest_by_country(limit=10)
    assert isinstance(latest, pd.DataFrame)
    assert latest["location"].nunique() == len(latest)
    assert set(latest["location"]) == {"Testland", "Mocktopia"}


def test_get_country_latest(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)

    series = storage.get_country_latest("Testland")
    assert series is not None
    assert series["location"] == "Testland"
    assert series["total_vaccinations"] == 1200  # latest row for Testland


def test_get_country_timeseries(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)

    ts = storage.get_country_timeseries("Testland")
    assert isinstance(ts, pd.DataFrame)
    assert len(ts) == 2
    assert list(ts["date"].astype(str)) == ["2023-01-01", "2023-01-02"]


def test_get_all_countries(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)

    countries = storage.get_all_countries()
    assert isinstance(countries, list)
    assert set(countries) >= {"Testland", "Mocktopia"}


def test_nonexistent_country_returns_expected(patch_db):
    df = make_sample_df()
    storage.save_df_to_db(df)

    series = storage.get_country_latest("NowhereLand")
    assert series is None

    ts = storage.get_country_timeseries("NowhereLand")
    assert ts.empty
