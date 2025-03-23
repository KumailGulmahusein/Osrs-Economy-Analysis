import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np

# Fetch data
url = "https://secure.runescape.com/m=itemdb_rs/api/graph/2.json"
response = requests.get(url)
data = response.json()  

# Convert daily and average data to DataFrames
daily_df = pd.DataFrame(list(data['daily'].items()), columns=['timestamp', 'daily_price'])
average_df = pd.DataFrame(list(data['average'].items()), columns=['timestamp', 'average_price'])

# Convert timestamp to datetime
daily_df['date'] = pd.to_datetime(daily_df['timestamp'].astype(int), unit='ms')
average_df['date'] = pd.to_datetime(average_df['timestamp'].astype(int), unit='ms')

# Merge both on date
merged_df = pd.merge(daily_df[['date', 'daily_price']], average_df[['date', 'average_price']], on='date')

# Create a figure with subplots: 1 row, 2 columns
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the line chart
ax.plot(merged_df['date'], merged_df['daily_price'], label='Daily Price', color='blue')
ax.plot(merged_df['date'], merged_df['average_price'], label='Average Price', color='orange', linestyle='--')

ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Daily vs. Average Price Over Time')
ax.legend()
tick_positions = np.linspace(0, len(merged_df) - 1, num=20, dtype=int)
plt.xticks(merged_df['date'].iloc[tick_positions], rotation=45)

# Adjust layout and show plot
plt.tight_layout()
plt.show()