from flask_pymongo import PyMongo
from pymongo import MongoClient

class DbService (object):
    CONNECTION_STRING = "mongodb://root:masterkey@mongo:27017"
    db = None
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DbService, self).__new__(self)
            self.db = self.__connect()
        return self.instance

    def __connect (self):
        client = MongoClient(self.CONNECTION_STRING)
        return client.intellisite
        
    def get_detections(self, skip:int = 0, limit:int = 0) -> list:    
        detections = self.db.detections.find().skip(skip).limit(limit)
        return [detection.pop("_id") for detection in detections]
        
    def get_alerts(self) -> list:
        alerts = self.db.alerts.find()
        return [alert.pop("_id") for alert in alerts]
    
    