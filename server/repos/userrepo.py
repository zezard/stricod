from models.user import User

class UserRepo:

    def __init__(self):
        raise NotImplementedError

    def addUser(self, username, password): 
        """ Store a user to the database if credentials are unique.

        param username: username string
        param password: password string
        returns: True if credentials are unique else False
        """
        raise NotImplementedError

    def getUidByName(self, username):
        """ Search for a username with the provided credentials

        param username: username string
        returns: the user's id if found, else None
        """
        raise NotImplementedError

    def getUserById(self, uid):
        """ Search for a username with the provided credentials

        param uid: user id 
        returns: A User-object if found else None
        """
        raise NotImplementedError

    def getUser(self, username, password):
        """ Search for a username with the provided credentials

        param username: username string
        param password: password string
        returns: A User-object if found else None
        """
        raise NotImplementedError

# ================================
# A MongoDB user repo is provided by default
# =============================
class MongoUserRepo(UserRepo):

    def __init__(self, userCollection):
        self.collection = userCollection 

    def addUser(self, username, password):

        if self.getUidByName(username):
            return None

        query = {"username":username, "password":password}
        uid = self.collection.insert_one(query).inserted_id

        if not uid: return None
        else: return uid



    def getUidByName(self, username):
        query = {"username":username}
        user = self.collection.find_one(query)

        if not user: return None
        else: return user['_id']

    def getUserById(self, uid):
        query = {"_id":uid}
        user = self.collection.find_one(query)

        if not user: return None
        else: return User(str(user['_id']), user['username'])

    def getUser(self, username, password):
        query = {"username":username, "password":password}
        user = self.collection.find_one(query)

        if not user: return None
        else: return User(str(user['_id']), user['username'])
