from datetime import datetime
import json

# Factory function to create a Position
def fromDMS(d,m,s, when=datetime.utcnow()):
    return Position({"d":d,"m":m,"s":s}, when)

def fromJSON(js):
    pos = json.loads(js)
    position = {'d':pos['degrees'],'m':pos['minutes'],'s':pos['seconds']}
    timestamp = datetime.strptime(pos["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
    return Position(position, timestamp) 

class Position:

    # Non-prefered to call this constructor directly
    def __init__(self, dms, timestamp):
        self.dms = dms
        self.timestamp = timestamp

    def __str__(self):
        timestamp = self.timestamp.isoformat()
        return json.dumps({
            'degrees':self.dms['d'],
            'minutes':self.dms['m'],
            'seconds':self.dms['s'],
            'timestamp':timestamp
            })

    def getDMS(self): return self.dms
    def getTimestamp(self): return self.timestamp
    def toJSON(self): return self.__str__()


        
