package services

import java.util.UUID

import akka.http.scaladsl.model.HttpRequest
import akka.http.scaladsl.server.{Directive, Directive0, Directive1, RequestContext}
import pdi.jwt.{Jwt, JwtAlgorithm}
import repositories.{TokenRepoComponent, UserRepoComponent}

import scala.concurrent.Future
import scala.util.{Failure, Success}



trait UserServiceComponent extends UserRepoComponent {
  val userService: UserService

  override val userRepo = new MongoDbUserRepo

  case class UserSession(username: String)

  trait UserService {
    def authenticate (username: String, password: String): Future[Option[String]]
  }

  class UserServiceImpl extends UserService with TokenRepoComponent
  {

    val tokenRepo = new MongoTokenRepo
    import scala.concurrent.ExecutionContext.Implicits.global
    private val notSoSecretKey = "vahzaiVeisaiS0Quujal"

    def generateToken(contents: String) = {
      val newToken = Jwt.encode(s"""$contents""", notSoSecretKey, JwtAlgorithm.HS256)
      tokenRepo.saveToken(newToken)
      newToken
    }

    def authenticator(token: String): Option[UserSession]= {
      Jwt.decode(token, notSoSecretKey, Seq(JwtAlgorithm.HS256)) match {
        case Success(userToken) => Some(UserSession(userToken))
        case Failure(_) => None
      }
    }

    def validateToken(req: HttpRequest): Option[UserSession] = {
      val userToken = req.headers.find(header => header.name() == "userToken")
      userToken match {
        case Some(token) => authenticator(token.value())
        case None => None
      }
    }

    override def authenticate(username: String, password: String) = userRepo.getUser(username, password) flatMap { u => u match {
      case Some(u) => Future.successful(Some(generateToken(s"""{"username":"$username"}""")))
      case None => Future.successful(None)
    }}

    def saveGeodata(userId: String, degrees: Int, minutes: Int, seconds: Int) = userRepo.saveGeodata(userId, degrees, minutes, seconds)
  }
}
