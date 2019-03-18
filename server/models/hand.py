import itertools
import operator
from typing import Any, Callable, Collection, Dict, List, Optional

from aenum import Enum

from .card import Card, CardSuit, CardValue

HAND_SIZE = 5  # Number of cards in a valid hand


class HandType(Enum):

    _init_ = "value display"

    # Used as filler
    UNSET = 0, "Unset"

    HIGH_CARD = 1, "High Card"
    PAIR = 2, "Pair"
    TWO_PAIR = 3, "Two Pair"
    THREE_OF_A_KIND = 4, "Three of a Kind"
    STRAIGHT = 5, "Straight"
    FLUSH = 6, "Flush"
    FULL_HOUSE = 7, "Full House"
    FOUR_OF_A_KIND = 8, "Four of a Kind"
    STRAIGHT_FLUSH = 9, "Straight Flush"

    @classmethod
    def _missing_value_(cls, value):
        """Overrides to direct display value to the correct enum."""
        for member in cls:
            if member.display == value:
                return member

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.display

    def __str__(self):
        return self.display


class Hand(object):

    type: HandType
    type_cards: List[Card]  # Ordered desc (most important card at 0)
    other_cards: List[Card]  # Ordered desc (highest card at 0)

    def __init__(self,
            type: Any, type_cards: List[Card], other_cards: List[Card]):
        self.type = HandType(type)
        self.type_cards = type_cards
        self.other_cards = other_cards

    def _compare_hands(self, other,
            compare: Callable[[Any, Any], bool]) -> bool:
        if self.type != other.type:
            return compare(self.type, other.type)

        # Compare type cards first
        type_cards_comparison: Optional[bool] = self._compare_cards(
            self.type_cards, other.type_cards, compare)
        if type_cards_comparison is not None:
            return type_cards_comparison

        # Then compare other cards
        num_eval: int = HAND_SIZE - len(self.type_cards)  # Evaluate only HAND_SIZE # of cards
        other_cards_comparison: Optional[bool] = self._compare_cards(
            self.other_cards[:num_eval], other.other_cards[:num_eval], compare)
        if other_cards_comparison is not None:
            return other_cards_comparison

        # Both hands are equal, hack - return comparison of equal items
        return compare(True, True)

    def _compare_cards(self,
            first: List[Card],
            second: List[Card],
            compare: Callable[[Any, Any], bool]) -> Optional[bool]:
        # Compare card-by-card in descending order
        for first_card, second_card in zip(first, second):
            if first_card != second_card:
                return compare(first_card, second_card)
        return None

    def __eq__(self, other):
        return self._compare_hands(other, operator.eq)

    def __gt__(self, other):
        return self._compare_hands(other, operator.gt)

    def __lt__(self, other):
        return self._compare_hands(other, operator.lt)

    def __repr__(self):
        return f"{self.type}: {(self.type_cards + self.other_cards)[:5]}"

    def __str__(self):
        return f"{self.type}: {(self.type_cards + self.other_cards)[:5]}"


def determine_hand(hole: Collection[Card], board: Collection[Card]) -> Hand:
    """Main entry point to determine the ranking of the hand."""
    ORDERED_FUNCS = [
        get_straight_flush,
        get_four_of_a_kind,
        get_full_house,
        get_flush,
        get_straight,
        get_three_of_a_kind,
        get_two_pair,
        get_pair,
        get_high_card,
    ]
    sorted_cards: List[Card] = sorted(list(hole) + list(board), reverse=True)

    func: Callable[List[Card], Optional[Hand]]
    for func in ORDERED_FUNCS:
        hand: Optional[Hand] = func(sorted_cards)
        if hand is not None:
            return hand


# All of these functions operate under the assumption that:
# 1) the functions above them did not return a result
# 2) the cards are sorted in descending order

