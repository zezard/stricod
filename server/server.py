from services import GeodataService, TokenService, UserService 
from repos import MongoGeodataRepo, MongoUserRepo
from db import MongoDbInstance
from utils import defaultTestConfig

import logging, json

from flask import Flask, request, g
app = Flask(__name__)

global userService, tokenService, geodataService
mdb = MongoDbInstance()
userService = UserService(MongoUserRepo(mdb.getUserCollection()))
tokenService = TokenService()
geodataService = GeodataService(MongoGeodataRepo(mdb.getGeodataCollection()))

def getVersion():
    import subprocess
    label = subprocess.check_output(["git", "describe","--always"])
    return label.decode('utf-8')

def parseAddRequest(request):
    credentials = request.get_json()
    username = credentials['username']
    password = credentials['password']
    if not username or not password:
        return None
    else:
        return (username,password)

def parseSavePosition(request):
    p = request.get_json()
    if not 'degrees' in p or not 'minutes' in p or not 'seconds' in p: return None
    d = p['degrees']; m = p['minutes']; s = p['seconds']
    if not d or not m or not s: return None
    else: return (d,m,s)

def authenticate(request):
    if not request.headers.has_key("userToken"): return None
    tokenStr = request.headers["userToken"]
    global tokenService
    if not tokenService.isValid(tokenStr): return None
    else: return tokenService.getUserId(tokenStr)


###########################
# User API
#######################

@app.route('/user/add', methods=["POST"])
def addUser():
    try: username, password = parseAddRequest(request)
    except TypeError: 'Invalid request',400
    global userService
    ok = userService.register(username, password)
    if not ok: return 'Username already exist', 409
    else: return 'User created', 201

@app.route('/user/auth', methods=["POST"])
def authUser():
    try: username, password = parseAddRequest(request)
    except TypeError: return 'Invalid request',400
    global userService
    user = userService.getUser(username, password)
    if not user: return 'Invalid credentials', 401
    else: return tokenService.newTokenFor(user.getId()),201



###########################
# Geodata API 
#######################

@app.route('/user/geodata', methods=["POST"])
def savePosition():
    try: uid = authenticate(request)
    except Exception as e: app.logger.debug(e); return 'Please login first', 401
    if not uid: return 'Please login first', 402

    try: dms = parseSavePosition(request)
    except TypeError: return 'Invalid request',400
    if not dms: return 'Invlid request', 400

    if not geodataService.addDmsPosition(dms[0],dms[1],dms[2],uid): return '',500
    else: return '',201

@app.route('/user/geodata', methods=["GET"])
def getLastPosition():
    try: uid = authenticate(request)
    except Exception: return 'Please login first', 401
    if not uid: return 'Please login first', 401
   
    pos = geodataService.getLastPosition(uid)
    if not pos: return '',200
    else: return pos.toJSON(),200,{'Content-Type': 'application/json'}
    

###########################
# Root route 
#######################

@app.route("/")
def root():
    return "Stricod version " + getVersion()

if __name__ == "__main__":
    app.run()
