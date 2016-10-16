enablePlugins(JavaAppPackaging)

name := "stricod-server"
organization := "com.stricod"
version := "0.1-rc1"
scalaVersion := "2.11.8"

scalacOptions := Seq("-unchecked", "-deprecation", "-encoding", "utf8")


libraryDependencies ++= {
  val akkaV       = "2.4.3"
  val scalaTestV  = "3.0.0"
  Seq(
    "com.typesafe.akka" %% "akka-actor" % akkaV,
    "com.typesafe.akka" %% "akka-stream" % akkaV,
    "com.typesafe.akka" %% "akka-http-experimental" % akkaV,
    "com.typesafe.akka" %% "akka-http-spray-json-experimental" % akkaV,
    "com.typesafe.akka" %% "akka-http-testkit" % akkaV,
    "org.slf4j" % "slf4j-log4j12" % "1.7.21",
    "org.scalatest"     %% "scalatest" % scalaTestV % "test",
    "org.reactivemongo" %% "reactivemongo" % "0.11.14",
    "com.pauldijou" %% "jwt-core" % "0.8.0"
  )
}

resolvers += "Typesafe repository releases" at "http://repo.typesafe.com/typesafe/releases/"
Revolver.settings
