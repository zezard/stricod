package util

import com.typesafe.config.ConfigFactory

object Configurator {
  private val config  = ConfigFactory.load()
  def getConfig = config
  def httpHost = config.getString("http.interface")
  def httpPort= config.getInt("http.port")
  def dbHost = config.getString("mongo.host")
  def dbPort = config.getString("mongo.port")
  def stricodDbName = config.getString("mongo.stricodDb")
  def geodataDbName = config.getString("mongo.geodataDb")
  def testStricodDbName = config.getString("mongo.test.stricodDb")
  def testGeodataDbName = config.getString("mongo.test.geodataDb")
}
