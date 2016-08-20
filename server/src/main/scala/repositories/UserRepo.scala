package repositories

import reactivemongo.api._
import reactivemongo.api.collections.bson.BSONCollection
import reactivemongo.bson.{BSONDocument, BSONDocumentReader, Macros, document}

import scala.concurrent.{Await, ExecutionContext, Future}
import scala.concurrent.duration._
import scala.util.{Failure, Success}

trait UserRepoComponent {
  val userRepo: UserRepo

  trait UserRepo {
    case class User(username: String, password: String, id: Long)
    def getUser(username: String, password: String): Future[Option[User]]
  }

  class MongoDbUserRepo extends UserRepo {
    import scala.concurrent.ExecutionContext.Implicits.global
    private val host = "localhost"
    private val port = 27017
    private val dbName = "stricod"
    private val mongoUri = s"mongodb://$host:$port/$dbName"
    private val driver = new MongoDriver()
    private val connection  = driver.connection(List("localhost"))

    private def getDb = connection.database(dbName)
    private def usersCollection: Future[BSONCollection] = getDb.map(_.collection("users"))

    implicit def userReader: BSONDocumentReader[User] = Macros.reader[User]
    override def getUser(username: String, password: String): Future[Option[User]] = {
      val query = BSONDocument("username" -> username, "password" -> password)
      for {
        doc <- usersCollection.flatMap(_.find(query).one[BSONDocument])
      } yield doc match {
        case Some(u) => Some(User(username = u.getAs[String]("username").getOrElse(""), password = u.getAs[String]("password").getOrElse(""), id = 0))
        case None => None
      }
    }
  }


  class RamUserRepo extends UserRepo {
    import ExecutionContext.Implicits.global
    var userDb = scala.collection.mutable.ListBuffer.empty[User]
    userDb += User("ztinker","foobar",1)
    userDb += User("tednoob","foobar",2)
    userDb += User("tulvgard","foobar",3)

    override def getUser(username: String, password: String) = Future(userDb.find(u => (u.username == username && u.password == password)))
  }
}
