import json

class Config:
    def __init__(self
            , dbUrl
            , stricodDbName
            , geodataDbName
            , tokenDbName
            , testStricodDbName='test_'
            , testGeodataDbName='test_'
            , testTokenDbName='test_'):
        self._dbUrl = dbUrl

        self._stricodDbName = stricodDbName
        self._geodataDbName = geodataDbName
        self._tokenDbName = tokenDbName

        self._testStricodDbName = testStricodDbName + self._stricodDbName 
        self._testGeodataDbname = testGeodataDbName + self._geodataDbName
        self._testGeodataDbname = testTokenDbName + self._tokenDbName

    def getDbUrl(self): return self._dbUrl
    def getStricodDbName(self): return self._stricodDbName
    def getGeodataDbName(self): return self._geodataDbName
    def getTokenDbName(self): return self._tokenDbName
    def getTestStricodDbName(self): return self._testStricodDbName
    def getTestGeodataDbName(self): return self._testGeodataDbname
    def getTokenDbName(self): return self._tokenDbName

def defaultConfig():
    return Config('mongodb://localhost:27017', 'stricod', 'geodata', 'token')

def fromJson(configPath):
    with open(configPath,'r') as f:
        js = json.loads(f.read())
        return Config(js['dbUrl'],js['stricodDbName'],js['geodataDbName'],js['tokenDbName'])
