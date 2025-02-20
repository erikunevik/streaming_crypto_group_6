
# Hardcoded due to limited free API calls
currencies_dict = {
    "SEK": 11.20,
    "DKK": 7.46,
    "NOK" : 11.61,
    "EUR" : 0
}

#--------ran out of api usage on free plan
# from requests import Session
# from constants import EXCHANGERATEAPI_KEY
# import json

# def get_latest_exchange_rate():
#     currency_url = "https://api.exchangeratesapi.io/v1/latest"
#     parameters = {
#         "access_key": EXCHANGERATEAPI_KEY,
#         "base" : "EUR",
#         "symbols" : "SEK,DKK,NOK",
#     }
#     session = Session()

#     response = session.get(currency_url, params=parameters)

#     return json.loads(response.text)["rates"]