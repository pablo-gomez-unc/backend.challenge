import os
from typing import Dict, List
from pymongo import MongoClient

from services.LoggingService import LoggingService

class DbClient(object):
    __CONNECTION_STRING = os.environ.get("MONGO_DB_CONNECTION_STRING") 
    
    def __new__(self,db=None,logger=None):
        if not hasattr(self, 'instance'):
            self.instance = super(DbClient, self).__new__(self)
        return self.instance
    
    def __init__(self,db=None,logger=None):
        self.db = self.__connect_db() if db is None else db
        self.logger = LoggingService().get_logger() if logger is None else logger
    
    def __connect_db (self) :
        client = MongoClient(self.__CONNECTION_STRING)
        return client.intellisite
        
    def get_detections(self, skip:int = 0, limit:int = 0) -> List:    
        try:
            detections_cursor = self.db.detections.find().skip(skip).limit(limit)
            detections = [detection for detection in detections_cursor]
            [detection.pop("_id") for detection in detections]
            return detections
        except:
            self.logger.error("Error trying to communicate with database" )
            return []
        
    def get_detections_by_maker(self) -> List: 
        try:   
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
        except:
            self.logger.error("Error trying to communicate with database" )
            return []

    def get_user(self, user_id:str, password:str) -> Dict:
        try:
            users_cursor = self.db.users.find({
                "$and" : [
                    {
                    "user_id" : { "$eq" : user_id}
                    },
                    {
                    "password" : { "$eq" : password}
                    }
                ]
            })   
            users = [user for user in users_cursor]
            if len(users) == 0:
                raise Exception("No user found with that user/password combination")
            [user.pop("_id") for user in users]
            return users[0] if len(users) != 0 else {}
        except:
            self.logger.error("Error trying to communicate with database" )
            return {}
        
    def get_user_list(self) -> List:
        try:
            users_cursor = self.db.users.find({},{"user_id":1})   
            users = [user for user in users_cursor]
            if len(users) == 0:
                raise Exception("No users in database")
            [user.pop("_id") for user in users]
            return users
        except:
            self.logger.error("Error trying to communicate with database" )
            return {}