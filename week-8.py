## 🐍 `covid_tracker.py` – Python Code
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load only specific columns to reduce memory usage
use_cols = ['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']

DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"


try:
    print("🔄 Loading data...")
    df = pd.read_csv(DATA_URL)
    print("✅ Data loaded successfully.\n")
except Exception as e:
    print("❌ Error loading data:", e)
    exit()

# Basic Info
print("🔍 Inspecting dataset:")
print(df.head())
print("\nColumns:", df.columns.tolist())

# Keep relevant columns
df = df[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter for selected countries
countries = ['South Africa', 'India', 'United States', 'Brazil', 'Germany']
df = df[df['location'].isin(countries)]

# Check for missing values
print("\n🧹 Missing values before cleaning:")
print(df.isnull().sum())

# Fill missing values
df.fillna(0, inplace=True)

# Group latest data for a quick summary
latest = df[df['date'] == df['date'].max()]
summary = latest.groupby('location')[['total_cases', 'total_deaths']].sum().sort_values(by='total_cases', ascending=False)

print("\n📊 Latest COVID-19 Stats:")
print(summary)

# --------- 📈 VISUALIZATIONS ---------

sns.set(style="whitegrid")

# 1. Line Plot - Total Cases Over Time
plt.figure(figsize=(10, 5))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)

plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.show()

# 2. Bar Plot - Latest Total Deaths
plt.figure(figsize=(8, 5))
sns.barplot(x=summary.index, y=summary['total_deaths'], palette="Reds")
plt.title("Total Deaths by Country (Latest)")
plt.xlabel("Country")
plt.ylabel("Total Deaths")
plt.tight_layout()
plt.show()

# 3. Histogram - New Daily Cases (all countries)
plt.figure(figsize=(8, 4))
sns.histplot(df['new_cases'], bins=50, color='skyblue')
plt.title("Distribution of New Daily Cases")
plt.xlabel("New Cases")
plt.tight_layout()
plt.show()

# 4. Scatter Plot - Total Cases vs Total Deaths
plt.figure(figsize=(6, 6))
sns.scatterplot(data=summary, x='total_cases', y='total_deaths', hue=summary.index, s=100)
plt.title("Total Cases vs Total Deaths")
plt.xlabel("Total Cases")
plt.ylabel("Total Deaths")
plt.tight_layout()
plt.show()
