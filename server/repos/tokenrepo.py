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


# ================================
# A MongoDB token repo is provided by default
# =============================
class MongoTokenRepo(TokenRepo):

    def __init__(self, tokenCollection):
        self.collection = tokenCollection

    def addToken(self, token, uid):
        if self.collection.find_one({"token":token}) != None:
            return False

        query = {"token":token, "userid":uid}
        tokenId = self.collection.insert_one(query).inserted_id
        if not tokenId: return False 
        else: return True 

    def getUserId(self, token):
        query = {"token":token}
        token = self.collection.find_one(query)
        if not token: return None
        else: return Token(token["userid"])

