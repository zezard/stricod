Stricod server
==============

The stricod server provides an Akka HTTP API for storing and retreiving 
positional data. 

API
---

Please refer to the tests for additional information.

Building and running
--------------------

To build the server you require 

* Scala
* Simple Build Tool (SBT)
* Mongo DB

### From command-line

Move to the server root-directory and type `sbt compile`. If the build is 
successful type `sbt run`.

You can also run the test suites by typing `sbt test`.

### From IntelliJ

Afer installing the Scala and SBT-plugins simple build the project from the 
menu. If the build is successfull you can create an SBT task as a 
run-configuration and there execute the SBT-task `run`.

You can also run the test suites by opening any suite, right-click and run 
the suite.
