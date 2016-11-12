from models.position import Position 

class GeodataRepo:

    def __init__(self):
        raise NotImplementedError

    def addPosition(self, position, uid):
        """ Add new position to the user's record.

        param position: A representation of the user's position
        param uid: User ID
        return: True if added, else False
        """
        raise NotImplementedError

    def getLastPosition(self, uid):
        """ Get the user's last known position

        param uid: User ID
        return: The last known position or None if non-existent
        """
        raise NotImplementedError

from datetime import datetime
from pymongo import DESCENDING
# ================================
# A MongoDB geodata repo is provided by default
# =============================
class MongoGeodataRepo(GeodataRepo):

    def __init__(self, geodataCollection):
        self.collection = geodataCollection

    def addPosition(self, position, uid):
        if position == None or uid == None:
            return False

        query = {"uid":uid,"dms":position.getDMS()}
        cid = self.collection.insert_one(query).inserted_id
        if not cid: return False
        else: return True
    
    def getLastPosition(self, uid):
        if uid == None:
            return None
        query = {"uid":uid}
        pos = self.collection.find(query).sort('_id', DESCENDING).limit(1)
        if pos.count(True) < 1: return None
        else: 
            pos = pos[0] # limit returns a list    
            return Position(pos['dms'], pos['_id'].generation_time)
