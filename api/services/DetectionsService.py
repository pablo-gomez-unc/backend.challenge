from typing import List
from clients.DbClient import DbClient

class DetectionsService (object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DetectionsService, self).__new__(self)
        return self.instance
    
    def get_detections(self, skip:int, limit:int) -> List:
        return DbClient().get_detections(skip,limit)
    
    def get_detections_by_maker(self) -> List:
        return DbClient().get_detections_by_maker()