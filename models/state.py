from typing import Any, Dict, List, Optional
import uuid

from .action import Action
from .blinds import Blinds
from .card import Card
from .deck import Deck


class State(object):

    bets: Dict[uuid.UUID, int]
    blinds: Blinds
    board: List[Card]
    dealer_position: int
    deck: Deck
    holes: Dict[uuid.UUID, List[Card]]
    in_play: List[uuid.UUID]
    players: List[uuid.UUID]
    pot: int
    stacks: Dict[uuid.UUID, int]
    to_act: int
    winners: List[uuid.UUID]

    def __init__(self,
            bets: Optional[Dict[uuid.UUID, int]] = None,
            blinds: Optional[Blinds] = None,
            board: Optional[List[Card]] = None,
            dealer_position: Optional[int] = None,
            deck: Optional[Deck] = None,
            holes: Optional[Dict[uuid.UUID, List[Card]]] = None,
            in_play: Optional[List[uuid.UUID]] = None,
            players: Optional[List[uuid.UUID]] = None,
            pot: Optional[int] = None,
            stacks: Optional[Dict[uuid.UUID, int]] = None,
            to_act: Optional[int] = None,
            winners: Optional[List[uuid.UUID] ]= None):
        self.bets = bets or {}
        self.blinds = blinds or Blinds(5, 10)
        self.board = board or []
        self.dealer_position = dealer_position or -1
        self.deck = deck or Deck()
        self.holes = holes or {}
        self.in_play = in_play or []
        self.players = players or []
        self.pot = pot or 0
        self.stacks = stacks or {}
        self.to_act = to_act or 0
        self.winners = winners or []

    @staticmethod
    def new_state(
            state,
            changes: Optional[Dict[str, Any]] = None):
        members = vars(state)
        if changes:
            members.update(changes)
        return State(**members)
