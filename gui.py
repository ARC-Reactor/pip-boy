import tkinter as tk
from tkinter import messagebox

# Globals
current_player = "X"
board = [""] * 9
buttons = []

# Colors
bg_color = "#013220"
fg_color = "#00FF00"
btn_bg = "#004d00"
active_bg = "#005500"

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe vs AI")
root.configure(bg=bg_color)
root.geometry("320x380")

def check_winner():
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diagonals
    ]
    for combo in win_conditions:
        a, b, c = combo
        if board[a] == board[b] == board[c] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def ai_move():
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            buttons[i].config(text="O")
            break

def make_move(i):
    global current_player
    if board[i] == "" and current_player == "X":
        board[i] = "X"
        buttons[i].config(text="X")
        winner = check_winner()
        if winner:
            handle_result(winner)
            return
        current_player = "O"
        root.after(500, ai_turn)  # Delay AI move for realism

def ai_turn():
    global current_player
    ai_move()
    winner = check_winner()
    if winner:
        handle_result(winner)
        return
    current_player = "X"

def handle_result(winner):
    if winner == "Draw":
        messagebox.showinfo("Game Over", "It's a draw!")
    else:
        messagebox.showinfo("Game Over", f"{winner} wins!")
    reset_board()

def reset_board():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    for btn in buttons:
        btn.config(text="")

# Create 3x3 grid of buttons
for i in range(9):
    btn = tk.Button(root, text="", font=('Arial', 20), width=5, height=2,
                    bg=btn_bg, fg=fg_color, activebackground=active_bg,
                    command=lambda i=i: make_move(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Restart Button
restart_btn = tk.Button(root, text="Restart", font=('Arial', 12),
                        command=reset_board,
                        bg=btn_bg, fg=fg_color, activebackground=active_bg)
restart_btn.grid(row=3, column=0, columnspan=3, pady=10)

# Start GUI
root.mainloop()
