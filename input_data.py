import mysql.connector
import requests

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='[USER]',
    password='[PASS]',
    database='[DATABASE]'
)
cursor = conn.cursor()

# Fetch JSON data from URL
url = 'https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json'
response = requests.get(url)
data = response.json()

# SQL insert statement
sql = """
    INSERT INTO items (id, name, examine, members, lowalch, highalch, value, `limit`, icon, price, last, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        examine = VALUES(examine),
        members = VALUES(members),
        lowalch = VALUES(lowalch),
        highalch = VALUES(highalch),
        value = VALUES(value),
        `limit` = VALUES(`limit`),
        icon = VALUES(icon),
        price = VALUES(price),
        last = VALUES(last),
        volume = VALUES(volume)
"""
# Open log file for failed items
failed_items_log = open('failed_items.log', 'w')

# Loop through each item and handle errors
successful = 0
failed = 0

for item_id, item in data.items():
    try:
        # Process only if item is a dict
        if not isinstance(item, dict):
            raise ValueError(f"Item {item_id} is not a dictionary.")

        # Fetch each value
        id_val = item.get('id', 0)
        name_val = item.get('name', '')
        examine_val = item.get('examine', '')
        members_val = item.get('members', 0)
        lowalch_val = item.get('lowalch', 0)
        highalch_val = item.get('highalch', 0)
        value_val = item.get('value', 0)
        limit_val = item.get('limit', 0)
        icon_val = item.get('icon', '')
        price_val = item.get('price', 0)
        last_val = item.get('last', 0)
        volume_val = item.get('volume', 0)

        values = (
            id_val,
            name_val,
            examine_val,
            members_val,
            lowalch_val,
            highalch_val,
            value_val,
            limit_val,
            icon_val,
            price_val,
            last_val,
            volume_val
        )

        # Execute SQL
        cursor.execute(sql, values)
        successful += 1
        
    except Exception as e:
        error_message = f"Failed to process item {item_id}: {e}\n"
        print(error_message.strip())
        failed_items_log.write(error_message)
        failed += 1

# Close log file
failed_items_log.close()

# Commit and close DB connection
conn.commit()
cursor.close()
conn.close()

print(f"Data import completed. Successful: {successful}, Failed: {failed}")
