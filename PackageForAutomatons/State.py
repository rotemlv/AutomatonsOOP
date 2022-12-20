class State:
    def __init__(self, symbol):
        self.degree_in = self.degree_out = 0
        self.symbol = symbol

    def deg_in(self):
        return self.degree_in

    def deg_out(self):
        return self.degree_out
