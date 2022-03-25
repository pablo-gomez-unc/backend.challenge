from typing import List
from clients.DbClient import DbClient

class DetectionsService(object):
    def __new__(self,client=None):
        if not hasattr(self, 'instance'):
            self.instance = super(DetectionsService, self).__new__(self)
        return self.instance
    
    def __init__(self,client=None):
        self.db_client = DbClient() if client is None else client
    
    def get_detections(self, skip:int, limit:int) -> List:
        return self.db_client.get_detections(skip,limit)
    
    def get_detections_by_maker(self) -> List:
        return self.db_client.get_detections_by_maker()
    