Stricod game server
===================

## Dependencies

* *Python3* to run the server
* *Virtualenv* to create a local installation of the dependencies
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
PYTHONPATH=./ python3 -B -m unittest tests/reposuite.py
```
to execute the `reposuite` tests
