import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.http.scaladsl.client.RequestBuilding
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.marshalling.ToResponseMarshallable
import akka.http.scaladsl.model.{HttpRequest, HttpResponse}
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.unmarshalling.Unmarshal
import akka.stream.{ActorMaterializer, Materializer}
import com.typesafe.config.Config
import com.typesafe.config.ConfigFactory

import services.UserServiceComponent

import scala.concurrent.ExecutionContextExecutor
import spray.json.DefaultJsonProtocol

case class UserAuthRequest(username: String, password: String)
case class UserAuthResponse(token: String)

trait Protocols extends DefaultJsonProtocol {
  implicit val userAuthRequest = jsonFormat2(UserAuthRequest.apply)
  implicit val userAuthResponse = jsonFormat1(UserAuthResponse.apply)
}

trait Service extends Protocols with UserServiceComponent {
  implicit val system: ActorSystem
  implicit def executor: ExecutionContextExecutor
  implicit val materializer: Materializer

  val userService = new UserServiceImpl

  def config: Config
  val logger: LoggingAdapter

  val routes = {
    logRequestResult("akka-http-microservice") {
      (path("auth") & post & entity(as[UserAuthRequest])) { req =>
        userService.authenticate(req.username, req.password) match {
          case Right(token) => complete((OK, token))
          case Left(errorMessage) => complete(Unauthorized, errorMessage)
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
