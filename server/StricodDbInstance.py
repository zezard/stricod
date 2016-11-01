from pymongo import MongoClient

class StricodDbInstance:

    def __init__(self):
        self._client  = MongoClient('mongodb://localhost:27017/')
        self._stricodDb = self._client.stricod
        self._geodataDb = self._client.geodata

    def getUserCollection(self): return self._stricodDb.users
    def getTokenCollection(self): return self._stricodDb.tokens
    def getGeodataCollection(self): return self._geodataDb.dms

