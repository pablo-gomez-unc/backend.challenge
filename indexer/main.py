import os
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC")
SUSPICIOUS_VEHICLE = os.environ.get("SUSPICIOUS_VEHICLE")

if __name__ == "__main__":
    consumer = KafkaConsumer(
        DETECTIONS_TOPIC,
        bootstrap_servers= KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value.decode('utf-8'))
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode()
    )
    for message in consumer:
        message = message.value
        if message['Category'] == SUSPICIOUS_VEHICLE :
            producer.send(ALERTS_TOPIC, value=message)