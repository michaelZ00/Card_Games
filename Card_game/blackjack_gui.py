import tkinter as tk
from tkinter import messagebox
from blackjack_game import BlackjackGame

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        master.title("Blackjack")
        master.geometry("800x600")
        master.configure(bg='darkgreen')

        # --- Game Goal Description ---
        self.goal_label = tk.Label(master, text="Goal: Get as close to 21 as possible without going over, and beat the dealer.", font=("Arial", 12), bg='darkgreen', fg='white', wraplength=700)
        self.goal_label.pack(pady=10)

        self.game = BlackjackGame()

        # --- Dealer Frame ---
        self.dealer_frame = tk.Frame(master, bg='darkgreen')
        self.dealer_frame.pack(pady=10)

        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer's Hand", font=("Arial", 16, "bold"), bg='darkgreen', fg='white')
        self.dealer_label.pack()

        self.dealer_cards_label = tk.Label(self.dealer_frame, text="", font=("Arial", 14), bg='darkgreen', fg='white', wraplength=700)
        self.dealer_cards_label.pack()

        self.dealer_score_label = tk.Label(self.dealer_frame, text="Score: 0", font=("Arial", 14), bg='darkgreen', fg='white')
        self.dealer_score_label.pack()

        # --- Player Frame ---
        self.player_frame = tk.Frame(master, bg='darkgreen')
        self.player_frame.pack(pady=20)

        self.player_label = tk.Label(self.player_frame, text="Player's Hand", font=("Arial", 16, "bold"), bg='darkgreen', fg='white')
        self.player_label.pack()

        self.player_cards_label = tk.Label(self.player_frame, text="", font=("Arial", 14), bg='darkgreen', fg='white', wraplength=700)
        self.player_cards_label.pack()

        self.player_score_label = tk.Label(self.player_frame, text="Score: 0", font=("Arial", 14), bg='darkgreen', fg='white')
        self.player_score_label.pack()

        # --- Message and Buttons Frame ---
        self.bottom_frame = tk.Frame(master, bg='darkgreen')
        self.bottom_frame.pack(pady=20)

        self.message_label = tk.Label(self.bottom_frame, text=self.game.message, font=("Arial", 14), bg='darkgreen', fg='white')
        self.message_label.pack(pady=10)

        self.deal_button = tk.Button(self.bottom_frame, text="Deal", font=("Arial", 12), command=self.deal_cards)
        self.deal_button.pack(side=tk.LEFT, padx=10)

        self.hit_button = tk.Button(self.bottom_frame, text="Hit", font=("Arial", 12), command=self.hit, state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.bottom_frame, text="Stand", font=("Arial", 12), command=self.stand, state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.update_display()

    def update_display(self):
        # Player's hand
        player_cards_text = ", ".join(str(card) for card in self.game.player.hand)
        self.player_cards_label.config(text=f"Cards: {player_cards_text}")
        self.player_score_label.config(text=f"Score: {self.game.get_player_score()}")

        # Dealer's hand
        if self.game.game_over:
            dealer_cards_text = ", ".join(str(card) for card in self.game.dealer.hand)
            self.dealer_score_label.config(text=f"Score: {self.game.get_dealer_score(hide_first_card=False)}")
        else:
            # Hide dealer's first card
            if len(self.game.dealer.hand) > 1:
                dealer_cards_text = f"Hidden, {self.game.dealer.hand[1]}"
            else:
                dealer_cards_text = "Hidden"
            self.dealer_score_label.config(text=f"Score: {self.game.get_dealer_score(hide_first_card=True)}")

        self.dealer_cards_label.config(text=f"Cards: {dealer_cards_text}")

        self.message_label.config(text=self.game.message)

        # Update button states
        if self.game.game_over:
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.deal_button.config(state=tk.NORMAL)
            if self.game.winner:
                messagebox.showinfo("Game Over", self.game.message, parent=self.master)
        else:
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.deal_button.config(state=tk.DISABLED)

    def deal_cards(self):
        self.game.deal_initial_cards()
        self.update_display()

    def hit(self):
        self.game.hit()
        self.update_display()

    def stand(self):
        self.game.stand()
        self.update_display()