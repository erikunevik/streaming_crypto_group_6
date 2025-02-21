from constants import (
    COINMARKET_API,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from requests import Session
import json
from sqlalchemy import create_engine
import pandas as pd
import time


def get_listings_data(sort):
    listing_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    listing_parameters = {
        "limit": 10,
        "convert": "EUR",
        "sort": sort,
        "sort_dir": "desc",
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    session = Session()
    
    session.headers.update(headers)
    response = session.get(listing_url, params=listing_parameters)

    if response.status_code == 200:
        return json.loads(response.text)["data"]
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

    # market cap
    cap_df = pd.DataFrame(get_listings_data("market_cap"))
    cap_df["market_cap"] = cap_df["quote"].apply(lambda x: x["EUR"]["market_cap"])
    cap_df["market_cap_dominance"] = cap_df["quote"].apply(lambda x: x["EUR"]["market_cap_dominance"])
    cap_df_brief = cap_df[["name", "symbol", "market_cap", "market_cap_dominance"]]
    cap_df_brief.to_sql(
        "cap_top_10",
        postgres_connection,
        schema="public",
        if_exists="replace",
        index=False,
    )

     # volume_24h
    vol_df = pd.DataFrame(get_listings_data("volume_24h"))
    vol_df["volume_24h"] = vol_df["quote"].apply(lambda x: x["EUR"]["volume_24h"])
    vol_df_brief = vol_df[["name", "symbol", "volume_24h"]]
    vol_df_brief.to_sql(
        "vol_top_10",
        postgres_connection,
        schema="public",
        if_exists="replace",
        index=False,
    )


# python preamble
if __name__ == "__main__":
    while True:
        main()
        print("running every hour")
        time.sleep(3600)