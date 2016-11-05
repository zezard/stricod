import unittest 

from repos import MongoUserRepo
from repos import MongoTokenRepo
from utils import Config
from .testdbinstance import MongoTestDbInstance

class TestUserRepo(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(Config.defaultTestConfig())):
        self.mdb = mdb
        self.userRepo = MongoUserRepo(self.mdb.getUserCollection())

    def tearDown(self):
        self.mdb.dropAll()

    def testCannotGetNonexistingUser(self):
        user = self.userRepo.getUser("-1")
        self.assertEqual(user, None)

    def testAddUser(self):
        uid = self.userRepo.addUser("foo","bar")
        self.assertNotEqual(uid, None)

        user = self.userRepo.getUser(uid)
        self.assertNotEqual(user, None)
        self.assertEqual(user.getName(), "foo")

    def testCannotAddExistingUser(self):
        uid1 = self.userRepo.addUser("foo","bar")
        uid2 = self.userRepo.addUser("foo","bar")
        self.assertEqual(uid2, None)
        uid3 = self.userRepo.addUser("foo","bar2")
        self.assertEqual(uid3, None)

class TestTokenRepo(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(Config.defaultTestConfig())):
        self.mdb = mdb 
        userRepo = MongoUserRepo(self.mdb.getUserCollection())
        uid = userRepo.addUser("foo","bar")
        self.user = userRepo.getUser(uid)
        self.tokenRepo = MongoTokenRepo(self.mdb.getTokenCollection())

    def tearDown(self):
        self.mdb.dropAll()

    def testAddToken(self):
        token = "just_a_stupid_token_string"
        self.tokenRepo.addToken(token, self.user.getId())
        self.assertEqual(self.user.getId(), self.tokenRepo.getUserId(token).get())

if __name__ == '__main__':
    unittest.main()

