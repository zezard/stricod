class User:
    def __init__(self, _id, name):
        self._id = _id
        self._name = name
    def getId(self): return self._id
    def getName(self): return self._name
    def __repr__(self): return "User("+str(self._id)+", "+self._name+")"

