from typing import Dict, List
import uuid

from . import game
from . import player
from . import table
from .action import Action
from .blinds import Blinds
from .state import State


class Poker(object):

    state: State

    def __init__(self):
        self.state = State()

    def add_player(self, name: str) -> uuid.UUID:
        player_uuid = uuid.uuid4()
        self.state = next(
            self.state,
            Action(table.TableActionType.ADD_PLAYER, player_uuid=player_uuid))
        return player_uuid

    def buy_in(self, player_uuid: uuid.UUID, amount: int) -> None:
        self.state = next(
            self.state,
            Action(table.TableActionType.BUY_IN,
                   player_uuid=player_uuid,
                   amount=amount))

    def cash_out(self, player_uuid: uuid.UUID) -> int:
        amount = self.state.stacks[player_uuid]
        self.state = next(
            self.state,
            Action(table.TableActionType.CASH_OUT, player_uuid=player_uuid))
        return amount

    def fold(self, player_uuid: uuid.UUID) -> None:
        self.state = next(
            self.state,
            Action(player.PlayerActionType.FOLD, player_uuid=player_uuid))

    def check(self, player_uuid: uuid.UUID) -> None:
        self.state = next(
            self.state,
            Action(player.PlayerActionType.CHECK, player_uuid=player_uuid))

    def bet(self, player_uuid: uuid.UUID, amount: int) -> None:
        self.state = next(
            self.state,
            Action(player.PlayerActionType.BET,
                   player_uuid=player_uuid,
                   amount=amount))

    def call(self, player_uuid: uuid.UUID, amount: int) -> None:
        self.state = next(
            self.state,
            Action(player.PlayerActionType.CALL,
                   player_uuid=player_uuid,
                   amount=amount))

    def raise_bet(self, player_uuid: uuid.UUID, amount: int) -> None:
        self.state = next(
            self.state,
            Action(player.PlayerActionType.RAISE,
                   player_uuid=player_uuid,
                   amount=amount))

    def start_game(self, blinds: Blinds = Blinds(5, 10)) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.START_GAME, blinds=blinds))

    def deal(self) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.DEAL))

    def end_round(self) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.END_ROUND))

    def flop(self) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.FLOP))

    def turn(self) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.TURN))

    def river(self) -> None:
        self.state = next(
            self.state, Action(game.GameActionType.RIVER))

    def showdown(self) -> List[uuid.UUID]:
        self.state = next(
            self.state, Action(game.GameActionType.SHOWDOWN))
        return self.state.winners

    def end_game(self) -> List[uuid.UUID]:
        self.state = next(
            self.state, Action(game.GameActionType.END))
        return self.state.winners


def next(state: State, action: Action) -> State:
    if isinstance(action.type, game.GameActionType):
        return game.next(state, action)
    if isinstance(action.type, player.PlayerActionType):
        return player.next(state, action)
    if isinstance(action.type, table.TableActionType):
        return table.next(state, action)
