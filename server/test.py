from StricodDbInstance import StricodDbInstance 
from UserRepo import MongoUserRepo
from TokenRepo import MongoTokenRepo

mdb = StricodDbInstance()
userRepo = MongoUserRepo(mdb.getUserCollection())
print(userRepo.getUser("foo","IdKpsV/K0ALbeD26T0/DQA=="))

tokenRepo = MongoTokenRepo(mdb.getTokenCollection())
print(tokenRepo.getUserId("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.NTgwMmExZmEzOWRmYTAzMWVkNzdlNzYz.1sKiHQYWFS-ZnOW2H2xREA53kWec48zKOIobjL1ybas"))
