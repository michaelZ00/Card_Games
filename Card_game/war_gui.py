import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os
from game import WarGame

class WarGUI:
    def __init__(self, master):
        self.master = master
        master.title("Card Game: War")
        master.geometry("800x600")
        master.configure(bg='green')

        self.game = None
        self.player_frames = {}
        self.card_images = {}

        # --- Load Card Images ---
        self.card_back_image = self.load_card_image("images/card_back.png")

        # --- Main Frames ---
        self.top_frame = tk.Frame(master, bg='green')
        self.top_frame.pack(pady=10)

        self.center_frame = tk.Frame(master, bg='green', padx=20, pady=20)
        self.center_frame.pack(expand=True)

        self.bottom_frame = tk.Frame(master, bg='green')
        self.bottom_frame.pack(pady=20)

        # --- Widgets ---
        self.message_label = tk.Label(self.bottom_frame, text="Welcome to War! Click 'Start Game'.", font=("Arial", 14), bg='green', fg='white')
        self.message_label.pack()

        self.play_turn_button = tk.Button(self.bottom_frame, text="Play Turn", font=("Arial", 12), command=self.play_turn, state=tk.DISABLED)
        self.play_turn_button.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(self.bottom_frame, text="Start Game", font=("Arial", 12), command=self.setup_game)
        self.start_button.pack(side=tk.LEFT, padx=10)

    def load_card_image(self, path, size=(100, 150)):
        if not os.path.exists(path):
            print(f"Warning: Image not found at {path}")
            return None
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def setup_game(self):
        num_players = simpledialog.askinteger("Number of Players", "Enter number of players (2 or more):", minvalue=2, parent=self.master)
        if not num_players:
            return

        player_names = []
        for i in range(num_players):
            name = simpledialog.askstring("Player Name", f"Enter name for Player {i+1}:", parent=self.master)
            if not name:
                name = f"Player {i+1}"
            player_names.append(name)

        self.game = WarGame(player_names)
        self.create_player_ui()
        self.update_display()

        self.message_label.config(text="Game started! Press 'Play Turn'.")
        self.start_button.config(state=tk.DISABLED)
        self.play_turn_button.config(state=tk.NORMAL)

    def create_player_ui(self):
        # Clear old frames if any
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        self.player_frames = {}

        for player in self.game.players:
            frame = tk.Frame(self.top_frame, bg='darkgreen', bd=2, relief='ridge', padx=10, pady=10)
            frame.pack(side=tk.LEFT, padx=20)

            name_label = tk.Label(frame, text=player.name, font=("Arial", 16, "bold"), bg='darkgreen', fg='white')
            name_label.pack()

            card_count_label = tk.Label(frame, text=f"Cards: {len(player.hand)}", font=("Arial", 12), bg='darkgreen', fg='white')
            card_count_label.pack()

            card_display_label = tk.Label(frame, image=self.card_back_image, bg='darkgreen', fg='white', font=("Arial", 14, "bold"), width=12, height=7, compound='center')
            card_display_label.pack(pady=5)
            card_display_label.image = self.card_back_image # Keep a reference

            self.player_frames[player.name] = {
                "frame": frame,
                "name_label": name_label,
                "card_count_label": card_count_label,
                "card_display_label": card_display_label
            }

    def play_turn(self):
        if not self.game:
            return

        turn_result = self.game.play_turn()

        # Update played cards display
        for player_name, p_frame in self.player_frames.items():
            card_played = False
            card_display_label = p_frame["card_display_label"]

            # Check if this player played a card in the main turn
            for played in turn_result.get("played_cards", []):
                if played["player"] == player_name:
                    card = played["card"]
                    card_image = self.load_card_image(card.image_path)
                    if card_image:
                        card_display_label.config(image=card_image, text='', bg='darkgreen')
                        card_display_label.image = card_image # Keep a reference
                    else:
                        color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
                        card_text = f"{card.rank}\n\n{card.suit}"
                        card_display_label.config(image='', text=card_text, fg=color, bg='white')
                        card_display_label.image = None
                    card_played = True
                    break
            # If player didn't play a card in the main turn, check war cards
            if not card_played:
                for war_card_info in turn_result.get("war_cards", []):
                    if war_card_info["player"] == player_name and war_card_info["face_up"]:
                        card = war_card_info["card"]
                        card_image = self.load_card_image(card.image_path)
                        if card_image:
                            card_display_label.config(image=card_image, text='', bg='darkgreen')
                            card_display_label.image = card_image # Keep a reference
                        else:
                            color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
                            card_text = f"{card.rank}\n\n{card.suit}"
                            card_display_label.config(image='', text=card_text, fg=color, bg='white')
                            card_display_label.image = None
                        card_played = True
                        break
            if not card_played: # If player didn't play any card this turn (e.g., out of cards or face-down war card)
                card_display_label.config(image='', text='', bg='darkgreen')
                card_display_label.image = None

        self.message_label.config(text=turn_result.get("message", ""))

        # Short delay before updating counts and resetting for next turn
        self.master.after(1500, lambda: self.finish_turn(turn_result))

    def finish_turn(self, turn_result):
        self.update_display()

        if turn_result["status"] == "game_over":
            winner = turn_result.get("winner")
            if winner:
                messagebox.showinfo("Game Over!", f"{winner} wins the game!", parent=self.master)
            else:
                messagebox.showinfo("Game Over!", "The game has ended with no clear winner (e.g., all players out of cards).", parent=self.master)
            self.play_turn_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)

    def update_display(self):
        if not self.game:
            return

        active_players = [p.name for p in self.game.players if len(p.hand) > 0]

        for player_name, p_frame in self.player_frames.items():
            if player_name in active_players:
                player_obj = next((p for p in self.game.players if p.name == player_name), None)
                card_display_label = p_frame["card_display_label"]
                p_frame["card_count_label"].config(text=f"Cards: {len(player_obj.hand)}")
                card_display_label.config(image=self.card_back_image, text='', bg='darkgreen')
                card_display_label.image = self.card_back_image # Keep reference
                p_frame["frame"].config(bg='darkgreen') # Reset background if player was greyed out
            else: # Player is out of the game
                p_frame["card_count_label"].config(text="Out of cards")
                p_frame["card_display_label"].config(image='', text='', bg='grey')
                p_frame["card_display_label"].image = None
                p_frame["frame"].config(bg='grey')