import tkinter as tk
from tkinter import messagebox
from othello import *


class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello Game")

        # Mac-specific menu bar configuration
        if root.tk.call('tk', 'windowingsystem') == 'aqua':
            root.createcommand('tk::mac::Quit', root.quit)

        self.board = list(INITIAL_STATE)
        self.current_player = 'X'
        self.buttons = []

        # Create game info frame
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=10)

        self.player_label = tk.Label(self.info_frame,
                                     text="Current Player: X",
                                     font=('Helvetica', 12))
        self.player_label.pack()

        self.score_label = tk.Label(self.info_frame,
                                    text="Score - X: 2  O: 2",
                                    font=('Helvetica', 12))
        self.score_label.pack()

        # Create board frame
        self.board_frame = tk.Frame(root, bg='gray')
        self.board_frame.pack(padx=20, pady=20)

        # Create the game board buttons
        for i in range(8):
            row = []
            for j in range(8):
                # Create a frame for each cell to handle the background
                cell_frame = tk.Frame(self.board_frame,
                                      width=50,
                                      height=50,
                                      bg='forest green')
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell_frame.grid_propagate(False)  # Maintain frame size

                # Create button within the frame
                button = tk.Button(cell_frame,
                                   width=3,
                                   height=1,
                                   font=('Helvetica', 14, 'bold'),
                                   relief='flat',
                                   borderwidth=0,
                                   highlightthickness=0,
                                   command=lambda r=i, c=j: self.make_move(r, c))
                button.place(relx=0.5, rely=0.5, anchor='center')
                row.append((button, cell_frame))
            self.buttons.append(row)

        self.update_board()

        # Center window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def update_board(self):
        """Update the visual representation of the board"""
        for i in range(8):
            for j in range(8):
                button, frame = self.buttons[i][j]
                text = self.board[i][j]

                # Reset button appearance
                button.configure(
                    text='',
                    bg='forest green',
                    fg='black'
                )

                if text == 'X':
                    button.configure(
                        text='⚫',  # Black circle
                        bg='forest green',
                        fg='black'
                    )
                elif text == 'O':
                    button.configure(
                        text='⚪',  # White circle
                        bg='forest green',
                        fg='white'
                    )
                frame.configure(bg='forest green')

        # Update score
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        self.score_label.configure(
            text=f"Score - X: {x_count}  O: {o_count}"
        )
        self.player_label.configure(
            text=f"Current Player: {self.current_player}"
        )

    def make_move(self, row, col):
        """Handle player moves"""
        if self.current_player != 'X':  # Only allow moves when it's player's turn
            return

        moves = legal_moves(self.board, self.current_player)
        if moves == ['pass']:
            self.handle_pass()
            return

        if (row, col) not in moves:
            messagebox.showwarning("Invalid Move",
                                   "That move is not legal!")
            return

        self.board = list(successor(self.board,
                                    self.current_player,
                                    (row, col)))
        self.update_board()
        self.current_player = opposite(self.current_player)
        self.root.after(500, self.computer_turn)

    def computer_turn(self):
        """Handle computer's turn"""
        if self.current_player != 'O':
            return

        moves = legal_moves(self.board, self.current_player)
        if not moves:
            self.game_over()
            return

        if moves == ['pass']:
            self.handle_pass()
            return

        move = best_move(self.board, self.current_player, 3)
        self.board = list(successor(self.board,
                                    self.current_player,
                                    move))
        self.update_board()
        self.current_player = opposite(self.current_player)

        # Check if game is over after computer's move
        if not legal_moves(self.board, self.current_player):
            self.game_over()

    def handle_pass(self):
        """Handle when a player must pass"""
        messagebox.showinfo("Pass",
                            f"Player {self.current_player} must pass!")
        self.current_player = opposite(self.current_player)
        if self.current_player == 'X':
            self.root.after(500, self.computer_turn)

    def game_over(self):
        """Handle game over state"""
        final_score = score(self.board)
        if final_score > 0:
            winner = "X wins!"
        elif final_score < 0:
            winner = "O wins!"
        else:
            winner = "It's a tie!"

        messagebox.showinfo("Game Over", winner)
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGUI(root)
    root.mainloop()