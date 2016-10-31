class User:
    def __init__(self, _id, name):
        self._id = _id
        self._name = name
    def getId(self): return self._id
    def getName(self): return self._name
    def __repr__(self): return "User("+str(self._id)+", "+self._name+")"

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

class Token:
    def __init__(self, token):
        self.token = token
    def __repr__(self): return "Token("+self.token+")"
    def get(self): return self.token

class TokenRepo:

    def __init__(self):
        raise NotImplementedError

    def addToken(self, token, uid):
        """ Store a token associated with the user id.

        param token: token string
        param uid: user id 
        returns: True if completed else False
        """
        raise NotImplementedError

    def getUserId(self, token):
        """ Get the user id associated with the token.

        param token: token string 
        returns: user id if associated with token 
        """
        raise NotImplementedError

