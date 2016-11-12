from repos import MongoUserRepo

class UserService:
    def __init__(self, repo=MongoUserRepo):
        self._repo = repo

    def find(self, username):
        return self._repo.getUser(username)

    def getUser(self,username, password):
        return self._repo.getUser(username ,password)

    def register(self, username, password):
        return self._repo.addUser(username, password)
