from deck import Deck
from player import Player

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.game_over = False
        self.winner = None
        self.message = "Welcome to Blackjack! Click 'Deal' to start."

    def deal_initial_cards(self):
        self.deck = Deck() # Reset and shuffle deck for a new game
        self.deck.shuffle()
        self.player.hand = []
        self.dealer.hand = []
        self.game_over = False
        self.winner = None
        self.message = ""

        self.player.add_cards([self.deck.deal(), self.deck.deal()])
        self.dealer.add_cards([self.deck.deal(), self.deck.deal()]) # One card face down for dealer

        self.check_for_blackjack()
        if not self.game_over:
            self.message = "Player's turn. Hit or Stand?"

    def _calculate_hand_value(self, hand):
        value = 0
        num_aces = 0
        for card in hand:
            if card.rank.isdigit():
                value += int(card.rank)
            elif card.rank in ["J", "Q", "K"]:
                value += 10
            elif card.rank == "A":
                num_aces += 1
                value += 11 # Assume 11 for now

        while value > 21 and num_aces > 0:
            value -= 10 # Change an Ace from 11 to 1
            num_aces -= 1
        return value

    def get_player_score(self):
        return self._calculate_hand_value(self.player.hand)

    def get_dealer_score(self, hide_first_card=True):
        if hide_first_card and not self.game_over:
            # Only show the value of the second card
            if len(self.dealer.hand) > 1:
                return self._calculate_hand_value([self.dealer.hand[1]])
            return 0 # Or some indicator that only one card is dealt
        return self._calculate_hand_value(self.dealer.hand)

    def hit(self):
        if self.game_over:
            return
        self.player.add_cards([self.deck.deal()])
        player_score = self.get_player_score()
        if player_score > 21:
            self.message = "Player busts! Dealer wins."
            self.winner = "Dealer"
            self.game_over = True
        elif player_score == 21:
            self.message = "Player has 21! Time for dealer to play."
            self.dealer_turn()
        else:
            self.message = "Player hits. Hit or Stand?"

    def stand(self):
        if self.game_over:
            return
        self.message = "Player stands. Dealer's turn."
        self.dealer_turn()

    def dealer_turn(self):
        if self.game_over:
            return

        player_score = self.get_player_score()
        while self.get_dealer_score(hide_first_card=False) < 17 and self.get_dealer_score(hide_first_card=False) < player_score:
            self.dealer.add_cards([self.deck.deal()])

        dealer_score = self.get_dealer_score(hide_first_card=False)
        if dealer_score > 21:
            self.message = "Dealer busts! Player wins!"
            self.winner = "Player"
        elif dealer_score > player_score:
            self.message = "Dealer wins!"
            self.winner = "Dealer"
        elif dealer_score < player_score:
            self.message = "Player wins!"
            self.winner = "Player"
        else:
            self.message = "Push! It's a tie."
            self.winner = "Push"
        self.game_over = True

    def check_for_blackjack(self):
        if self.get_player_score() == 21 and self.get_dealer_score(hide_first_card=False) == 21:
            self.message = "Both have Blackjack! Push!"
            self.winner = "Push"
            self.game_over = True
        elif self.get_player_score() == 21:
            self.message = "Player has Blackjack! Player wins!"
            self.winner = "Player"
            self.game_over = True
        elif self.get_dealer_score(hide_first_card=False) == 21:
            self.message = "Dealer has Blackjack! Dealer wins!"
            self.winner = "Dealer"
            self.game_over = True