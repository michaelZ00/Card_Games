import tkinter as tk
from tkinter import messagebox
from war_gui import WarGUI
# We will create these files in the next steps
# from blackjack_gui import BlackjackGUI

class GameLauncher:
    def __init__(self, master): 
        self.master = master
        master.title("Game Center")
        master.geometry("300x200")
        master.configure(bg='lightgrey')

        self.label = tk.Label(master, text="Choose a Game to Play", font=("Arial", 16))
        self.label.pack(pady=20)

        self.war_button = tk.Button(master, text="Play War", font=("Arial", 12), command=self.play_war)
        self.war_button.pack(pady=10)

        self.blackjack_button = tk.Button(master, text="Play Blackjack", font=("Arial", 12), command=self.play_blackjack)
        self.blackjack_button.pack(pady=10)

    def play_war(self):
        # Create a new window for the War game
        war_window = tk.Toplevel(self.master)
        war_window.grab_set() # Modal window
        app = WarGUI(war_window)

    def play_blackjack(self):
        # This will launch the Blackjack game GUI
        # We would need to create blackjack_gui.py containing the BlackjackGUI class
        print("Launching Blackjack... (GUI code would go in blackjack_gui.py)")
        messagebox.showinfo("Launcher", "Launching Blackjack Game! (This would open a new window)")


if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root) # This creates the main menu
    root.mainloop()
