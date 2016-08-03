package repositories

import java.io._

trait UserRepoComponent {
  val userRepo: UserRepo

  trait UserRepo {
    case class User(username: String, password: String, id: Long)
    def getUser(username: String, password: String): Option[User]
    def dump()
  }

  class RamUserRepo extends UserRepo {
    var userDb = scala.collection.mutable.ListBuffer.empty[User]
    userDb += User("ztinker","foobar",1)
    userDb += User("tednoob","foobar",2)
    userDb += User("tulvgard","foobar",3)

    override def getUser(username: String, password: String) = userDb.find(u => (u.username == username && u.password == password))
    override def dump() = {
      new java.io.PrintWriter(new File("userDb.csv")) {
        val dbDump = userDb.map(u => u.username + "," + u.password + "," + u.id).mkString("\n")
        write(dbDump)
        close
      }
    }
  }
}
