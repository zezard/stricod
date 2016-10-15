package util

import com.typesafe.config.ConfigFactory

object Configurator {
  private val config  = ConfigFactory.load()
  def getConfig = config
  def httpHost = config.getString("http.interface")
  def httpPort= config.getInt("http.port")
  def dbHost = config.getString("mongo.host")
  def stricodDbName = config.getString("mongo.stricodDb")
  def geodataDbName = config.getString("mongo.geodataDb")
  def getSecurityKey = config.getString("security.key")
}
