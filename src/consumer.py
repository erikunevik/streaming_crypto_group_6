from quixstreams import Application
from pprint import pprint
#from quixstreams.sinks.community.postgresql import PostgreSQLSink

def retrieve_btc_info(btc):
    quote_data = btc["quote"]["SEK"]
    return {         
        "Price": round(quote_data["price"], 4),
        "Total supply": btc["total_supply"],
        "Max supply": btc.get("max_supply"),
        "Market cap": quote_data["market_cap"],
        "Market cap dominance": quote_data["market_cap_dominance"],
        "Percentage change in 1 hour": quote_data["percent_change_1h"],
        "Percentage change in 24 hours": quote_data["percent_change_24h"],
        "Percentage change in 7 days": quote_data["percent_change_7d"],
        "Last updated": quote_data["last_updated"],
        
    }

def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="message_consumers",
        auto_offset_reset="earliest",
    )

    crypto_topic = app.topic(name="crypto", value_deserializer="json")

    streaming_data = app.dataframe(topic=crypto_topic)

    streaming_data = streaming_data.apply(retrieve_btc_info)

    streaming_data.update(lambda btc_output: (pprint(btc_output), print()))

    # sink to postgres


    # Keep the application running
    app.run()

if __name__ == "__main__":
    main()
