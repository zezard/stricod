import unittest

from services import TokenService, GeodataService
from repos import MongoGeodataRepo
from .testdbinstance import MongoTestDbInstance
from utils import defaultTestConfig

class TestTokenService(unittest.TestCase):

    def setUp(self):
        testConfig = defaultTestConfig()
        self.mdb = MongoTestDbInstance(testConfig)
        self.service = TokenService()

    def tearDown(self):
        self.mdb.dropAll()

    def testNewToken(t):
        token = t.service.newTokenFor(869301)
        t.assertIsNotNone(token)

    def testGetUserId(t):
        uid = 98979
        token = t.service.newTokenFor(uid)
        uidFromToken = t.service.getUserId(token)
        t.assertIsNotNone(uidFromToken)
        t.assertEqual(uid, uidFromToken)

class TestGeodataService(unittest.TestCase):

    def setUp(self):
        testConfig = defaultTestConfig()
        self.mdb = MongoTestDbInstance(testConfig)
        self.service = GeodataService(MongoGeodataRepo(self.mdb.getGeodataCollection()))

    def tearDown(self):
        self.mdb.dropAll()

    def testAddDmsPosition(t):
        uid = 8479
        ok = t.service.addDmsPosition(1,2,3, uid)
        t.assertTrue(ok)

    def testGetLastPosition(t):
        uid = 5902
        ok = t.service.addDmsPosition(1,2,3, uid)
        t.assertTrue(ok)
        pos = t.service.getLastPosition(uid)
        dms = pos.getDMS()
        t.assertEqual(dms['d'],1)
        t.assertEqual(dms['m'],2)
        t.assertEqual(dms['s'],3)

