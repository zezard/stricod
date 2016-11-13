import sys
import urllib3
import json

HTTP_CODES = {
    200: "Ok",
    201: "Created",
    400: "Bad request",
    401: "Unauthroized"
}

def getUrl(): 
    return  "http://localhost:5000"

def authedGet(pool, api_node, token):
    return pool.request(
            'GET', 
            getUrl()+api_node,
            headers={'token':token})

def post(pool, api_node, payload):
    return pool.request(
            'POST', 
            getUrl()+api_node, 
            headers={'Content-Type': 'application/json'}, 
            body=payload)

def authedPost(pool, api_node, token,  payload):
    return pool.request(
            'POST', 
            getUrl()+api_node, 
            headers={'Content-Type': 'application/json', 'token': token}, 
            body=payload)

def extractToken(req):
    decoded = req.data.decode('utf-8')
    contents = json.loads(decoded)
    if "token" in contents.keys():
        print("Extracted token: ",contents["token"])
        return contents["token"]
    else:
        raise Exception("Error: no token found")

def extractDms(req):
    decoded = req.data.decode('utf-8')
    contents = json.loads(decoded)
    return contents

def login(pool):
    
    payload = json.dumps({
        "username": input("Username: "), 
        "password": input("Password: ") 
    })

    return post(pool, "/user/auth", payload)


def register(pool):

    payload = json.dumps({
        "username": input("Username: "), 
        "password": input("Password: ") 
    })

    return post(pool, "/user/add", payload)

def getGeodata(pool, token):

    return authedGet(pool, "/user/geodata", token)

def saveGeodata(pool, token):

    payload = json.dumps({
        "degrees": int(input("degrees: ")), 
        "minutes": int(input("minutes: ")),
        "seconds": int(input("seconds: "))
    })

    return authedPost(pool, "/user/geodata", token, payload)

def usage():
    print("Usage:", sys.argv[0], "COMMAND [TOKEN]")
    print("COMMAND is any of:")
    print("\n".join(["\tlogin","\tregister","\tgetGeodata TOKEN\tsaveGeodata TOKEN"]))
    print("\nTOKEN is a token received from logging in")

if __name__ == "__main__":
    COMMAND_INDEX = 1
    TOKEN_INDEX = 2

    pool = urllib3.PoolManager()

    if len(sys.argv) < 2: 
        usage();  exit(1)

    if sys.argv[COMMAND_INDEX] == "login":
        req = login(pool)
        extractToken(req)

    elif sys.argv[COMMAND_INDEX] == "register":
        req = register(pool)

    elif sys.argv[COMMAND_INDEX] == "getGeodata":
        token = sys.argv[TOKEN_INDEX]
        req = getGeodata(pool, token)
        print(extractDms(req))

    elif sys.argv[COMMAND_INDEX] == "saveGeodata":
        token = sys.argv[TOKEN_INDEX]
        req = saveGeodata(pool, token)


    else:
        print("Error:", sys.argv[COMMAND_INDEX], "is not a command\n")
        usage()
        exit(1)


    if req.status in HTTP_CODES.keys():
        print("HTTP response code: ", req.status, HTTP_CODES[req.status])
    else:
        print("HTTP response code: ", req.status)


