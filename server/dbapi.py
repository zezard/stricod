class User:
    def __init__(self, _id, name, email)
        self._id = _id
        self._name = name
    def getId(self): return self._id
    def getName(self): return self._name

class UserRepo:

    def __init__(self):
        raise NotImplementedError

    def addUser(self, username, password): 
        """ Store a user to the database if credentials are unique.

        param username: username string
        param password: password string
        returns: True if credentials are unique else False
        """

    def getUser(self, username, password):
        """ Search for a username with the provided credentials 

        param username: username string
        param password: password string
        returns: A User-object if found else None 
        """

