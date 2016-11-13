from services import GeodataService, TokenService, UserService 
from repos import MongoGeodataRepo, MongoUserRepo
from db import MongoDbInstance
from utils import defaultTestConfig

import logging, json, functools




from flask import Flask, request, render_template
app = Flask(__name__)

global userService, tokenService, geodataService
mdb = MongoDbInstance()
userService = UserService(MongoUserRepo(mdb.getUserCollection()))
tokenService = TokenService()
geodataService = GeodataService(MongoGeodataRepo(mdb.getGeodataCollection()))

CONTENT_JSON = {'Content-Type': 'application/json'}

def getVersion():
    import subprocess
    label = subprocess.check_output(["git", "describe","--always"])
    return label.decode('utf-8')

def parseAddRequest(request):
    credentials = request.get_json()
    if not "username" in credentials.keys() or not "password" in credentials.keys(): return None
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
    if not request.headers.has_key("token"): return None
    tokenStr = request.headers["token"]
    global tokenService
    if not tokenService.isValid(tokenStr): return None
    else: return tokenService.getUserId(tokenStr)


###########################
# User API
#######################

@app.route('/user/add', methods=["POST"])
def addUser():
    try: username, password = parseAddRequest(request)
    except TypeError: return 'Invalid request',400
    global userService
    ok = userService.register(username, password)
    if not ok: return 'Username already exist', 409
    else:
        return 'User created', 201

@app.route('/user/auth', methods=["POST"])
def authUser():
    try: username, password = parseAddRequest(request)
    except TypeError: return 'Invalid request',400
    global userService
    user = userService.getUser(username, password)
    if not user: return 'Invalid credentials', 401
    else:
        return (json.dumps({"token":tokenService.newTokenFor(user.getId()).decode("utf-8")}),
            201,
            CONTENT_JSON)

###########################
# API level decorators
#######################

def login_required(fun):
    global tokenService

    def getUserToken(request):
        if not request.headers.has_key("token"):
            return abort(401)
        return request.headers["token"]

    def checkValid(tokenStr):
        try:
            if not tokenService.isValid(tokenStr): return False
            else: return True
        except Exception:
            return False


    @functools.wraps(fun)
    def decorated_function(*args, **kwargs):
        tokenStr = getUserToken(request)
        if not checkValid(tokenStr):
            return '',401
        else:
            return fun(tokenService.getUserId(tokenStr))
    return decorated_function

###########################
# Geodata API
#######################

@app.route('/user/geodata', methods=["POST"])
@login_required
def savePosition(uid):
    try: dms = parseSavePosition(request)
    except TypeError: return 'Invalid request',400
    if not dms: return 'Invlid request', 400
    if not geodataService.addDmsPosition(dms[0],dms[1],dms[2],uid): return '',500
    else:
        return '',201

@app.route('/user/geodata', methods=["GET"])
@login_required
def getLastPosition(uid):
    pos = geodataService.getLastPosition(uid)
    if not pos: return '{}',200
    else:
        return pos.toJSON(),200,CONTENT_JSON

###########################
# Root route 
#######################
@app.route("/")
def root():
    return render_template("status.html", gitVersion=getVersion(), msgs=memlog.get())

if __name__ == "__main__":
    app.run()
