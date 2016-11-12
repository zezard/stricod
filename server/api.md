# API

The server stores location coordinates. Its API allows for storing and retrieving location data per user.
Please note that account credentials are sent as clear text and that your connection should be secured
with TLS or similar.

## Registering a user

Before authenticating a user must register.

```
HTTP-request: POST /user/add
HTTP-request data:
{
    username: "your-desired-username",
    password: "your-password"
}

HTTP-response status: 201 Created
HTTP-response status: 409 Conflict
```


## Authentication

Before accessing any API nodes a user has to authenticate.

```
HTTP-request: POST /user/auth
HTTP-request data:
{
    username: "your-username",
    password: "your-password"
}

HTTP-response status: 200 OK
HTTP-response data:
{
    token: "a token string used to access the user API"
}
HTTP-response status: 401 Unauthorized
```

Use the token in preceding calls by embedding it in the header to the user API.

## Storing location data

A user can store location data as Degrees, Seconds, Minutes data:

```
HTTP-request: POST /user/geodata
HTTP-request header:
{
    "userToken": "Your token here"
}
HTTP-request data:
{
    degrees: Int,
    minutes: Int,
    seconds, Int
}

HTTP-response status: 201 Created
HTTP-response data: {}
HTTP-response status: 401 Unauthorized
```

## Retrieving location data

A user can retrieve its last known location as Degrees, Seconds, Minutes data:

```
HTTP-request: GET /user/geodata
HTTP-request header:
{
"userToken": "Your token here"
}
HTTP-request data: {}

HTTP-response status: 200 OK
HTTP-response data: {
   degrees: Int, 
   minutes: Int, 
   seconds: Int, 
   timestamp: "2016-11-12T13:39:01+00:00"
}
HTTP-response status: 401 Unauthorized
```
