from json import JSONEncoder
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
    def to_dict(state) -> Dict[str, Any]:
        return {
            "bets": {
                str(id): state.bets[id]
                for id in state.bets.keys()
            },
            "blinds": Blinds.to_dict(state.blinds),
            "board": state.board,
            "dealer_position": state.dealer_position,
            "holes": {
                str(id): [Card.to_dict(card) for card in state.holes[id]]
                for id in state.holes.keys()
            },
            "in_play": [str(id) for id in state.in_play],
            "players": [str(id) for id in state.players],
            "pot": state.pot,
            "stacks": {
                str(id): state.stacks[id]
                for id in state.stacks.keys()
            },
            "to_act": state.to_act,
            "winners": [str(id) for id in state.winners],
        }

    @staticmethod
    def new_state(
            state,
            changes: Optional[Dict[str, Any]] = None):
        members = vars(state)
        if changes:
            members.update(changes)
        return State(**members)
