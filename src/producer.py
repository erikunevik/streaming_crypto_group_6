import time
from quixstreams import Application
from constants import COINMARKET_API
from connect_api import get_latest_coin_data

app = Application(broker_address="localhost:9092", consumer_group="crypto_group",)

crypto_topic = app.topic(name="crypto", value_serializer="json")

"""
TODO: This now only pushes the price for Bitcoin, we should add more interesting data to the Kafka meessage
"""

def main():
    with app.get_producer() as producer:
        while True:
            crypto_latest = get_latest_coin_data()

            kafka_message = crypto_topic.serialize(key=crypto_latest["symbol"], value=crypto_latest)

            print(f"produce event with key = {kafka_message.key}, price = {crypto_latest['quote']['SEK']['price']}")

            producer.produce(topic=crypto_topic.name, key= kafka_message.key, value= kafka_message.value)
            
            time.sleep(30)

#python preamble

if __name__ == "__main__":
    main()