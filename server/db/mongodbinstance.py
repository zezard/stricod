from pymongo import MongoClient
from utils import defaultConfig, defaultTestConfig
import os

class MongoDbInstance:

    def __init__(self, config = defaultConfig()):
        if "STRICOD_TEST" in os.environ.keys():
            config = defaultTestConfig()
        self._client  = MongoClient(config.getDbUrl())
        self._stricodDb = self._client[config.getStricodDbName()]
        self._geodataDb = self._client[config.getGeodataDbName()]

    def getUserCollection(self): return self._stricodDb.users
    def getGeodataCollection(self): return self._geodataDb.dms

