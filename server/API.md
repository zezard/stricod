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
```

Use the token in preceding calls by embedding it in the header to the user API.

## Storing location data

A user can store location data as Degrees, Seconds, Minutes data:

```
HTTP-request: POST /user/geodata
HTTP-request data:
{
    degrees: Int,
    minutes: Int,
    seconds, Int
}
HTTP-response status: 201 Created
HTTP-response data: {}
```

## Retrieving location data

A user can retrieve the last 30 location entries as Degrees, Seconds, Minutes data:

```
HTTP-request: GET /user/geodata
HTTP-request data: {}
HTTP-response status: 200 OK
HTTP-response data: {
    [
        {degrees: Int, minutes: Int, seconds: Int},
        {degrees: Int, minutes: Int, seconds: Int},
        ...
        {degrees: Int, minutes: Int, seconds: Int}
    ]
}
```
