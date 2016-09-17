package databases

import reactivemongo.api.MongoDriver
import reactivemongo.api.collections.bson.BSONCollection

import scala.concurrent.Future

object MongoDbBackend {
    import scala.concurrent.ExecutionContext.Implicits.global
    private val host = "localhost"
    private val dbName = "stricod"
    private val geoDbName = "geodata"
    private val driver = new MongoDriver()
    private val connection  = driver.connection(List(host))

    private def getDb = connection.database(dbName)
    private def getGeoDb = connection.database(geoDbName)

    def geoDataCollection: Future[BSONCollection] = getGeoDb.map(_.collection("dms"))
    def usersCollection: Future[BSONCollection] = getDb.map(_.collection("users"))
    def tokenCollection: Future[BSONCollection] = getDb.map(_.collection("tokens"))

}
