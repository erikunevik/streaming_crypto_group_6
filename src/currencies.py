from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    EXCHANGERATEAPI_KEY
)
from requests import Session
import json
from sqlalchemy import create_engine
import pandas as pd
import datetime
import time


def get_latest_exchange_rate():
    currency_url = "https://api.exchangeratesapi.io/v1/latest"
    parameters = {
        "access_key": EXCHANGERATEAPI_KEY,
        "base" : "EUR",
        "symbols" : "SEK,DKK,NOK",
    }
    session = Session()

    response = session.get(currency_url, params=parameters)

    if response.status_code == 200:
        return json.loads(response.text)["rates"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    db_user = POSTGRES_USER
    db_host = POSTGRES_HOST
    db_port = POSTGRES_PORT
    db_password = POSTGRES_PASSWORD
    db_name = POSTGRES_DBNAME

    postgres_connection = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    # create dataframe
    currency_dict = get_latest_exchange_rate()
    currency_df = pd.DataFrame(currency_dict, index=[0])
    currency_df["EUR"] = 1
    currency_df["date"] = datetime.date.today()
    
    currency_df.to_sql(
        "currency_table",
        postgres_connection,
        schema="public",
        if_exists="replace",
        index=False,
        )

# python preamble
if __name__ == "__main__":
    while True:
        main()
        print("running once per day")
        time.sleep(86400)

# # Hardcoded values
# currencies_dict = {
#     "SEK": 11.20,
#     "DKK": 7.46,
#     "NOK" : 11.61,
#     "EUR" : 0
# }