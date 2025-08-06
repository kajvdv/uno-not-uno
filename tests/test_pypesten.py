import pytest
import logging

from pesten.pesten import Pesten, card, card_string, CannotDraw

logger = logging.getLogger(__name__)


# class Client(Pesten):
#     def inspect_stack(self, play_stack):
#         for card, upper_card in zip(play_stack, play_stack[1:]):
#             if not (
#                 upper_card // 13 == card // 13
#                 or upper_card % 13 == card % 13 
#             ):
#                 return False
#         return True
            
#     def can_be_played(self, card):
#         top_card = self.play_stack[-1]
#         return (
#             top_card // 13 == card // 13
#             or top_card % 13 == card % 13 
#         )
    
#     def should_be_next(self, player_i):
#         if self.has_won:
#             return player_i
#         return (player_i + 1) % self.player_count

#     def draw_and_inspect(self):
#         len_prev_draw = len(self.draw_stack)
#         prev_curr_player = self.current_player
#         if len(self.draw_stack) == 0:
#             self.play_turn(-1)
#             #TODO assert for reshuffling
#         else:
#             self.play_turn(-1)
#             assert self.should_be_next(prev_curr_player) == self.current_player, "Did not go to next player after drawing card"
#             assert len(self.draw_stack) == len_prev_draw - 1, "Not taken from draw stack"
    
#     def play_and_inspect(self):
#         # Plays all the cards one by one and checks if turn was correct
#         for i, card in enumerate(self.curr_hand):
#             play_stack = self.play_stack
#             prev_curr_player = self.current_player
#             len_prev_stack = len(play_stack)
#             assert self.inspect_stack(play_stack)
#             if self.can_be_played(card):
#                 print(f"{card_string(card)} can be played on top {card_string(self.play_stack[-1])}")
#                 self.play_turn(i)
#                 assert len_prev_stack + 1 == len(play_stack), 'Valid card can not be played'
#                 assert self.should_be_next(prev_curr_player) == self.current_player, "Player did not change after playing a valid card"
#                 return
#             else:
#                 print(f"{card_string(card)} ({card}) can not be played on top {card_string(self.play_stack[-1])}")
#                 self.play_turn(i)
#                 assert len_prev_stack == len(play_stack), "Unvalid card was played"
#                 assert prev_curr_player == self.current_player, "Player was changed after playing unvalid card"
#         self.draw_and_inspect()


# @pytest.mark.parametrize('seed', range(1000))
# def test_game_without_special_rules(seed):
#     import random
#     cards = [card(suit, value) for suit in range(4) for value in range(13)] 
#     random.seed(seed)
#     random.shuffle(cards)
#     client = Client(2, 8, cards)
#     while not client.has_won:
#         client.play_and_inspect()


GETTING_CHOOSE      = 1
CHECK_CARD          = 2
PLAY_CHOOSE         = 3
DRAW_CARD           = 4
DECIDE_NEXT_PLAYER  = 5
ANOTHER_TURN        = 6
SKIP_TURN           = 7
REVERSE_ORDER       = 8
DRAW_MULTIPLE_CARD  = 9
CHANGE_SUIT         = 10
GAME_WON            = 11

