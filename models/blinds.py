

class Blinds(object):

    small: int
    big: int

    def __init__(self, small, big):
        self.small = small
        self.big = big

    def __str__(self):
        return f"Small blinds: {self.small:.2f}, Big blinds: {self.big:.2f}"
