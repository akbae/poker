import random
from typing import Dict, List, Optional
import uuid

from .action import Action, ActionType
from .blinds import Blinds
from .card import Card
from .deck import Deck
from .hand import determine_hand, Hand
from .state import State


class GameActionType(ActionType):

    START_GAME = 0, "Start Game"
    END_ROUND = 1, "End Round"
    DEAL = 2, "Deal"
    FLOP = 3, "Flop"
    TURN = 4, "Turn"
    RIVER = 5, "River"
    SHOWDOWN = 6, "Showdown"
    END_GAME = 7, "End Game"


def next(state: State, action: Action) -> State:
    if action.type is GameActionType.START_GAME:
        return start_game(state)
    if action.type is GameActionType.END_ROUND:
        return end_round(state)
    if action.type is GameActionType.DEAL:
        return deal(state)
    if action.type is GameActionType.FLOP:
        return flop(state)
    if action.type is GameActionType.TURN:
        return type(state)
    if action.type is GameActionType.RIVER:
        return river(state)
    if action.type is GameActionType.SHOWDOWN:
        return showdown(state)
    if action.type is GameActionType.END_GAME:
        return end_game(state, action.winners)


def start_game(state: State) -> State:
    board = []
    dealer_position = (state.dealer_position + 1) % len(state.players)
    deck = Deck()
    holes = {}
    winners = []
    # Order so dealer is last
    in_play = state.players[dealer_position + 1:] + state.players[:dealer_position + 1]
    # Bet blinds
    bets = {
        in_play[0]: state.blinds.small,
        in_play[1]: state.blinds.big,
    }
    pot = state.blinds.small + state.blinds.big
    stacks = state.stacks
    stacks[in_play[0]] -= min(state.blinds.small, stacks[in_play[0]])
    stacks[in_play[1]] -= min(state.blinds.big, stacks[in_play[1]])
    # Start action from UTG
    to_act = 2 % len(in_play)
    changes = {
        "bets": bets,
        "board": board,
        "dealer_position": dealer_position,
        "deck": deck,
        "holes": holes,
        "in_play": in_play,
        "pot": pot,
        "stacks": stacks,
        "to_act": to_act,
        "winners": winners,
    }
    return State.new_state(state, changes=changes)


def end_round(state: State) -> State:
    bets = {}
    return State.new_state(state, changes={"bets": bets})


def deal(state: State) -> State:
    DEAL_SIZE = 2  # Number of hole cards to deal

    holes: Dict[uuid.UUID, List[Card]] = {}
    for player_uuid in state.in_play:
        holes[player_uuid] = state.deck.draw(num=DEAL_SIZE)
    return State.new_state(state, changes={"holes": holes})


def flop(state: State) -> State:
    FLOP_SIZE = 3  # Number of flop cards to deal

    board = state.deck.draw(num=FLOP_SIZE)
    return State.new_state(state, changes={"board": board})


def turn(state: State) -> State:
    TURN_SIZE = 1  # Number of turn cards to deal

    board = state.board
    board.extend(state.deck.draw(num=TURN_SIZE))
    return State.new_state(state, changes={"board": board})


def river(state: State) -> State:
    RIVER_SIZE = 1  # Number of river cards to deal

    board = state.board
    board.extend(state.deck.draw(num=RIVER_SIZE))
    return State.new_state(state, changes={"board": board})


def showdown(state: State) -> State:
    winners: List[uuid.UUID] = []
    winning_hand: Optional[Hand] = None

    for player_uuid in state.in_play:
        hand = determine_hand(state.holes[player_uuid], state.board)
        if winning_hand is None or hand > winning_hand:
            winners = [player_uuid]
            winning_hand = hand
        elif hand == winning_hand:
            winners.append(player_uuid)

    return end_game(state, winners)


def end_game(state: State, winners: List[uuid.UUID]) -> State:
    stacks: Dict[uuid.UUID, int] = state.stacks
    winnings = _divide_pot(state.pot, len(winners))
    for winner_uuid, winning in zip(winners, winnings):
        stacks[winner_uuid] += winning
    changes = {
        "stacks": stacks,
        "winners": winners,
    }
    return State.new_state(state, changes=changes)


def _divide_pot(pot, num_splits):
    """Randomly selects among winners to provide the additional cent
    (if necessary)."""
    split = int(float(pot) / num_splits)
    winnings = [split] * num_splits
    difference = pot - sum(winnings)
    if difference == 0:
        return winnings
    random_indices = random.sample(range(num_splits), difference)
    for index in random_indices:
        winnings[index] += 1
    return winnings
