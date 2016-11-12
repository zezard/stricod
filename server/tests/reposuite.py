import unittest 

from repos import MongoUserRepo, MongoGeodataRepo
from utils import defaultTestConfig 
from .testdbinstance import MongoTestDbInstance

class TestUserRepo(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(defaultTestConfig())):
        self.mdb = mdb
        self.userRepo = MongoUserRepo(self.mdb.getUserCollection())

    def tearDown(self):
        self.mdb.dropAll()

    def testCannotGetNonexistingUser(self):
        user = self.userRepo.getUserById("-1")
        self.assertEqual(user, None)

    def testAddUser(self):
        uid = self.userRepo.addUser("foo","bar")
        self.assertNotEqual(uid, None)

        user = self.userRepo.getUserById(uid)
        self.assertNotEqual(user, None)
        self.assertEqual(user.getName(), "foo")

    def testCannotAddExistingUser(self):
        uid1 = self.userRepo.addUser("foo","bar")
        uid2 = self.userRepo.addUser("foo","bar")
        self.assertEqual(uid2, None)
        uid3 = self.userRepo.addUser("foo","bar2")
        self.assertEqual(uid3, None)

from models import position 
class TestGeodataRepo(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(defaultTestConfig())):
        self.mdb = mdb
        self.repo = MongoGeodataRepo(self.mdb.getGeodataCollection())

        userRepo = MongoUserRepo(self.mdb.getUserCollection())
        uid = userRepo.addUser("foo","bar")
        self.user = userRepo.getUserById(uid)

    def tearDown(self):
        self.mdb.dropAll()

    def testAddGeodata(self):
        pos = position.fromDMS(123,456,789)
        ok = self.repo.addPosition(pos, self.user.getId())
        self.assertTrue(ok)
        dms = self.repo.getLastPosition(self.user.getId())
        self.assertIsNotNone(dms)


if __name__ == '__main__':
    unittest.main()

