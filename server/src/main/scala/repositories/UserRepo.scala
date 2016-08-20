package repositories

import databases.MongoDbBackend
import reactivemongo.bson.{BSONDocument, BSONDocumentReader, BSONObjectID}

import scala.concurrent.{ExecutionContext, Future}

trait UserRepoComponent {
  val userRepo: UserRepo

  trait UserRepo {
    case class User(username: String, password: String, id: String)
    def getUser(username: String, password: String): Future[Option[User]]
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

    override def getUser(username: String, password: String): Future[Option[User]] = {
      val query = BSONDocument("username" -> username, "password" -> password)
      for { user <- mdb.usersCollection.flatMap(_.find(query).one[User]) } yield user
    }
  }
}
