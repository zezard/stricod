import akka.event.NoLogging
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.model.ContentTypes._
import akka.http.scaladsl.model.{HttpResponse, HttpRequest}
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.testkit.ScalatestRouteTest
import akka.stream.scaladsl.Flow
import org.scalatest._

class ServiceSpec extends FlatSpec with Matchers with ScalatestRouteTest with Service {
  override def testConfigSource = "akka.loglevel = WARNING"
  override def config = testConfig
  override val logger = NoLogging

  it should "authenticate a valid user by username and password" in {
    Post(s"/auth", UserAuthRequest("tulvgard","foobar")) ~> routes ~> check {
      status shouldBe OK
    }
  }

  it should "allow to push geodata to authenticated user" in {
    Post(s"/user/geodata", PushGeodataRequest(9876, 1489, 9323)) ~> routes ~> check {
      status shouldBe OK
    }
  }
}
