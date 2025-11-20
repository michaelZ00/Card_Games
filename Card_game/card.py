class Card:
    """
    Represents a single playing card with a suit and a rank.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()

    def _get_value(self):
        """
        Gets the numerical value of the card for comparison.
        """
        if self.rank == "J":
            return 11
        elif self.rank == "Q":
            return 12
        elif self.rank == "K":
            return 13
        elif self.rank == "A":
            return 14
        else:
            return int(self.rank)

    def __repr__(self):
        """
        Returns a string representation of the card.
        """
        return f"{self.rank} of {self.suit}"

    @property
    def image_path(self):
        """Returns the path to the card's image file."""
        return f"images/{self.rank}_of_{self.suit}.png"