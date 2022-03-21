import os
from typing import List
from pymongo import MongoClient

class DbClient (object):
    __CONNECTION_STRING = os.environ.get("MONGO_DB_CONNECTION_STRING") 
    db = None
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DbClient, self).__new__(self)
            self.instance.__connect()
        return self.instance

    def __connect (self) -> None:
        client = MongoClient(self.__CONNECTION_STRING)
        self.db = client.intellisite
        
    def get_detections(self, skip:int = 0, limit:int = 0) -> List:    
        detections_cursor = self.db.detections.find().skip(skip).limit(limit)
        detections = [detection for detection in detections_cursor]
        [detection.pop("_id") for detection in detections]
        return detections
        
    def get_detections_by_maker(self) -> List:    
        detections_cursor = self.db.detections.aggregate([
            {
                "$group" : {
                    "_id" : "$Make",
                    "Detections_count" : {"$sum" : 1}
                } 
            }
        ])
        detections = [detection for detection in detections_cursor]
        for detection in detections:
            detection["Make"] = detection["_id"]
            del detection["_id"]
        return detections

    
    