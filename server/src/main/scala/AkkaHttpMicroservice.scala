import Models.GeoData
import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.server.Route
import akka.http.scaladsl.server.Directives._
import akka.stream.{ActorMaterializer, Materializer}
import com.typesafe.config.{Config, ConfigFactory}
import services.UserServiceComponent

import scala.concurrent.ExecutionContextExecutor
import spray.json.DefaultJsonProtocol
import util.Configurator

case class UserAuthRequest(username: String, password: String)
case class UserAuthResponse(token: String)
case class PushGeodataRequest(degrees: Int, minutes: Int, seconds: Int)
case class GeoDataByUserIdRequest(userId: String)
case class GeoDataByUserIdResponse(degrees: Int, minutes: Int, seconds: Int)

trait Protocols extends DefaultJsonProtocol {
  implicit val userAuthRequest = jsonFormat2(UserAuthRequest.apply)
  implicit val userAuthResponse = jsonFormat1(UserAuthResponse.apply)
  implicit val pushGeodataRequest = jsonFormat3(PushGeodataRequest.apply)
  implicit val geoDataByUserIdResponse = jsonFormat3(GeoDataByUserIdResponse.apply)
}

trait Service extends Protocols with UserServiceComponent {
  implicit val system: ActorSystem
  implicit def executor: ExecutionContextExecutor
  implicit val materializer: Materializer

  val userService = new UserServiceImpl

  def config: Config
  val logger: LoggingAdapter

  private def checkUserAuth(tokenField: Option[String], protectedRoutes: (UserSession => Route)) = {
    tokenField match {
      case None => complete(Unauthorized, "Invalid credentials")
      case Some(token) => {
        userService.authenticator(token) match {
          case None => complete(Unauthorized, "Invalid credentials")
          case Some(user) => protectedRoutes(user)
        }
      }
    }
  }

  val routes = extractRequest { req =>
    logRequestResult("akka-http-microservice") {
      pathPrefix("user") {
        (path("auth") & post & entity(as[UserAuthRequest])) { authReq =>
          onSuccess(userService.authenticate(authReq.username, authReq.password)) {
            case Some(newToken) => complete(OK, UserAuthResponse(newToken))
            case None => complete(Unauthorized, "Invalid credentials")
          }
        } ~
        path("geodata") {
          checkUserAuth(userService.getToken(req), { user =>
            (post & entity(as[PushGeodataRequest])) { geodata =>
              userService.saveGeodata(user.userId, geodata.degrees, geodata.minutes, geodata.seconds)
              complete(Created)
            } ~
            get {
              onSuccess(userService.getGeodata(user.userId)) {
                case Nil => complete(OK, "")
                case coordinates: Seq[GeoData] => complete(OK, coordinates.map(c => GeoDataByUserIdResponse(c.degrees, c.minutes, c.seconds)))
              }
            }
          })
        }
      }
    }
  }
}


object AkkaHttpMicroservice extends App with Service {
  override implicit val system = ActorSystem()
  override implicit val executor = system.dispatcher
  override implicit val materializer = ActorMaterializer()

  override val logger = Logging(system, getClass)
  override val config = Configurator.getConfig

  Http().bindAndHandle(routes, Configurator.httpHost, Configurator.httpPort)
}
