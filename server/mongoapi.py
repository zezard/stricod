from dbapi import User, UserRepo, Token, TokenRepo
from pymongo import MongoClient

class MongoStricodInstance:

    def __init__(self):
        self._client  = MongoClient('mongodb://localhost:27017/')
        self._stricodDb = self._client.stricod
        self._geodataDb = self._client.geodata

    def getUserCollection(self): return self._stricodDb.users
    def getTokenCollection(self): return self._stricodDb.tokens
    def getGeodataCollection(self): return self._geodataDb.dms

class MongoTokenRepo(TokenRepo):

    def __init__(self, tokenCollection):
        self.collection = tokenCollection

    def getUserId(self, token):
        query = {"token":token}
        token = self.collection.find_one(query)
        if not token: return None
        else: return Token(token["token"])

class MongoUserRepo(UserRepo):

    def __init__(self, userCollection):
        self.collection = userCollection 

    def getUser(self, username, password):
        query = {"username":username, "password":password}
        user = self.collection.find_one(query)

        if not user: return None
        else: return User(user['_id'], user['username'])

