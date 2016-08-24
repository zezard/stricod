import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.http.scaladsl.client.RequestBuilding
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.server.Directives._
import akka.stream.{ActorMaterializer, Materializer}
import com.typesafe.config.Config
import com.typesafe.config.ConfigFactory
import services.UserServiceComponent

import scala.concurrent.ExecutionContextExecutor
import spray.json.DefaultJsonProtocol

case class UserAuthRequest(username: String, password: String)
case class UserAuthResponse(token: String)
case class PushGeodataRequest(degrees: Int, minutes: Int, seconds: Int)

trait Protocols extends DefaultJsonProtocol {
  implicit val userAuthRequest = jsonFormat2(UserAuthRequest.apply)
  implicit val userAuthResponse = jsonFormat1(UserAuthResponse.apply)
  implicit val pushGeodataRequest = jsonFormat3(PushGeodataRequest.apply)
}

trait Service extends Protocols with UserServiceComponent {
  implicit val system: ActorSystem
  implicit def executor: ExecutionContextExecutor
  implicit val materializer: Materializer

  val userService = new UserServiceImpl

  def config: Config
  val logger: LoggingAdapter

  val routes = extractRequest { req =>
    logRequestResult("akka-http-microservice") {
      pathPrefix("user") {
        (path("auth") & post & entity(as[UserAuthRequest])) { authReq =>
          onSuccess(userService.authenticate(authReq.username, authReq.password)) {
            case Some(newToken) => complete(OK, UserAuthResponse(newToken))
            case None => complete(Unauthorized, "Invalid credentials")
          }
        } ~
        (path("geodata") & post & entity(as[PushGeodataRequest])) { geodata =>
          userService.validateToken(req) match {
            case Some(userToken) => {
              userService.saveGeodata("57a47592807f07ed0bd17a60", geodata.degrees, geodata.minutes, geodata.seconds)
              complete(Created)
            }
            case None => complete(Unauthorized, "Invalid credentials")
          }
        }
      }
    }
  }
}


object AkkaHttpMicroservice extends App with Service {
  override implicit val system = ActorSystem()
  override implicit val executor = system.dispatcher
  override implicit val materializer = ActorMaterializer()

  override val config = ConfigFactory.load()
  override val logger = Logging(system, getClass)

  Http().bindAndHandle(routes, config.getString("http.interface"), config.getInt("http.port"))
}
