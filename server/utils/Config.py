import json

class Config:

    def __init__(self, dbUrl, stricodDbName, geodataDbName, tokenDbName):
        self._dbUrl = dbUrl
        self._stricodDbName = stricodDbName
        self._geodataDbName = geodataDbName
        self._tokenDbName = tokenDbName

    def getDbUrl(self): return self._dbUrl
    def getTokenDbName(self): return self._tokenDbName
    def getStricodDbName(self): return self._stricodDbName
    def getGeodataDbName(self): return self._geodataDbName


def defaultConfig():
    return Config('mongodb://localhost:27017', 'stricod', 'geodata', 'token')

def defaultTestConfig():
    return Config('mongodb://localhost:27017', 'test_stricod', 'test_geodata', 'test_token')

def fromJson(configPath):
    with open(configPath,'r') as f:
        js = json.loads(f.read())
        return Config(js['dbUrl'],js['stricodDbName'],js['geodataDbName'],js['tokenDbName'])
