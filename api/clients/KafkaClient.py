from cmath import log
import json
import os
from flask import app, current_app, jsonify

from kafka import KafkaConsumer

class KafkaClient (object):
    __KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL") 
    __ALERTS_TOPIC = os.environ.get("ALERTS_TOPIC") 
    alerts_consumer = None
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(KafkaClient, self).__new__(self)
        return self.instance
    
    def __register_consumer (self):
        self.alerts_consumer = KafkaConsumer(
            self.__ALERTS_TOPIC,
            bootstrap_servers= self.__KAFKA_BROKER_URL        
        )
    
    def listen (self):
        self.__register_consumer()
        for message in self.alerts_consumer:
            yield message.value