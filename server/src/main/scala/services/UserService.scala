package services

import java.util.UUID

import Models.{GeoData, User}
import akka.http.scaladsl.model.HttpRequest
import akka.http.scaladsl.server.{Directive, Directive0, Directive1, RequestContext}
import pdi.jwt.{Jwt, JwtAlgorithm}
import repositories.{GeoDataRepoComponent, TokenRepoComponent, UserRepoComponent}

import scala.concurrent.Future
import scala.util.{Failure, Success}



trait UserServiceComponent extends UserRepoComponent {
  val userService: UserService

  override val userRepo = new MongoDbUserRepo

  case class UserSession(userId: String)

  trait UserService {
    def authenticate (username: String, password: String): Future[Option[String]]
  }

  class UserServiceImpl extends UserService with TokenRepoComponent with GeoDataRepoComponent
  {

    val tokenRepo = new MongoTokenRepo
    val geoDataRepo = new MongoGeoDataRepo

    import scala.concurrent.ExecutionContext.Implicits.global
    private val notSoSecretKey = "vahzaiVeisaiS0Quujal"

    def generateToken(user: User) = {
      val newToken = Jwt.encode(user.id, notSoSecretKey, JwtAlgorithm.HS256)
      tokenRepo.saveToken(newToken)
      newToken
    }

    def authenticator(token: String): Option[UserSession]= {
      Jwt.decode(token, notSoSecretKey, Seq(JwtAlgorithm.HS256)) match {
        case Success(userToken) => Some(UserSession(userToken))
        case Failure(_) => None
      }
    }

    def getToken(req: HttpRequest): Option[String] = {
      val userToken = req.headers.find(header => header.name() == "userToken")
      userToken match {
        case Some(token) => Some(token.value())
        case None => None
      }
    }

    def validateToken(token: String): Option[UserSession] = {
      authenticator(token)
    }

    override def authenticate(username: String, password: String) = userRepo.getUser(username, password) flatMap { u => u match {
      case Some(u) => Future.successful(Some(generateToken(u)))
      case None => Future.successful(None)
    }}

    def saveGeodata(userId: String, degrees: Int, minutes: Int, seconds: Int) = userRepo.saveGeodata(userId, GeoData(degrees, minutes, seconds))
    def getGeodata(userId: String): Future[Seq[GeoData]] = {
      geoDataRepo.getGeoData(userId) flatMap { gd => gd match {
          case Nil => Future.successful(Seq())
          case geoData: Seq[Foo] => Future.successful(geoData.map(e => e.geodata))
        }
      }
    }
  }
}
