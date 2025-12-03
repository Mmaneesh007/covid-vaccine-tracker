# %% [markdown]
# # 📊 COVID-19 Vaccine Data Analysis
# 
# This notebook demonstrates how to use the **COVID-19 Vaccine Tracker API** to perform data analysis and visualization.
# 
# **Prerequisites:**
# 1. Ensure the API is running: `.\app\experimental\start_api.ps1`
# 2. Install dependencies: `pip install pandas matplotlib requests`

# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
plt.style.use('ggplot')

# %% [markdown]
# ## 1. Fetching Global Data
# Let's start by getting the list of all available countries.

# %%
response = requests.get(f"{BASE_URL}/countries")
countries = response.json()['countries']
print(f"Total Countries Available: {len(countries)}")
print(f"Sample: {countries[:10]}")

# %% [markdown]
# ## 2. Comparing Vaccination Campaigns
# We will compare the vaccination progress of **India**, **USA**, and **United Kingdom**.

# %%
target_countries = ["India", "United States", "United Kingdom"]
data_list = []

for country in target_countries:
    resp = requests.get(f"{BASE_URL}/countries/{country}")
    if resp.status_code == 200:
        data_list.append(resp.json())

df_comparison = pd.DataFrame(data_list)
df_comparison = df_comparison[['country', 'total_vaccinations_per_hundred', 'people_fully_vaccinated_per_hundred']]
df_comparison.set_index('country', inplace=True)

print(df_comparison)

# %%
# Plotting the comparison
ax = df_comparison.plot(kind='bar', figsize=(10, 6), rot=0)
plt.title("Vaccination Coverage Comparison")
plt.ylabel("Per 100 People")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Analyzing Forecast Trends
# Let's look at the predicted vaccination trend for **India** over the next 30 days.

# %%
country = "India"
days = 30
resp = requests.get(f"{BASE_URL}/forecast/{country}?days={days}")
forecast_data = resp.json()['forecast']

df_forecast = pd.DataFrame(forecast_data)
df_forecast['ds'] = pd.to_datetime(df_forecast['ds'])

print(df_forecast.head())

# %%
plt.figure(figsize=(12, 6))
plt.plot(df_forecast['ds'], df_forecast['yhat'], label='Predicted Doses', color='blue', linewidth=2)
plt.fill_between(df_forecast['ds'], df_forecast['yhat_lower'], df_forecast['yhat_upper'], color='blue', alpha=0.1, label='Confidence Interval')
plt.title(f"30-Day Vaccination Forecast for {country}")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# ## 4. AI Sentiment Analysis
# Let's ask the chatbot a few questions and see the sentiment of the responses.

# %%
questions = [
    "Is the vaccine safe?",
    "What are the side effects?",
    "When will the pandemic end?"
]

print(f"{'Question':<40} | {'Sentiment':<10}")
print("-" * 55)

for q in questions:
    resp = requests.post(f"{BASE_URL}/chat", json={"message": q, "language": "en"})
    data = resp.json()
    # Note: Sentiment might be null if not implemented in API response yet, but let's check
    sentiment = data.get('sentiment', 'N/A') 
    print(f"{q:<40} | {str(sentiment):<10}")

# %%
