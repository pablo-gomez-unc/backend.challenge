from typing import List
from clients.DbClient import DbClient

class DetectionsService (object):
    __db_client = None
    __instance = None
    
    def __init__(self):
        if DetectionsService.__instance is not None:
            pass
        DetectionsService.__instance = self
        DetectionsService.__db_client = DbClient()
    
    def __init__(self,db_client):
        if DetectionsService.__instance is not None:
            pass
        DetectionsService.__instance = self
        DetectionsService.__db_client = db_client
    
    def get_detections(self, skip:int, limit:int) -> List:
        return self.__db_client.get_detections(skip,limit)
    
    def get_detections_by_maker(self) -> List:
        return self.__db_client.get_detections_by_maker()
    