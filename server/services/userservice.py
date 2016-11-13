from repos import MongoUserRepo

class UserService:
    def __init__(self, repo=MongoUserRepo):
        self._repo = repo

    def find(self, username):
        return self._repo.getUser(username)

    def getUser(self,username, password):
        from Crypto.Hash import SHA256
        return self._repo.getUser(username, SHA256.new(password.encode("utf-8")).hexdigest())

    def register(self, username, password):
        from Crypto.Hash import SHA256
        return self._repo.addUser(username, SHA256.new(password.encode("utf-8")).hexdigest())
