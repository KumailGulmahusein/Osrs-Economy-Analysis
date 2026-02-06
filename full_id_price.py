import requests
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timezone
import time
from config import HEADERS, DB_CONFIG

headers = HEADERS

# API details
ITEM_ID = 2
API_URL = f"https://api.weirdgloop.org/exchange/history/osrs/all?id={ITEM_ID}"

# Connect to MySQL
try:
    conn = mysql.connector.connect(**DB_CONFIG)

    cursor = conn.cursor()
    print("Connected to MySQL")
except mysql.connector.Error as err:
    print(err)
    exit(1)

# Table name for this item
table_name = f"item_{ITEM_ID}_prices"

# Create table if not exists
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price INT,
    volume INT,
    timestamp DATETIME,
    UNIQUE KEY unique_entry (timestamp)
)
"""
cursor.execute(create_table_query)

# Fetch data from API
items_data = []
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    item_key = str(ITEM_ID)

    if item_key in data:
        for entry in data[item_key]:
            timestamp_ms = entry.get("timestamp")
            date = datetime.fromtimestamp(timestamp_ms / 1000, timezone.utc)

            items_data.append((
                entry.get("price"),
                entry.get("volume"),
                date
            ))
    else:
        print(f"No data found for item {ITEM_ID}")
else:
    print(f"Failed: {response.status_code}")

time.sleep(1)

# Insert into the item-specific table
if items_data:
    insert_query = f"""
    INSERT INTO {table_name} (price, volume, timestamp)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        price = VALUES(price),
        volume = VALUES(volume)
    """
    cursor.executemany(insert_query, items_data)
    conn.commit()
    print(f"Inserted/Updated {cursor.rowcount} rows into {table_name}")
else:
    print("No data to insert")

# Close connection
cursor.close()
conn.close()