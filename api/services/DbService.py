from pymongo import MongoClient

class DbService :
    @staticmethod
    def get_db():
        CONNECTION_STRING = "mongodb://root:masterkey@mongo:27017"
        client = MongoClient(CONNECTION_STRING)
        return client.intellisite