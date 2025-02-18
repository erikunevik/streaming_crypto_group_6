from pprint import pprint
from quixstreams import Application
from quixstreams.sinks.community.postgresql import PostgreSQLSink

from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)

def retrieve_coins_info(coin):
    quote_data = coin["quote"]["USD"]
    return {    
        "Name": coin["name"],         
        "Price": round(quote_data["price"], 4),
        "Total supply": coin["total_supply"],
        "Max supply": coin.get("max_supply"),
        "Market cap": quote_data["market_cap"],
        "Market cap dominance": quote_data["market_cap_dominance"],
        "Percentage change in 1 hour": quote_data["percent_change_1h"],
        "Percentage change in 24 hours": quote_data["percent_change_24h"],
        "Percentage change in 7 days": quote_data["percent_change_7d"],
        "Percentage change in 30 days": quote_data["percent_change_30d"],
        "Last updated": quote_data["last_updated"],
    }

def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="quotes_coins",
        schema_auto_update=True,
    )

    return sink

def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="crypto_consumers",
        auto_offset_reset="earliest",
    )


    crypto_topic = app.topic(name="crypto", value_deserializer="json")
    
    streaming_data = app.dataframe(topic=crypto_topic)
    
    # transformation
    
    streaming_data = streaming_data.apply(retrieve_coins_info)
    
    streaming_data.update(lambda btc_output: (pprint(btc_output), print()))
    
    # sink postgres
   
    postgres_sink = create_postgres_sink()
    
    streaming_data.sink(postgres_sink)

    # Keep the application running
    app.run()

if __name__ == "__main__":
    main()