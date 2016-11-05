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

    def testCannotGetNonexistingUser(self):
        user = self.userRepo.getUser("foo")
        self.assertEqual(user, None)

    def testAddUser(self):
        self.userRepo.addUser("foo","bar")
        user = self.userRepo.getUser("foo")
        self.assertEqual(user.getName(), "foo")

    def testCannotAddExistingUser(self):
        self.userRepo.addUser("foo","bar")
        user = self.userRepo.getUser("foo")
        self.assertEqual(user.getName(), "foo")

        ok = self.userRepo.addUser("foo","bar2")
        self.assertEqual(ok, False)

class TestTokenRepo(unittest.TestCase):

    def setUp(self):
        self.mdb = MongoTestDbInstance(Config.defaultTestConfig())
        userRepo = MongoUserRepo(self.mdb.getUserCollection())
        userRepo.addUser("foo","bar")
        self.user = userRepo.getUser("foo")
        self.tokenRepo = MongoTokenRepo(self.mdb.getTokenCollection())

    def tearDown(self):
        self.mdb.dropAll()

    def testAddToken(self):
        token = "just_a_stupid_token_string"
        self.tokenRepo.addToken(token, self.user.getId())
        self.assertEqual(self.user.getId(), self.tokenRepo.getUserId(token).get())

if __name__ == '__main__':
    unittest.main()

