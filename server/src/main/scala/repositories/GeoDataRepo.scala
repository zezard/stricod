package repositories

import Models.{GeoData, Token}
import databases.MongoDbBackend
import reactivemongo.bson.{BSONDateTime, BSONDocument, BSONDocumentReader, BSONObjectID, Macros}

import scala.concurrent.Future

trait GeoDataRepoComponent {

  case class Foo(_id: BSONObjectID, userId: BSONObjectID, timestamp: BSONDateTime, geodata: GeoData)
  trait GeoDataRepo {
    def saveGeodata(token: String): Future[Unit]
    def getGeoData(userId: String): Future[Seq[Foo]]
  }

  class MongoGeoDataRepo extends GeoDataRepo {
    private val mdb = MongoDbBackend
    private val defaultNumberOfGeoDatas = 30

    import scala.concurrent.ExecutionContext.Implicits.global
    implicit def geoDataWriter = Macros.writer[GeoData]
    implicit def geoDataReader = Macros.reader[GeoData]

    override def saveGeodata(token: String): Future[Unit] = ???


    override def getGeoData(userId: String): Future[Seq[Foo]] = {

      implicit def geoDataReader = Macros.reader[GeoData]
      implicit object FooReader extends BSONDocumentReader[Foo] {
        def read(bson: BSONDocument): Foo = {
          val dId = bson.getAs[BSONObjectID]("_id").get
          val userId = bson.getAs[BSONObjectID]("userId").get
          val timestamp = bson.getAs[BSONDateTime]("timestamp").get
          val geodata = bson.getAs[GeoData]("geodata").get
          Foo(dId, userId, timestamp, geodata)
        }
      }
      val query = BSONDocument("userId" -> BSONObjectID(userId))
      //val projection = BSONDocument("geodata" -> 1)
      mdb.geoDataCollection flatMap {
        _.find(query).cursor[Foo]().collect[Seq](defaultNumberOfGeoDatas)
      }
      //mdb.geoDataCollection flatMap { _.find(query, projection).cursor[GeoData]().collect[Seq](defaultNumberOfGeoDatas) }
    }
  }
}
