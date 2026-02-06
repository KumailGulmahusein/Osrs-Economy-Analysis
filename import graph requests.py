import requests
import pandas as pd
import time
from datetime import datetime, timezone
from config import HEADERS

headers = HEADERS

# API details
ITEM_ID = 2
API_URL = f"https://api.weirdgloop.org/exchange/history/osrs/all?id={ITEM_ID}"

items_data = []

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    data = response.json()

    # The data is keyed by item ID as a string
    item_key = str(ITEM_ID)

    if item_key in data:
        for entry in data[item_key]:
            timestamp_ms = entry.get("timestamp")

            # Convert milliseconds → seconds
            date = datetime.fromtimestamp(
                timestamp_ms / 1000, timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")

            items_data.append({
                "item_id": ITEM_ID,
                "price": entry.get("price"),
                "volume": entry.get("volume"),  # will be None, that's fine
                "timestamp": date,
            })
    else:
        print(f"No data found for item {ITEM_ID}")

else:
    print(f"Failed to fetch data for item {ITEM_ID}: {response.status_code} - {response.text}")

time.sleep(1)  # Polite delay

# Save to CSV
df = pd.DataFrame(items_data)
filename = f"osrs_item_{ITEM_ID}_prices.csv"
print(f"Saving data to: {filename}")
df.to_csv(filename, index=False)
