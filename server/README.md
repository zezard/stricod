Stricod game server
===================

This is a simple game server for storing and retreiving game data from the 
game database. The server is configured for developing and testing Stricod.

The server is built to implement different databses although there 
is a default MongoDB implementation. Install MongoDB on your host 
to run the Stricod server locally for development.

## Project structure

```
.
|-- db                  Database instance implementations 
|-- models              Abstractions like Position, User and Token 
|-- repos               Database read and write abstractions
|-- services            Web service layer
|-- server.py           REST API router
|-- tests               
`-- utils               Usefull tools 
```

## Dependencies

* *Python3*
* *MongoDB*
* *Virtualenv* to create a local installation of the dependencies (optional)
* *pymongodb* (installed with pip, see below) for database access

## Installation

Create a virual environment with `virtualenv` called `end`
(you can name it whatever you like).
```
/path/to/stricod/server $: virtualenv -p python3 env
/path/to/stricod/server $: ./env/bin/activate
```

Install dependencies
```
/path/to/stricod/server $: pip install -r dependencies.txt 
```

## Running tests

Set the `PYTHONPATH` and call `unittest`. From the project root, run:
```
/path/to/stricod/server $: PYTHONPATH=./ python3 -B -m unittest tests/reposuite.py
```
to execute the `reposuite` tests. More tests are located in `tests` directory. 
