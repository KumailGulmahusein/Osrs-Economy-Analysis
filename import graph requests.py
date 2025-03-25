import requests
import pandas as pd
import time
from datetime import datetime, timezone

headers = {
    'User-Agent': 'Time Series',
    'From': '@siirberus on Discord'
}

# API details
Item_ID = 2
API_URL = f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=1h&id={Item_ID}"


items_data = []

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Process data and add to list
    for entry in data["data"]:
        timestamp = entry.get("timestamp", 0)
        date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        items_data.append({
            "item_id": Item_ID,
            "timestamp": date,
            "avgHighPrice": entry.get("avgHighPrice", "N/A"),
            "avgLowPrice": entry.get("avgLowPrice", "N/A"),
            "highPriceVolume": entry.get("highPriceVolume", "N/A"),
            "lowPriceVolume": entry.get("lowPriceVolume", "N/A"),
        })
else:
    print(f"Failed to fetch data for item {Item_ID}: {response.status_code} - {response.text}")

time.sleep(1)  # Needed for large requests

# Save to CSV
df = pd.DataFrame(items_data)
filename = f"osrs_item_{Item_ID}_prices.csv"
print(f"Saving data to: {filename}")
df.to_csv(filename, index=False)