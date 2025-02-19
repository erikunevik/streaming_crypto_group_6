from requests import Session
from constants import EXCHANGERATEAPI_KEY
import json

def get_latest_exchange_rate():
    currency_url = "https://api.exchangeratesapi.io/v1/latest"
    parameters = {
        "access_key": EXCHANGERATEAPI_KEY,
        "base" : "EUR",
        "symbols" : "SEK,DKK,NOK",
    }
    session = Session()

    response = session.get(currency_url, params=parameters)

    return json.loads(response.text)["rates"]

# currencies_dict = {
#     "SEK": 10.72,
#     "DKK": 7.34,
#     "NOK" : 11.74,
#     "EUR" : 0.96
# }