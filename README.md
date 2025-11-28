# COVID-19 Vaccine Tracker

A comprehensive vaccination tracking system with data ingestion, ETL pipeline, time series forecasting, and interactive dashboard.

## Features

- **Automated Data Ingestion**: Downloads latest vaccination data from Our World in Data
- **ETL Pipeline**: Cleans and transforms raw data with rolling averages and vaccination percentages
- **SQLite Database**: Efficient local storage for processed vaccination data
- **Interactive Dashboard**: Streamlit web app with country comparisons, time series plots, and global maps
- **Forecasting**: Prophet-based time series predictions for 30-day vaccination trends

## Data Source

This project uses the [Our World in Data COVID-19 Vaccination Dataset](https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations), which aggregates global vaccination statistics from official sources.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note**: Prophet may require compilation tools. On Windows, you may need to install Microsoft C++ Build Tools. If you encounter issues, consider using simpler forecasting methods.

## Usage

### Run Complete ETL Pipeline

Execute the full data download, cleaning, and database update:

```bash
python run_all.py
```

### Launch Dashboard

Start the Streamlit web application:

```bash
streamlit run app/streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Individual Modules

**Download data only:**
```bash
python src/etl.py
```

**Test forecasting for a country:**
```python
from src.etl import load_data
from src.clean import clean_vax
from src.forecast import fit_prophet_for_country

df = clean_vax(load_data())
forecast = fit_prophet_for_country(df[df.location=='India'], periods=30)
print(forecast.tail())
```

## Project Structure

```
COVID-19 vaccine tracker/
├── data/                    # Cached data and SQLite database
│   ├── vaccinations.csv     # Downloaded OWID data
│   └── vax_tracker.db       # SQLite database
├── src/                     # Source code modules
│   ├── etl.py              # Data download and loading
│   ├── clean.py            # Data cleaning and transformations
│   ├── storage.py          # Database operations
│   └── forecast.py         # Time series forecasting
├── app/                     # Streamlit application
│   └── streamlit_app.py    # Main dashboard
├── tests/                   # Unit and integration tests
│   └── test_etl.py         # ETL pipeline tests
├── run_all.py              # End-to-end automation script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
└── README.md              # This file
```

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

## Deployment

### Docker

Build and run the containerized application:

```bash
docker build -t vaccine-tracker .
docker run -p 8501:8501 vaccine-tracker
```

### Streamlit Cloud

1. Push this repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository and deploy

### Scheduled Updates

To automatically update data daily, set up a cron job:

```bash
# Run ETL pipeline daily at 2 AM
0 2 * * * cd /path/to/project && python run_all.py
```

## License

This project uses public data from Our World in Data. Please review their [data license](https://github.com/owid/covid-19-data/blob/master/LICENSE) for usage terms.

## Contributing

Contributions are welcome! Potential enhancements:
- Additional data sources (WHO, national health authorities)
- More sophisticated forecasting models (ARIMA, XGBoost)
- Enhanced dashboard features (date range filters, export capabilities)
- API endpoints for programmatic access

## Acknowledgments

- [Our World in Data](https://ourworldindata.org/) for providing comprehensive vaccination data
- [Facebook Prophet](https://facebook.github.io/prophet/) for time series forecasting capabilities
