import akka.actor.ActorSystem
import akka.event.NoLogging
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.model.HttpRequest
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.model.headers.RawHeader
import akka.http.scaladsl.testkit.{RouteTestTimeout, ScalatestRouteTest}
import org.scalatest._
import reactivemongo.api.MongoDriver
import util.Configurator

import scala.concurrent.duration.DurationInt

class ServiceSpec extends FunSuite
  with Matchers
  with BeforeAndAfterAll
  with ScalatestRouteTest with Service {
  override def testConfigSource = "akka.loglevel = WARNING"
  override def config = testConfig
  override val logger = NoLogging
  implicit def default(implicit system: ActorSystem) = RouteTestTimeout(new DurationInt(5).second)

  case class TestUser(username: String, password: String)

  val user1 = TestUser("Gustav Vasa", "Regalskepp")

  override def beforeAll = {
    userService.addUser(user1.username, user1.password)
  }

  override def afterAll = {
    val host = Configurator.dbHost
    val driver = new MongoDriver()
    val connection  = driver.connection(List(host))
    val dbname = Configurator.stricodDbName
    connection.database(Configurator.stricodDbName).map(_.drop())
    connection.database(Configurator.geodataDbName).map(_.drop())
  }

  private def getUserToken(username: String, password: String): String = {
    Post("/user/auth", UserAuthRequest(username, password)) ~> routes ~> check {
      status shouldBe OK
      responseAs[UserAuthResponse].token
    }
  }

  private def authorizedRequest(request: HttpRequest, token: String): RouteTestResult = {
    val tokenHeader = RawHeader("userToken",token)
    request.addHeader(tokenHeader) ~> routes
  }

  test("should authenticate a valid account by username and password") {
    getUserToken(user1.username, user1.password)
  }

  test("should not authenticate an invalid account") {
    Post("/user/auth", UserAuthRequest("Christan","Tyrann")) ~> routes ~> check {
      status shouldBe Unauthorized
    }
  }

  test("should not create new users with identifal username") {
    Post("/user/add", UserAuthRequest(user1.username, user1.password)) ~> routes ~> check {
      status shouldBe Conflict
    }
  }

  test("should not allow to push geodata to authenticated user") {
    authorizedRequest(Post("/user/geodata", PushGeodataRequest(9876, 1489, 9323)), "{}") ~> check {
      status shouldBe Unauthorized
    }
  }

  test("should allow to push geodata to authenticated user") {
    val token = getUserToken(user1.username, user1.password)
    authorizedRequest(Post("/user/geodata", PushGeodataRequest(9876, 1489, 9323)), token) ~> check {
      status shouldBe Created
    }
  }

  test("should not allow to fetch geodata for authenticated user") {
    val nonValidToken = "not4v4l1dt0k3n"
    authorizedRequest(Get("/user/geodata"), nonValidToken) -> check {
      status shouldBe Unauthorized
    }
  }

  test("should allow to fetch geodata for authenticated user")  {
    val token = getUserToken(user1.username, user1.password)
    authorizedRequest(Get("/user/geodata"), token) -> check {
      status shouldBe OK
      val coordinates = responseAs[Seq[GeoDataByUserIdResponse]]
      assert(coordinates.length > 0)
    }
  }

}
