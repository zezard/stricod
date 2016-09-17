package repositories

import Models.{GeoData, User}
import databases.MongoDbBackend
import reactivemongo.bson.{BSONDateTime, BSONDocument, BSONDocumentReader, BSONDocumentWriter, BSONObjectID, BSONTimestamp, Macros}

import scala.concurrent.{ExecutionContext, Future}

trait UserRepoComponent {
  val userRepo: UserRepo

  trait UserRepo {

    def getUser(username: String, password: String): Future[Option[User]]
    def saveGeodata(userId: String, geoData: GeoData): Unit
  }

  class MongoDbUserRepo extends UserRepo {

    import ExecutionContext.Implicits.global

    private val mdb = MongoDbBackend

    implicit object UserReader extends BSONDocumentReader[User] {
      override def read(doc: BSONDocument): User = User(
        username = doc.getAs[String]("username").get,
        password = doc.getAs[String]("password").get,
        id = doc.getAs[BSONObjectID]("_id").get.stringify
      )
    }

    implicit def geoDataWriter: BSONDocumentWriter[GeoData] = Macros.writer[GeoData]

    override def getUser(username: String, password: String): Future[Option[User]] = {
      val query = BSONDocument("username" -> username, "password" -> password)
      for { user <- mdb.usersCollection.flatMap(_.find(query).one[User]) } yield user
    }

    def saveGeodata(userId: String, geoData: GeoData) = {
      val document = BSONDocument(
        "userId" -> BSONObjectID(userId),
        "timestamp" -> BSONDateTime(System.currentTimeMillis()),
        "geodata" -> geoData
      )
      mdb.geoDataCollection flatMap { _.insert(document).map(_ => {}) }
    }
  }
}
