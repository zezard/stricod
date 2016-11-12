from pymongo import MongoClient
from utils import defaultConfig 

class MongoDbInstance:

    def __init__(self, config = defaultConfig()):
        self._client  = MongoClient(config.getDbUrl())
        self._stricodDb = self._client[config.getStricodDbName()]
        self._geodataDb = self._client[config.getGeodataDbName()]

    def getUserCollection(self): return self._stricodDb.users
    def getTokenCollection(self): return self._stricodDb.tokens
    def getGeodataCollection(self): return self._geodataDb.dms

