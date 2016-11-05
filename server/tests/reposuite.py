import unittest 

from repos import MongoUserRepo
from repos import MongoTokenRepo
from utils import Config
from .testdbinstance import MongoTestDbInstance

class TestUserRepo(unittest.TestCase):

    def setUp(self):
        self.mdb = MongoTestDbInstance(Config.defaultTestConfig())
        self.userRepo = MongoUserRepo(self.mdb.getUserCollection())

    def tearDown(self):
        self.mdb.dropAll()


    def testAddUser(self):
        self.userRepo.addUser("foo","bar")
        user = self.userRepo.getUser("foo","bar")
        self.assertEqual(user.getName(), "foo")

class TestTokenRepo(unittest.TestCase):

    def setUp(self):
        mdb = MongoTestDbInstance(Config.defaultTestConfig())
        userRepo = MongoUserRepo(mdb.getUserCollection())
        userRepo.addUser("foo","bar")
        self.user = userRepo.getUser("foo","bar")
        self.tokenRepo = MongoTokenRepo(mdb.getTokenCollection())

    def testAddToken(self):
        token = "just_a_stupid_token_string"
        self.tokenRepo.addToken(token, self.user.getId())
        self.assertEqual(self.user.getId(), self.tokenRepo.getUserId(token).get())


if __name__ == '__main__':
    unittest.main()

