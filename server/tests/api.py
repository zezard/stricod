from .testdbinstance import MongoTestDbInstance
from utils import defaultTestConfig
import urllib
from urllib import request 
import json
import unittest

BASE_URL="http://localhost:5000"
TIMEOUT=10
json_header={"Content-Type":"application/json"}

def post(api,payload,token=None):
    if token: H = {**json_header, **{"userToken":token}}
    else: H = json_header
    req = request.Request(BASE_URL+api,
            data=payload,
            headers=H)
    return request.urlopen(req, timeout=TIMEOUT)

def get(api, token=None):
    if token: H = {"userToken":token}
    else: H = None
    req = request.Request(BASE_URL+api, headers=H)
    return request.urlopen(req, timeout=TIMEOUT)

def toData(d):
    return json.dumps(d).encode("utf-8")

class TestAddUser(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(defaultTestConfig())):
        self.mdb = mdb

    def tearDown(self):
        self.mdb.dropAll()

    def testShouldAddUser(t):
        res = post("/user/add",
                toData({"username":"test","password":"test"}))
        t.assertEqual(res.status, 201)

    def testShouldNotAddDuplicate(t):
        try:
            res = post("/user/add",
                    toData({"username":"test","password":"test"}))
        except urllib.error.HTTPError as e:
            t.assertEqual(e.code, 409)

class TestAuthentication(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(defaultTestConfig())):
        self.mdb = mdb
        self.username = "MrFoo"
        self.password = "suchBar"
        res = post("/user/add",
                toData({"username":self.username,"password":self.password}))

    def tearDown(self):
        self.mdb.dropAll()
    
    def testShouldAuthenticate(t):
        res = post("/user/auth",
                toData({"username":t.username,"password":t.password}))
        t.assertEqual(res.status, 201)
        tokenStr = res.read().decode("utf-8")

    def testShouldNotAuthenticate(t):
        try:
            res = post("/user/auth",
                    toData({"username":t.username+"1","password":t.password+"1"}))
        except urllib.error.HTTPError as e:
            t.assertEqual(e.code, 401)

class TestGeodataApi(unittest.TestCase):

    def setUp(self, mdb = MongoTestDbInstance(defaultTestConfig())):
        self.mdb = mdb
        self.username = "MrFoo"
        self.password = "suchBar"
        post("/user/add",
            toData({"username":self.username,"password":self.password}))
        res = post("/user/auth",
                toData({"username":self.username,"password":self.password}))
        self.token = res.read().decode("utf-8")

    def tearDown(self):
        self.mdb.dropAll()

    def testShouldSavePosition(t):
        res = post("/user/geodata",
                toData({"degrees":1,"minutes":2,"seconds":3}),
                token=t.token)
        t.assertEqual(res.status, 201)

    def testShouldGetLastPosition(t):
        res = post("/user/geodata",
                toData({"degrees":1,"minutes":2,"seconds":3}),
                token=t.token)
        t.assertEqual(res.status, 201)
        res = get("/user/geodata", token=t.token)
        t.assertEqual(res.status, 200)
        js = json.loads(res.read().decode("utf-8"))

        t.assertEqual(js["degrees"], 1)
        t.assertEqual(js["minutes"], 2)
        t.assertEqual(js["seconds"], 3)
        t.assertTrue("timestamp" in js.keys())
