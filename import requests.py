import requests

headers = {
    'User-Agent': 'prioce_predictor - @siirberus on Discord',
    'From': 'kumail.gulamhusein@gmail.com'
}
response = requests.get(f"https://prices.runescape.wiki/api/v1/osrs/latest?id={2}", headers=headers)
data = response.json()
print(data)
