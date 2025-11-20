import tkinter as tk
from tkinter import messagebox
from blackjack_game import BlackjackGame
from PIL import Image, ImageTk

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
        self.card_images = {}  # Our card image cache
        self.load_card_images()
        self.card_back_image = self.load_specific_card_image("images/card_back.png")

        # --- Dealer Frame ---
        self.dealer_frame = tk.Frame(master, bg='darkgreen')
        self.dealer_frame.pack(pady=10)

        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer's Hand", font=("Arial", 16, "bold"), bg='darkgreen', fg='white')
        self.dealer_label.pack()

        self.dealer_cards_label = tk.Label(self.dealer_frame, image=None, bg='darkgreen')  # Use image, not text
        self.dealer_cards_label.pack()

        self.dealer_score_label = tk.Label(self.dealer_frame, text="Score: 0", font=("Arial", 14), bg='darkgreen', fg='white')
        self.dealer_score_label.pack()

        # --- Player Frame ---
        self.player_frame = tk.Frame(master, bg='darkgreen')
        self.player_frame.pack(pady=20)

        self.player_label = tk.Label(self.player_frame, text="Player's Hand", font=("Arial", 16, "bold"), bg='darkgreen', fg='white')
        self.player_label.pack()

        self.player_cards_label = tk.Label(self.player_frame, image=None, bg='darkgreen')  # Use image, not text
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

    def load_card_images(self):
        """Loads all card images and stores them in the cache."""
        for card in self.game.deck.cards:
            try:
                image = Image.open(card.image_path)
                image = image.resize((75, 110), Image.Resampling.LANCZOS)  # Adjust size as needed
                photo = ImageTk.PhotoImage(image)
                self.card_images[str(card)] = photo
            except FileNotFoundError:
                print(f"Error: Card image not found at {card.image_path}")
                self.card_images[str(card)] = None  # Store None if image is missing

    def load_specific_card_image(self, path, size=(75, 110)):
        """Loads a single image, like the card back."""
        try:
            image = Image.open(path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Error: Card image not found at {path}")
            return None

    def update_display(self):
        # Player's hand
        player_images = [self.card_images.get(str(card)) for card in self.game.player.hand]
        # Display the last card only for simplicity
        if player_images:
            self.player_cards_label.config(image=player_images[-1])
            self.player_cards_label.image = player_images[-1]  # Keep reference
        else:
            self.player_cards_label.config(image=None)

        self.player_score_label.config(text=f"Score: {self.game.get_player_score()}")
    
        # Dealer's hand
        if self.game.game_over:
            dealer_images = [self.card_images.get(str(card)) for card in self.game.dealer.hand]
            if dealer_images:
                # For simplicity, just show the last card image. A real implementation would composite them.
                self.dealer_cards_label.config(image=dealer_images[-1])
                self.dealer_cards_label.image = dealer_images[-1]
            self.dealer_score_label.config(text=f"Score: {self.game.get_dealer_score(hide_first_card=False)}")
        else:
            # Hide dealer's first card
            if len(self.game.dealer.hand) > 1:
                # Show one card face up and one face down
                self.dealer_cards_label.config(image=self.card_back_image)
                self.dealer_cards_label.image = self.card_back_image
            else:
                self.dealer_cards_label.config(image=None)

            self.dealer_score_label.config(text=f"Score: {self.game.get_dealer_score(hide_first_card=True)}")

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