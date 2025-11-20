import random
from card import Card

class Deck:
    """
    Represents a deck of 52 playing cards.
    """
    def __init__(self):
        self.cards = self._create_deck()
        self.shuffle()

    def _create_deck(self):
        """
        Creates a standard 52-card deck.
        """
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        Deals one card from the top of the deck.
        """
        if self.cards:
            return self.cards.pop()
        return None