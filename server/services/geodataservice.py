from models import fromDMS 
from repos import MongoGeodataRepo
from utils import defaultConfig

class GeodataService:
    def __init__(self, repo=MongoGeodataRepo):
        self._repo = repo

    def addDmsPosition(self, d, m, s, uid): 
        position = fromDMS(d,m,s)
        ok = self._repo.addPosition(position, uid)
        if not ok: return False
        else: return True

    def getLastPosition(self, uid):
        return self._repo.getLastPosition(uid)
