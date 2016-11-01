class Token:
    def __init__(self, token):
        self.token = token
    def __repr__(self): return "Token("+self.token+")"
    def get(self): return self.token
