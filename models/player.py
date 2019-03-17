import uuid

from .action import Action, ActionType
from . import game
from .state import State


class PlayerActionType(ActionType):

    # Can be performed any time
    FOLD = 0, "Fold"
    # Can only be performed if first to act or previously checked/folded
    CHECK = 1, "Check"
    BET = 2, "Bet"
    # Can only be performed if previously bet, called, or raised
    CALL = 3, "Call"
    RAISE = 4, "Raise"

    @staticmethod
    def is_valid_action(max_type, type) -> bool:
        if type is PlayerActionType.FOLD:
            return True
        elif type in (PlayerActionType.CHECK, PlayerActionType.BET):
            return max_type < PlayerActionType.BET
        return max_type > PlayerActionType.CHECK

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


def next(state: State, action: Action) -> State:
    if action.type is PlayerActionType.FOLD:
        return fold(state, action.player_uuid)
    if action.type is PlayerActionType.CHECK:
        return check(state, action.player_uuid)
    if action.type is PlayerActionType.BET:
        return bet(state, action.player_uuid, action.amount)
    if action.type is PlayerActionType.CALL:
        return call(state, action.player_uuid, action.amount)
    if action.type is PlayerActionType.RAISE:
        return raise_bet(state, action.player_uuid, action.amount)


def fold(state: State, player_uuid: uuid.UUID) -> State:
    holes = state.holes
    holes.pop(player_uuid)
    in_play = state.in_play
    in_play.remove(player_uuid)
    changes = {
        "holes": holes,
        "in_play": in_play,
    }
    new_state = State.new_state(state, changes=changes)
    if len(in_play) == 1:
        # Last fold -> end game
        return game.end_game(new_state, in_play)
    return new_state


def check(state: State, player_uuid: uuid.UUID) -> State:
    to_act = (state.to_act + 1) % len(state.in_play)
    return State.new_state(state, changes={"to_act": to_act})


def bet(state: State, player_uuid: uuid.UUID, amount: int) -> State:
    bets = state.bets
    bets[player_uuid] = amount
    pot = state.pot + amount
    stacks = state.stacks
    stacks[player_uuid] -= amount
    to_act = (state.to_act + 1) % len(state.in_play)
    changes = {
        "bets": bets,
        "pot": pot,
        "stacks": stacks,
        "to_act": to_act,
    }
    return State.new_state(state, changes=changes)


def call(state: State, player_uuid: uuid.UUID, amount: int) -> State:
    bets = state.bets
    bets[player_uuid] = bets.setdefault(player_uuid, 0)
    bets[player_uuid] += amount
    pot = state.pot + amount
    stacks = state.stacks
    stacks[player_uuid] -= amount
    to_act = (state.to_act + 1) % len(state.in_play)
    changes = {
        "bets": bets,
        "pot": pot,
        "stacks": stacks,
        "to_act": to_act,
    }
    return State.new_state(state, changes=changes)


def raise_bet(state: State, player_uuid: uuid.UUID, amount: int) -> State:
    bets = state.bets
    bets[player_uuid] = bets.setdefault(player_uuid, 0)
    bets[player_uuid] += amount
    pot = state.pot + amount
    stacks = state.stacks
    stacks[player_uuid] -= amount
    to_act = (state.to_act + 1) % len(state.in_play)
    changes = {
        "bets": bets,
        "pot": pot,
        "stacks": stacks,
        "to_act": to_act,
    }
    return State.new_state(state, changes=changes)
