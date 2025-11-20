class Player:
    """
    Represents a player in the game with a hand of cards.
    """
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_cards(self, new_cards):
        """
        Adds cards to the player's hand.
        """
        self.hand.extend(new_cards)

    def play_card(self):
        """
        Plays one card from the top of the player's hand.
        """
        if self.hand:
            return self.hand.pop(0)
        return None

    def has_enough_cards_for_war(self):
        """
        Checks if the player has enough cards for a war (at least 4 cards).
        """
        return len(self.hand) >= 4