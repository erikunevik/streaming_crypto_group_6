from requests import Session
from constants import COINMARKET_API
import json

def get_latest_coin_data(symbol="BTC"):
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    parameters = {
        "symbol": symbol,
        "convert": "SEK",
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(api_url, params=parameters)

    if response.status_code == 200:
        return json.loads(response.text)["data"][symbol]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)