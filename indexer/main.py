import os
import json
from time import sleep
from kafka import KafkaProducer
from kafka import KafkaConsumer
from faker import Faker

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC")

if __name__ == "__main__":
    consumer = KafkaConsumer(
        DETECTIONS_TOPIC,
        bootstrap_servers= KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    for message in consumer:
        message = message.value
        producer.send(ALERTS_TOPIC, value=message)
        sleep(3)