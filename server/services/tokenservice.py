import jwt
import time

from utils import defaultConfig

class TokenService:
    def __init__(self, config=defaultConfig()):
        self._config = config
        self._validPeriod = 1000 * 60 * 60 * 24 * 1 # valid for one day

    def timeMillis(self): return int(round(time.time() * 1000))

    def newTokenFor(self, uid):
        expireDate = self.timeMillis() + self._validPeriod
        payload = {'uid':uid, 'exp': expireDate}
        if not payload: return None
        else: return jwt.encode(payload, self._config.getJwtSecret(), algorithm='HS256')

    def getUserId(self, tokenStr):
        payload = jwt.decode(tokenStr, self._config.getJwtSecret(), algorithms=['HS256'])
        if not 'uid' in payload.keys(): return None
        else: return payload['uid']

    def isValid(self, tokenStr):
        payload = jwt.decode(tokenStr, self._config.getJwtSecret(), algorithms=['HS256'])
        if not 'exp' in payload.keys(): return False
        if not 'uid' in payload.keys(): return False
        if payload['exp'] < self.timeMillis(): return False
        else: return True


