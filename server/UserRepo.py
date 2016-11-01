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

    def getUser(self, username, password):
        query = {"username":username, "password":password}
        user = self.collection.find_one(query)

        if not user: return None
        else: return User(user['_id'], user['username'])

