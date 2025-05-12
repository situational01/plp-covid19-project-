import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

# Load COVID-19 data from Our World in Data (OWID)
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
print("Fetching data...")
response = requests.get(url)

if response.status_code != 200:
    raise Exception("Failed to fetch data. Please check the URL or your internet connection.")

print("Data fetched successfully. Processing...")
data = pd.read_csv(StringIO(response.text), parse_dates=['date'])

# Filter relevant columns
columns = [
    'location', 'date', 'total_cases', 'new_cases',
    'total_deaths', 'new_deaths', 'population'
]
df = data[columns].dropna(subset=['total_cases', 'location', 'date'])

# Filter out continents and global aggregates
excluded = ['World', 'Europe', 'Asia', 'Africa', 'North America', 'South America', 'Oceania', 'International']
df = df[~df['location'].isin(excluded)]

# Get latest data per country
latest_date = df['date'].max()
latest_df = df[df['date'] == latest_date]
top_countries = latest_df.sort_values(by='total_cases', ascending=False).head(10)

# Plot top 10 countries by total cases
plt.figure(figsize=(12, 6))
sns.barplot(data=top_countries, x='total_cases', y='location', palette='Reds_r')
plt.title(f"Top 10 Countries by Total COVID-19 Cases as of {latest_date.date()}")
plt.xlabel("Total Cases")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("top10_total_cases.png")
plt.show()

# Plot case trend for selected country
country = "United States"
country_df = df[df['location'] == country]

plt.figure(figsize=(12, 6))
sns.lineplot(data=country_df, x='date', y='total_cases', label='Total Cases')
sns.lineplot(data=country_df, x='date', y='total_deaths', label='Total Deaths')
plt.title(f"COVID-19 Case Trend in {country}")
plt.xlabel("Date")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig(f"{country.lower().replace(' ', '_')}_trend.png")
plt.show()
