from models.hand import *
from models.card import *

s2 = Card(2, "s")
s3 = Card(3, "s")
d3 = Card(3, "d")
s4 = Card(4, "s")
d4 = Card(4, "d")
s5 = Card(5, "s")
s6 = Card(6, "s")
d6 = Card(6, "d")
s7 = Card(7, "s")
s8 = Card(8, "s")
d9 = Card(9, "d")


high_card = Hand(HandType.HIGH_CARD, [d9, s5, d4, s3, s2], [])

low_pair_low_kicker = Hand(HandType.PAIR, [s3, d3], [s5, d4, s2])
low_pair_high_kicker = Hand(HandType.PAIR, [s3, d3], [s7, d4, s2])
high_pair_high_kicker = Hand(HandType.PAIR, [s6, d6], [s7, d4, s2])

two_pair = Hand(HandType.TWO_PAIR, [s6, d6, s3, d3], [s2])

low_straight = Hand(HandType.STRAIGHT, [s6, s5, d4, s3, s2], [])
high_straight = Hand(HandType.STRAIGHT, [s7, s6, s5, d4, s3], [])

flush = Hand(HandType.FLUSH, [s8, s7, s6, s5, s3], [])

group = [d9, s8, s6, d6, s5, d4, s4]
hand = determine_hand([], group)


from models.poker import Poker

poker = Poker()
austin = poker.add_player("Austin")
poker.buy_in(austin, 100)
test = poker.add_player("Test")
poker.buy_in(test, 100)
test2 = poker.add_player("Test 2")
poker.buy_in(test2, 100)
poker.start_game()
poker.deal()
poker.call(austin, 10)
poker.call(test, 5)
poker.check(test2)
poker.state.stacks
poker.state.bets
poker.state.pot
poker.end_round()
poker.flop()
poker.bet(test, 20)
poker.fold(test2)
poker.fold(austin)
poker.state.stacks
poker.state.bets
poker.state.pot
