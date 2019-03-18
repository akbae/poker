import random
from typing import List, Optional

from .card import Card, CardSuit, CardValue


class Deck(object):

    cards: List[Card]

    def __init__(self, seed: Optional[int] = None):
        random.seed(seed)
        self.cards = self._init_cards()

    def _init_cards(self) -> List[Card]:
        cards = [Card(value, suit)
                 for value in CardValue
                 for suit in CardSuit]
        random.shuffle(cards)
        return cards

    def draw(self, num: int = 1) -> List[Card]:
        drawn_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return drawn_cards

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return "\n".join(map(str, self.cards))

    def __str__(self):
        return ", ".join(map(str, self.cards))
