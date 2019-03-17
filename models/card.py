from typing import Any

from aenum import Enum


class CardSuit(Enum):

    _init_ = "value long display"

    CLUBS = "c", "clubs", " of clubs"
    DIAMONDS = "d", "diamonds", " of diamonds"
    HEARTS = "h", "hearts", " of hearts"
    SPADES = "s", "spades", " of spades"

    @classmethod
    def _missing_value(cls, value):
        """Overrides to default long to the correct enum."""
        for member in cls:
            if member.long == value:
                return member

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.display


class CardValue(Enum):

    _init_ = "value display"

    TWO = 2, "2"
    THREE = 3, "3"
    FOUR = 4, "4"
    FIVE = 5, "5"
    SIX = 6, "6"
    SEVEN = 7, "7"
    EIGHT = 8, "8"
    NINE = 9, "9"
    TEN = 10, "10"
    JACK = 11, "J"
    QUEEN = 12, "Q"
    KING = 13, "K"
    ACE = 14, "A"

    @classmethod
    def _missing_value_(cls, value):
        """Overrides to direct display value to the correct enum."""
        for member in cls:
            if member.display == value:
                return member

    def __add__(self, other):
        return CardValue(self.value + other)

    def __sub__(self, other):
        return CardValue(self.value - other)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return self.display


class Card(object):
    def __init__(self, value: Any, suit: Any):
        self.value = CardValue(value)
        self.suit = CardSuit(suit)

    def __eq__(self, other):
        """Each card is unique, so only value is required for equality."""
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        """Reflects __eq__."""
        return hash(self.value)

    def __repr__(self):
        return f"{self.value}{self.suit!r}"

    def __str__(self):
        return f"{self.value}{self.suit}"
