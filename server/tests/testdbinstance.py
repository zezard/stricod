from db import MongoDbInstance 
class MongoTestDbInstance(MongoDbInstance):
    def dropAll(self): 
        self.getUserCollection().delete_many({})
        self.getGeodataCollection().delete_many({})