class Client(Pesten):
    def __init__(self, player_count, hand_count, cards, rules = {}):
        super().__init__(player_count, hand_count, cards, rules)
        self.state = GETTING_CHOOSE
        self.choose = None

    def _can_play(self, choose):
        curr_hand = self.hands[self.current_player]
        card = curr_hand[choose]
        top_card = self.play_stack[-1]
        return (
            top_card // 13 == card // 13
            or top_card % 13 == card % 13 
        )

    def _is_special_card(self, card):
        value = card % 13
        return value in self.rules

    def _get_special_state(self, card):
        value = card % 13
        rule = self.rules[value]
        if rule == 'another_turn':
            return ANOTHER_TURN
        if rule == "skip_turn":
            return SKIP_TURN
        if rule == "reverse_order":
            return REVERSE_ORDER
        if rule == "draw_card-2":
            return DRAW_CARD
        if rule == "change_suit":
            return CHANGE_SUIT

    def cycle(self):
        choose = self.choose
        prev_player = self.prev_player
        logger.debug(f"{prev_player=}")
        if self.state == GETTING_CHOOSE:
            assert type(choose) == int
            logger.debug(f"GETTING_CHOOSE -> CHECK_CARD")
            return CHECK_CARD
        if self.state == CHECK_CARD:
            
            if choose < 0:
                logger.debug(f"CHECK_CARD -> DRAW_CARD")
                return DRAW_CARD
            elif not self._can_play(choose):
                logger.debug(f"CHECK_CARD -> GETTING_CHOOSE")
                return GETTING_CHOOSE
            else:
                assert prev_player == self.current_player
                logger.debug(f"CHECK_CARD -> PLAY_CHOOSE")
                return PLAY_CHOOSE
        if self.state == PLAY_CHOOSE:
            assert 0 <= choose < len(self.curr_hand)
            choosen_card = self.curr_hand[choose]
            self.play_turn(choose)
            if self.has_won:
                logger.debug(f"PLAY_CHOOSE -> GAME_WON")
                return GAME_WON
            elif self._is_special_card(choosen_card):
                state = self._get_special_state(choosen_card)
                logger.debug(f"PLAY_CHOOSE -> {state}")
                return state
            else:
                logger.debug("PLAY_CHOOSE -> DECIDE_NEXT_PLAYER")
                return DECIDE_NEXT_PLAYER
        if self.state == DRAW_CARD:
            assert choose < 0
            self.play_turn(choose)
            logger.debug("DRAW_CARD -> DECIDE_NEXT_PLAYER")
            return DECIDE_NEXT_PLAYER
        if self.state == DECIDE_NEXT_PLAYER:
            assert self.current_player != prev_player, "Player did not change after turn"
            logger.debug("DECIDE_NEXT_PLAYER -> GETTING_CHOOSE")
            return GETTING_CHOOSE
        if self.state == ANOTHER_TURN:
            assert prev_player == self.current_player, "Player did not played again while they should've"
            return GETTING_CHOOSE
        if self.state == SKIP_TURN:
            
            return GETTING_CHOOSE
        if self.state == REVERSE_ORDER:

            return DECIDE_NEXT_PLAYER
        if self.state == DRAW_MULTIPLE_CARD:

            return GETTING_CHOOSE
        if self.state == CHANGE_SUIT:

            return GETTING_CHOOSE
        raise Exception(f"State {self.state} is not defined")

    def inspect_play_turn(self, choose):
        self.choose = choose
        logger.debug(f"Topcard: {self.play_stack[-1]} / {card_string(self.play_stack[-1])}")
        logger.debug(f"Choose: {self.choose} / {card_string(self.curr_hand[choose])}")
        self.prev_player = self.current_player
        for _ in range(100): # Only cycle max 100 times
            self.state = self.cycle()
            if self.state == GETTING_CHOOSE:
                return
            elif self.state == GAME_WON:
                return
        raise Exception("Game got stuck")
        

@pytest.mark.parametrize('seed', range(1000))
@pytest.mark.parametrize('rules', [
    {}, # no rules
    {5: "another_turn"},
    {5: "skip_turn"},
    {5: "reverse_order"},
    {5: "draw_card-2"},
    {5: "change_suit"},
])
def test_two_player_games(seed, rules):
    from pesten.pesten import card
    import random
    cards = [card(suit, value) for suit in range(4) for value in range(13)] 
    random.seed(seed)
    random.shuffle(cards)
    game = Client(2, 8, cards, rules=rules)
    while True:
        prev_player = game.current_player
        for i, _ in enumerate(game.curr_hand):
            game.inspect_play_turn(i)
            if prev_player != game.current_player:
                break
        if game.state == GAME_WON:
            break
        try:
            game.inspect_play_turn(-1)
        except CannotDraw:
            logger.warning("Test stopped because players couldn't play a card anymore")
            return
        