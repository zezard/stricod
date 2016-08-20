package services

import java.util.UUID

import repositories.UserRepoComponent

import scala.concurrent.Future
import scala.util.{Failure, Success}

object generateToken {
  def apply(unique: String) = UUID.randomUUID.toString
}

trait UserServiceComponent extends UserRepoComponent {
  val userService: UserService

  override val userRepo = new MongoDbUserRepo

  trait UserService {
    def authenticate (username: String, password: String): Future[Either[String, String]]
  }

  class UserServiceImpl extends UserService {

    import scala.concurrent.ExecutionContext.Implicits.global

    override def authenticate(username: String, password: String) = userRepo.getUser(username, password) flatMap { u => u match {
      case Some(u) => Future { Right(generateToken(username)) }
      case None => Future { Left(s"No user found $username") }
    }}
  }
}
