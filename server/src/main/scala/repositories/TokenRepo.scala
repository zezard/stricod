package repositories

import Models.Token
import databases.MongoDbBackend
import reactivemongo.bson.{BSONDocument, Macros}

import scala.concurrent.Future

trait TokenRepoComponent {

  trait TokenRepo {
    def saveToken(token: String): Future[Unit]
    def findToken(token: String): Future[Option[Token]]
  }

  class MongoTokenRepo extends TokenRepo {
    private val mdb = MongoDbBackend


    import scala.concurrent.ExecutionContext.Implicits.global

    override def saveToken(token: String): Future[Unit] = {
      val document = BSONDocument("token" -> token)
      mdb.tokenCollection.flatMap(_.insert(document).map(_ => ()))
    }

    override def findToken(token: String): Future[Option[Token]] = {
      implicit def tokenWriter = Macros.reader[Token]
      val document = BSONDocument("token" -> token)
      mdb.tokenCollection.flatMap(_.find(document).one[Token])
    }
  }
}
