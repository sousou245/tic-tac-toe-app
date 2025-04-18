import tkinter as tk
from tkinter import messagebox, ttk
from database import (
    get_or_create_player,
    update_score,
    save_game_history,
    get_leaderboard,
    get_player_history,
)
from game_logic import check_winner
import random
from style import apply_style

class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        apply_style(self.root)  # Apply custom styles
        self.player_name = ""
        self.board = [""] * 9
        self.current_player = "X"
        self.buttons = []

    def run(self):
        self.show_start_screen()
        self.root.mainloop()

    def show_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Tic Tac Toe",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2C3E50",
        ).pack(pady=10)

        leaderboard = get_leaderboard()
        tk.Label(
            self.root,
            text="Leaderboard:",
            font=("Arial", 18),
            fg="white",
            bg="#2C3E50",
        ).pack()

        leaderboard_frame = tk.Frame(self.root, bg="#2C3E50")
        leaderboard_frame.pack(pady=10)

        for player in leaderboard:
            tk.Label(
                leaderboard_frame,
                text=f"{player['name']}: {player['score']} points",
                font=("Arial", 16),
                fg="white",
                bg="#34495e",
                anchor="w",
                padx=20,
            ).pack(fill="x", pady=3)

        tk.Label(
            self.root,
            text="Enter your name:",
            font=("Arial", 16),
            fg="white",
            bg="#2C3E50",
        ).pack(pady=10)

        name_entry = tk.Entry(self.root, font=("Arial", 14))
        name_entry.pack(pady=5)

        def start_game():
            self.player_name = name_entry.get().strip()
            if not self.player_name:
                messagebox.showerror("Error", "Please enter your name.")
                return

            get_or_create_player(self.player_name)
            self.show_game_screen()

        tk.Button(
            self.root,
            text="Start Game",
            command=start_game,
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            relief="solid",
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="View Game History",
            command=self.show_history_screen,
            font=("Arial", 16, "bold"),
            bg="#2C3E50",
            fg="white",
            relief="solid",
        ).pack(pady=10)

    def show_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board = [""] * 9
        self.current_player = "X"

        tk.Label(
            self.root,
            text=f"Player: {self.player_name}",
            font=("Arial", 16),
            fg="white",
            bg="#2C3E50",
        ).pack(pady=10)

        grid_frame = tk.Frame(self.root, bg="#34495e")
        grid_frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                grid_frame,
                text="",
                font=("Arial", 20),
                width=5,
                height=2,
                command=lambda i=i: self.make_move(i),
                relief="solid",
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.status_label = tk.Label(
            self.root, text="Your turn!", font=("Arial", 14), fg="white", bg="#2C3E50"
        )
        self.status_label.pack(pady=10)

    def make_move(self, index):
        if self.board[index] or self.current_player != "X":
            return

        self.board[index] = "X"
        self.buttons[index].config(text="X")

        if check_winner(self.board):
            self.end_game(self.player_name)
            return

        self.current_player = "O"
        self.status_label.config(text="Computer's turn...")
        self.root.after(1000, self.computer_move)

    def computer_move(self):
        empty_indices = [i for i, val in enumerate(self.board) if val == ""]
        if empty_indices:
            index = random.choice(empty_indices)
            self.board[index] = "O"
            self.buttons[index].config(text="O")

        if check_winner(self.board):
            self.end_game("Computer")
            return

        self.current_player = "X"
        self.status_label.config(text="Your turn!")

    def end_game(self, winner):
        if winner == self.player_name:
            update_score(self.player_name, 1)
            save_game_history(self.player_name, self.board, winner)
            messagebox.showinfo("Game Over", "You win!")
        elif winner == "Computer":
            save_game_history(self.player_name, self.board, winner)
            messagebox.showinfo("Game Over", "You lose!")
        else:
            save_game_history(self.player_name, self.board, "Draw")
            messagebox.showinfo("Game Over", "It's a draw!")

        self.show_start_screen()

    def show_history_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Game History for {self.player_name}",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2C3E50",
        ).pack(pady=10)

        history = get_player_history(self.player_name)
        if not history:
            tk.Label(
                self.root,
                text="No game history found.",
                font=("Arial", 16),
                fg="white",
                bg="#2C3E50",
            ).pack(pady=10)
        else:
            history_frame = tk.Frame(self.root, bg="#2C3E50")
            history_frame.pack(pady=10)

            tree = ttk.Treeview(
                history_frame, columns=("Board", "Winner"), show="headings", height=10
            )
            tree.heading("Board", text="Board")
            tree.heading("Winner", text="Winner")
            tree.column("Board", anchor="center")
            tree.column("Winner", anchor="center")
            tree.pack()

            for game in history:
                tree.insert("", "end", values=(str(game["board"]), game["winner"]))

        def back_to_menu():
            self.show_start_screen()

        tk.Button(
            self.root,
            text="Back to Menu",
            command=back_to_menu,
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            relief="solid",
        ).pack(pady=10)

if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()
