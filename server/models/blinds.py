from typing import Dict

class Blinds(object):

    small: int
    big: int

    def __init__(self, small, big):
        self.small = small
        self.big = big

    @staticmethod
    def to_dict(blinds) -> Dict[str, int]:
        return blinds.__dict__

    def __str__(self):
        return f"Small blinds: {self.small:.2f}, Big blinds: {self.big:.2f}"
