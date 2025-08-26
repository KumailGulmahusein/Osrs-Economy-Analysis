import requests

headers = {
    'User-Agent': '[DISCORD] on Discord',
    'From': '[EMAIL]'
}
response = requests.get(f"https://prices.runescape.wiki/api/v1/osrs/latest?id={2}", headers=headers)
data = response.json()
print(data)
