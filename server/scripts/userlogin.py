import urllib2
import json

urly = "http://localhost:9000"
api_suffix = "/user/auth"

username = "tulvgard"
password = "foobar" 

payload = {
    "data": {
        "username": username, 
        "password": password
    },
    "Content-Type": "application/json"
}

request = urllib2.Request(urly+api_suffix, data=json.dumps(payload))
request.post()
