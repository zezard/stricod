from StricodDbInstance import StricodDbInstance 
from UserRepo import MongoUserRepo
from TokenRepo import MongoTokenRepo

mdb = StricodDbInstance()
userRepo = MongoUserRepo(mdb.getUserCollection())
userRepo.addUser("foo","bar")
user = userRepo.getUser("foo","bar")
print(user)

tokenRepo = MongoTokenRepo(mdb.getTokenCollection())
token = "just_a_stupid_token_string"
tokenRepo.addToken(token, user.getId())
print(tokenRepo.getUserId(token))
