import os
import json

from time import sleep

from kafka import KafkaProducer
from kafka import KafkaConsumer

from pymongo import MongoClient

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
DETECTIONS_TOPIC = os.environ.get("DETECTIONS_TOPIC")
ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC")
SUSPICIOUS_VEHICLE = os.environ.get("SUSPICIOUS_VEHICLE")

def get_database():
    CONNECTION_STRING = "mongodb://root:masterkey@mongo:27017"
    client = MongoClient(CONNECTION_STRING)
    return client["intellisite"]

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
    
    db = get_database()
    alerts = db['alerts']
    detections = db['detections']
    
    for message in consumer:
        message = message.value
        detections.insert_one(message)
        del message['_id']
        if message['Category'] == SUSPICIOUS_VEHICLE :
            producer.send(ALERTS_TOPIC, value=message)
            alerts.insert_one(message)