def get_straight_flush(cards: List[Card]) -> Optional[Hand]:
    flush: Optional[Hand] = get_flush(cards)
    if flush is None:
        return None
    straight: Optional[Hand] = get_straight(flush.type_cards)
    if straight is None:
        return None

    return Hand(HandType.STRAIGHT_FLUSH, flush.type_cards, flush.other_cards)


def get_four_of_a_kind(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE = 4

    match: Optional[Hand] = _get_match(cards, TYPE_SIZE)
    if match is None:
        return None

    return Hand(HandType.FOUR_OF_A_KIND, match.type_cards, match.other_cards)


def get_full_house(cards: List[Card]) -> Optional[Hand]:
    three_of_a_kind: Optional[Hand] = get_three_of_a_kind(cards)
    if three_of_a_kind is None:
        return None
    pair: Optional[Hand] = get_pair(three_of_a_kind.other_cards)
    if pair is None:
        return None

    return Hand(HandType.FULL_HOUSE,
                three_of_a_kind.type_cards + pair.type_cards,
                pair.other_cards)


def get_flush(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE: int = HAND_SIZE

    suits: Dict[CardSuit, List[Card]] = {}
    flush_suit: Optional[CardSuit] = None
    for card in cards:
        suits[card.suit] = suits.get(card.suit, [])
        suits[card.suit].append(card)
        if len(suits[card.suit]) == TYPE_SIZE:
            flush_suit = card.suit

    if flush_suit is None:
        return None

    type_cards: List[Card] = suits.pop(flush_suit)
    other_cards: List[Card] = list(itertools.chain(*suits.values()))
    return Hand(HandType.FLUSH, type_cards, other_cards)


def get_straight(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE: int = HAND_SIZE

    unique = set(cards)
    if len(unique) < TYPE_SIZE:
        # Not enough unique cards for a straight
        return None
    # Re-sort them
    unique_cards = sorted(list(unique), reverse=True)

    for i in range(len(unique_cards) - TYPE_SIZE + 1):
        num_straight: int = _num_straight(unique_cards, i)
        # Assumption that if there is a straight, there will not be another
        if num_straight >= TYPE_SIZE:
            type_cards = cards[i:i + num_straight]
            other_cards = cards[:i] + cards[i + num_straight:]
            return Hand(HandType.STRAIGHT, type_cards, other_cards)

    return None


def _num_straight(cards, start):
    num_straight = 1
    for next_card in cards[start + 1:]:
        if next_card.value != cards[start].value - num_straight:
            # Straight has ended
            return num_straight
        num_straight += 1

    return num_straight


def get_three_of_a_kind(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE = 3

    match: Optional[Hand] = _get_match(cards, TYPE_SIZE)
    if match is None:
        return None

    return Hand(HandType.THREE_OF_A_KIND, match.type_cards, match.other_cards)


def get_two_pair(cards: List[Card]) -> Optional[Hand]:
    high_pair: Optional[Hand] = get_pair(cards)
    if high_pair is None:
        return None
    low_pair: Optional[Hand] = get_pair(high_pair.other_cards)
    if low_pair is None:
        return None

    return Hand(HandType.TWO_PAIR,
                high_pair.type_cards + low_pair.type_cards,
                low_pair.other_cards)


def get_pair(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE = 2  # 2 cards in a pair

    match: Optional[Hand] = _get_match(cards, TYPE_SIZE)
    if match is None:
        return None

    return Hand(HandType.PAIR, match.type_cards, match.other_cards)


def get_high_card(cards: List[Card]) -> Optional[Hand]:
    TYPE_SIZE: int = HAND_SIZE

    return Hand(HandType.HIGH_CARD, cards[:TYPE_SIZE], [])


def _get_match(cards: List[Card], num_match: int) -> Optional[Hand]:
    for i in range(len(cards) - num_match + 1):
        type_cards = cards[i:i + num_match]
        if type_cards == [type_cards[0]] * num_match:  # Values are equivalent
            other_cards = cards[:i] + cards[i + num_match:]
            return Hand(HandType.UNSET, type_cards, other_cards)

    return None
