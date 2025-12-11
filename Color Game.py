import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Interactive Dice-style Color Game
# - Animates a rolling die (unicode faces)
# - Supports Fair and Tweaked probability modes
# - Tracks player profit and history, can show plots

colors = ["Red", "Blue", "Yellow", "Green", "White", "Purple"]
fair_probabilities = [1/6] * 6
tweaked_probabilities = [0.13, 0.174, 0.174, 0.174, 0.174, 0.174]

UNICODE_DICE = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
# Mapping color names to hex values for UI
COLOR_HEX = {
    "Red": "#e74c3c",
    "Blue": "#3b82f6",
    "Yellow": "#facc15",
    "Green": "#10b981",
    "White": "#ffffff",
    "Purple": "#9b59b6",
}


class ColorDiceGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color Dice Game")
        self.geometry("420x380")
        self.resizable(False, False)

        self.mode = tk.StringVar(value="Fair")
        self.bet_amount = tk.IntVar(value=10)
        self.total_profit = 0.0
        self.plays = 0
        self.history = []  # profit history
        self.outcome_history = []  # color outcomes

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Die display (use tk.Label so we can set background color)
        initial_bg = COLOR_HEX.get(colors[0], "#ffffff")
        self.die_label = tk.Label(frm, text=UNICODE_DICE[0], font=("Segoe UI Emoji", 72), bg=initial_bg, width=3)
        # Ensure padding and placement similar to ttk
        self.die_label.grid(row=0, column=0, columnspan=2, pady=(0, 6))

        self.color_label = tk.Label(frm, text=colors[0], font=("Segoe UI", 14, "bold"), bg=self.cget("bg"))
        self.color_label.grid(row=1, column=0, columnspan=2)

        # Controls
        ttk.Label(frm, text="Mode:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        modes = ttk.Frame(frm)
        modes.grid(row=2, column=1, sticky="e", pady=(10, 0))
        ttk.Radiobutton(modes, text="Fair", variable=self.mode, value="Fair").pack(side="left")
        ttk.Radiobutton(modes, text="Tweaked", variable=self.mode, value="Tweaked").pack(side="left")

        ttk.Label(frm, text="Bet amount:").grid(row=3, column=0, sticky="w")
        ttk.Spinbox(frm, from_=1, to=1000, textvariable=self.bet_amount, width=8).grid(row=3, column=1, sticky="e")

        self.roll_btn = ttk.Button(frm, text="Roll", command=self.start_roll)
        self.roll_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Statistics
        self.profit_label = ttk.Label(frm, text=f"Total Profit: ${self.total_profit:.2f}")
        self.profit_label.grid(row=5, column=0, sticky="w")
        self.plays_label = ttk.Label(frm, text=f"Plays: {self.plays}")
        self.plays_label.grid(row=5, column=1, sticky="e")

        # History and plots
        btns = ttk.Frame(frm)
        btns.grid(row=6, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(btns, text="Show Plots", command=self.show_plots).pack(side="left", padx=6)
        ttk.Button(btns, text="Reset", command=self.reset_game).pack(side="left", padx=6)

        # Small footer
        ttk.Label(frm, text="Close the window to exit.").grid(row=7, column=0, columnspan=2, pady=(18, 0))

    def start_roll(self):
        self.roll_btn.config(state="disabled")
        self._animate_count = 18
        self._animate()

    def _animate(self):
        # Quick animation: change die face and color label
        face_idx = np.random.randint(0, 6)
        color_name = colors[face_idx]
        bg = COLOR_HEX.get(color_name, "#ffffff")
        fg = "#000000" if color_name == "White" or bg.lower() in ["#facc15"] else "#ffffff"
        self.die_label.config(text=UNICODE_DICE[face_idx], bg=bg, fg=fg)
        self.color_label.config(text=color_name)
        self._animate_count -= 1
        if self._animate_count > 0:
            self.after(60, self._animate)
        else:
            self.after(80, self._resolve_roll)

    def _resolve_roll(self):
        # Choose final outcome based on mode probabilities
        mode = self.mode.get()
        probs = fair_probabilities if mode == "Fair" else tweaked_probabilities
        outcome = np.random.choice(colors, p=probs)
        # map color to index for display
        idx = colors.index(outcome)
        # Color the die area to match outcome
        bg = COLOR_HEX.get(outcome, "#ffffff")
        fg = "#000000" if outcome == "White" or bg.lower() in ["#facc15"] else "#ffffff"
        self.die_label.config(text=UNICODE_DICE[idx], bg=bg, fg=fg)
        self.color_label.config(text=outcome)

        bet = float(self.bet_amount.get())
        if outcome == "Red":
            payout_multiplier = 2.0 if mode == "Fair" else 1.9
            profit = bet * payout_multiplier - bet
        else:
            profit = -bet

        self.total_profit += profit
        self.plays += 1
        self.history.append(profit)
        self.outcome_history.append(outcome)

        self.profit_label.config(text=f"Total Profit: ${self.total_profit:.2f}")
        self.plays_label.config(text=f"Plays: {self.plays}")

        self.roll_btn.config(state="normal")

    def reset_game(self):
        if messagebox.askyesno("Reset", "Reset stats and history?"):
            self.total_profit = 0.0
            self.plays = 0
            self.history.clear()
            self.outcome_history.clear()
            self.profit_label.config(text=f"Total Profit: ${self.total_profit:.2f}")
            self.plays_label.config(text=f"Plays: {self.plays}")
            # reset die color to initial
            initial_bg = COLOR_HEX.get(colors[0], "#ffffff")
            initial_fg = "#000000" if colors[0] == "White" else "#ffffff"
            self.die_label.config(bg=initial_bg, fg=initial_fg, text=UNICODE_DICE[0])

    def show_plots(self):
        if not self.history:
            messagebox.showinfo("No Data", "No plays yet — roll at least once to see plots.")
            return

        df = pd.DataFrame({
            "Profit": self.history,
            "Outcome": self.outcome_history
        })

        # Profit distribution
        plt.figure(figsize=(8, 4))
        plt.hist(df["Profit"], bins=12, alpha=0.7)
        plt.title("Profit Distribution")
        plt.xlabel("Profit per Play")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

        # Cumulative profit
        plt.figure(figsize=(8, 4))
        plt.plot(pd.Series(self.history).cumsum())
        plt.title("Cumulative Profit Over Plays")
        plt.xlabel("Play Number")
        plt.ylabel("Total Profit")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = ColorDiceGame()
    app.mainloop()
