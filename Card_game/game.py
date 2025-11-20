from deck import Deck
from player import Player

class Game:
    """
    Manages the game of War.
    """
    def __init__(self, player_names=["Player 1", "Player 2"]):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self._deal_cards()
        self.turn_limit = 1000

    def _deal_cards(self):
        """
        Deals the cards to the players.
        """
        num_players = len(self.players)
        card_index = 0
        while self.deck.cards:
            player_to_deal = self.players[card_index % num_players]
            player_to_deal.add_cards([self.deck.deal()])
            card_index += 1

    def play_turn(self):
        """
        Plays one turn of the game.
        """
        turn_result = {
            "status": "continue",
            "played_cards": [],
            "message": "",
            "winner": None,
            "war_cards": []
        }

        active_players = [p for p in self.players if len(p.hand) > 0]
        if len(active_players) < 2:
            turn_result["status"] = "game_over"
            if active_players:
                turn_result["winner"] = active_players[0].name
            return turn_result

        cards_on_table = []
        for player in active_players:
            card = player.play_card()
            if card:
                cards_on_table.append((player, card))
                turn_result["played_cards"].append({"player": player.name, "card": card})

        if not cards_on_table:
            turn_result["status"] = "game_over"
            return turn_result

        max_value = max(card.value for _, card in cards_on_table)
        winners = [(p, c) for p, c in cards_on_table if c.value == max_value]

        if len(winners) == 1:
            winner, _ = winners[0]
            turn_result["message"] = f"{winner.name} wins the round!"
            winner.add_cards([card for _, card in cards_on_table])
            turn_result["winner"] = winner.name
        else:
            turn_result["message"] = "It's a WAR!"
            war_result = self.war([p for p, _ in winners], [c for _, c in cards_on_table])
            turn_result.update(war_result)

        return turn_result

    def war(self, warring_players, war_pile):
        """
        Handles the "war" scenario.
        """
        war_result = {
            "winner": None,
            "message": "",
            "war_cards": []
        }

        while True:
            # Check for forfeits
            active_warriors = []
            for p in warring_players:
                if len(p.hand) < 4:
                    war_result["message"] += f"\n{p.name} forfeits war (not enough cards)!"
                else:
                    active_warriors.append(p)

            if len(active_warriors) < 2:
                if len(active_warriors) == 1:
                    winner = active_warriors[0]
                    war_result["winner"] = winner.name
                    war_result["message"] += f"\n{winner.name} wins the war by default!"
                    winner.add_cards(war_pile)
                else:
                    war_result["message"] += "\nAll players forfeited. Cards discarded."
                return war_result

            # Place face-down cards
            for p in active_warriors:
                for _ in range(3):
                    card = p.play_card()
                    if card:
                        war_pile.append(card)
                        war_result["war_cards"].append({"player": p.name, "card": card, "face_up": False})

            # Place face-up cards
            face_up_cards = []
            for p in active_warriors:
                card = p.play_card()
                if card:
                    face_up_cards.append((p, card))
                    war_pile.append(card)
                    war_result["war_cards"].append({"player": p.name, "card": card, "face_up": True})

            max_value = max(c.value for _, c in face_up_cards)
            winners = [(p, c) for p, c in face_up_cards if c.value == max_value]

            if len(winners) == 1:
                winner, _ = winners[0]
                war_result["winner"] = winner.name
                war_result["message"] += f"\n{winner.name} wins the war!"
                winner.add_cards(war_pile)
                return war_result
            else:
                war_result["message"] += "\nAnother WAR!"
                warring_players = [p for p, _ in winners]
                # The loop continues with the new set of tied players

    def start_game(self):
        # This method is no longer needed for the console version.
        # The GUI will drive the game turn by turn.
        pass