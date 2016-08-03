package services

import java.util.UUID

import repositories.UserRepoComponent

import scala.concurrent.{ExecutionContext, Future}

object generateToken {
  def apply(unique: String) = UUID.randomUUID.toString
}

trait UserServiceComponent extends UserRepoComponent {
  val userService: UserService

  override val userRepo = new RamUserRepo

  trait UserService {
    def authenticate (username: String, password: String): Either[String, String]
  }
  class UserServiceImpl extends UserService {
    override def authenticate(username: String, password: String) = {
      userRepo.getUser(username, password) match {
        case Some(user) => Right(generateToken(username))
        case None => Left(s"No user found $username")
      }
    }
  }
}
