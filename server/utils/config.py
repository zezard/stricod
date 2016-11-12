import json

class Config:

    def __init__(self, dbUrl, stricodDbName, geodataDbName, jwtSecret):
        self._dbUrl = dbUrl
        self._stricodDbName = stricodDbName
        self._geodataDbName = geodataDbName
        self._jwtSecret = jwtSecret

    def getDbUrl(self): return self._dbUrl
    def getJwtSecret(self): return self._jwtSecret
    def getStricodDbName(self): return self._stricodDbName
    def getGeodataDbName(self): return self._geodataDbName

def defaultConfig():
    return Config(
            'mongodb://localhost:27017', 
            'stricod', 
            'geodata', 
            'phoo6TazeeL7sei7thuw')

def defaultTestConfig():
    return Config(
            'mongodb://localhost:27017', 
            'test_stricod', 
            'test_geodata', 
            'ThooYeiXuk1ahs4lahfe') 

def fromJson(configPath):
    with open(configPath,'r') as f:
        js = json.loads(f.read())
        return Config(js['dbUrl'],js['stricodDbName'],js['geodataDbName'],js['jwtSecret'])
