import uuid

from .action import Action, ActionType
from .blinds import Blinds
from .deck import Deck
from .state import State


class TableActionType(ActionType):

    ADD_PLAYER = 0, "Add Player"
    BUY_IN = 1, "Buy In"
    CASH_OUT = 2, "Cash Out"
    SET_BLINDS = 3, "Set Blinds"

    def __str__(self):
        return self.display


def next(state: State, action: Action) -> State:
    if action.type is TableActionType.ADD_PLAYER:
        return add_player(state, action.player_uuid)
    if action.type is TableActionType.BUY_IN:
        return buy_in(state, action.player_uuid, action.amount)
    if action.type is TableActionType.CASH_OUT:
        return buy_in(state, action.player_uuid)
    if action.type is TableActionType.SET_BLINDS:
        return set_blinds(state, action.blinds)


def add_player(state: State, player_uuid: uuid.UUID) -> State:
    players = state.players
    players.append(player_uuid)
    stacks = state.stacks
    stacks[player_uuid] = 0
    changes = {
        "players": players,
        "stacks": stacks,
    }
    return State.new_state(state, changes=changes)


def buy_in(state: State, player_uuid: uuid.UUID, amount: int) -> State:
    stacks = state.stacks
    stacks[player_uuid] += amount
    return State.new_state(state, changes={"stacks": stacks})


def cash_out(state: State, player_uuid: uuid.UUID) -> State:
    players = state.players
    players.remove(player_uuid)
    stacks = state.stacks
    stacks[player_uuid] = 0
    changes = {
        "players": players,
        "stacks": stacks,
    }
    return State.new_state(state, changes=changes)


def set_blinds(state: State, blinds: Blinds) -> State:
    return State.new_state(state, changes={"blinds": blinds})
