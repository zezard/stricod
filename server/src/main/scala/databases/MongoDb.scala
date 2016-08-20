package databases

import reactivemongo.api.MongoDriver
import reactivemongo.api.collections.bson.BSONCollection

import scala.concurrent.Future

object MongoDbBackend {
    import scala.concurrent.ExecutionContext.Implicits.global
    private val host = "localhost"
    private val dbName = "stricod"
    private val driver = new MongoDriver()
    private val connection  = driver.connection(List(host))

    private def getDb = connection.database(dbName)
    def usersCollection: Future[BSONCollection] = getDb.map(_.collection("users"))
    def geoDataCollection: Future[BSONCollection] = getDb.map(_.collection("geodata"))

}
