Stricod server
==============

The stricod server provides an Akka HTTP API for storing and retreiving 
positional data. 

API
---

Refer to the API.md document.

Building and running
--------------------

To build the server you require 

* Scala (tested with JDK8)
* Simple Build Tool (SBT)
* Mongo DB

### From command-line

Move to the server root-directory and type `sbt compile`. If the build is 
successful type `sbt run`.

You can also run the test suites by typing `sbt test`.

### From IntelliJ

Afer installing the Scala plugin import the server-project. 
During import, you can choose to select "Use auto-import" to make 
IntelliJ update the sbt dependencies when you make a change. 

Build the project by selecting "Build" -> "Make Project" from the top menu.

If the build is successfull you can create an SBT task as a 
run-configuration and there execute the SBT-task `run`.

Select "Run" -> "Edit Configuations" -> "+" -> "SBT Task". Then in the "Tasks" 
input field, type `run` and name it to whatever you want.

You can also run the test suites by opening any suite, right-click 
and run the suite.
