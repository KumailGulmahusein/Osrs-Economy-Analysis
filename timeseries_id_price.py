import requests
import mysql.connector
import time
from datetime import datetime
from config import DB_CONFIG, HEADERS


ITEM_ID = 2
URL = f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=24h&id={ITEM_ID}"


def main():

    time.sleep(1)


    # 1. Fetch data
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    data = response.json()["data"]


    # 2. Connect to MySQL
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()


    # 3. Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS osrs_market_data (
            item_id INT NOT NULL,
            timestamp DATETIME NOT NULL,
            high_price INT,
            low_price INT,
            high_volume BIGINT,
            low_volume BIGINT,
            PRIMARY KEY (item_id, timestamp)
        )
    """)


    # 4. Insert SQL
    insert_sql = """
        INSERT INTO osrs_market_data
        (item_id, timestamp, high_price, low_price, high_volume, low_volume)
        VALUES (%s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
            high_price = VALUES(high_price),
            low_price = VALUES(low_price),
            high_volume = VALUES(high_volume),
            low_volume = VALUES(low_volume)
    """


    # 5. Prepare rows
    rows = []

    for row in data:

        ts = datetime.utcfromtimestamp(row["timestamp"])

        rows.append((
            ITEM_ID,
            ts,
            row["avgHighPrice"],
            row["avgLowPrice"],
            row["highPriceVolume"],
            row["lowPriceVolume"]
        ))


    # 6. Insert
    cursor.executemany(insert_sql, rows)
    conn.commit()


    print(f"Inserted/updated {len(rows)} rows")


    # 7. Close
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
