import time
from quixstreams import Application
from constants import COINMARKET_API
from connect_api import get_latest_coin_data

app = Application(broker_address="localhost:9092", consumer_group="crypto_group",)

crypto_topic = app.topic(name="crypto", value_serializer="json")

def main():
    with app.get_producer() as producer:
        while True:
            crypto_latest = get_latest_coin_data("BTC,SOL")
            for value in crypto_latest.values():
                kafka_message = crypto_topic.serialize(key=value["symbol"], value=value)

                print(f"produce event with key = {kafka_message.key}, price = {value['quote']['USD']['price']}")

                producer.produce(topic=crypto_topic.name, key= kafka_message.key, value= kafka_message.value)
            
            time.sleep(30)

#python preamble

if __name__ == "__main__":
    main()