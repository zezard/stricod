import akka.actor.ActorSystem
import akka.event.NoLogging
import akka.http.javadsl.model
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.model.{HttpHeader, HttpRequest}
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.model.headers.RawHeader
import akka.http.scaladsl.server.RouteResult
import akka.http.scaladsl.testkit.{RouteTestTimeout, ScalatestRouteTest}
import org.scalatest._

import scala.concurrent.duration.DurationInt

class ServiceSpec extends FunSuite with Matchers with ScalatestRouteTest with Service {
  override def testConfigSource = "akka.loglevel = WARNING"
  override def config = testConfig
  override val logger = NoLogging
  implicit def default(implicit system: ActorSystem) = RouteTestTimeout(new DurationInt(5).second)

  private def getUserToken(username: String, password: String): String = {
    Post("/user/auth", UserAuthRequest("tulvgard","foobar")) ~> routes ~> check {
      status shouldBe OK
      responseAs[UserAuthResponse].token
    }
  }

  private def authorizedRequest(request: HttpRequest, token: String): RouteTestResult = {
    val tokenHeader = RawHeader("userToken",token)
    request.addHeader(tokenHeader) ~> routes
  }

  test("should authenticate a valid account by username and password") {
    Post("/user/auth", UserAuthRequest("tulvgard","foobar")) ~> routes ~> check {
      val authToken = responseAs[UserAuthResponse]
      status shouldBe OK
    }
  }

  test("should not authenticate an invalid account") {
    Post(s"/user/auth", UserAuthRequest("tulvgard","notsofoo")) ~> routes ~> check {
      status shouldBe Unauthorized
    }
  }

  test("should not allow to push geodata to authenticated user") {
    authorizedRequest(Post(s"/user/geodata", PushGeodataRequest(9876, 1489, 9323)), "{}") ~> check {
      status shouldBe Unauthorized
    }
  }

  test("should allow to push geodata to authenticated user") {
    val token = getUserToken("tulvgard","foobar")
    authorizedRequest(Post(s"/user/geodata", PushGeodataRequest(9876, 1489, 9323)), token) ~> check {
      status shouldBe Created
    }
  }

  test("should allow to fetch geodata for authenticated user")  {
    val token = getUserToken("tulvgard", "foobar")
    authorizedRequest(Get("/user/geodata", GeoDataByUserIdRequest("57a47592807f07ed0bd17a60")), token) -> check {
      status shouldBe OK
      val coordinates = responseAs[Seq[GeoDataByUserIdResponse]]
      assert(coordinates.length > 0)
    }
  }

}
