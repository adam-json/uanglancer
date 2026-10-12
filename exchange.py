import requests

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)
data = response.json()

print(data["rates"]["IDR"])