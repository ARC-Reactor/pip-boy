import tkinter as tk
import random
import subprocess
import platform
import shutil

bg_color = "#000000"
text_color = "#00FF00"
font_style = ("Courier", 10, "bold")

class SuperTicTacToe(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=bg_color)
        self.boards = [[["" for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.buttons = [[] for _ in range(9)]
        self.winner_board = [""] * 9
        self.current_player = "X"
        self.active_board = -1

        self.status_label = tk.Label(self, text="Player X's Turn", fg=text_color, bg=bg_color, font=font_style)
        self.status_label.pack(pady=5)

        self.main_frame = tk.Frame(self, bg=bg_color)
        self.main_frame.pack(padx=5, pady=5)
        self.draw_boards()

    def draw_boards(self):
        for i in range(9):
            frame = tk.Frame(self.main_frame, bg=bg_color, bd=1, relief=tk.RIDGE)
            frame.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons[i] = []
            for r in range(3):
                for c in range(3):
                    btn = tk.Button(frame, text="", width=4, height=2,
                                    font=font_style, fg=text_color, bg="#003300",
                                    command=lambda b=i, x=r, y=c: self.make_move(b, x, y))
                    btn.grid(row=r, column=c, padx=1, pady=1)
                    self.buttons[i].append(btn)

    def make_move(self, board_index, row, col):
        if self.active_board != -1 and self.active_board != board_index:
            return
        if self.boards[board_index][row][col] != "" or self.winner_board[board_index] != "":
            return

        self.boards[board_index][row][col] = self.current_player
        btn_index = row * 3 + col
        self.buttons[board_index][btn_index].config(text=self.current_player)

        if self.check_win(self.boards[board_index], self.current_player):
            self.winner_board[board_index] = self.current_player
            for b in self.buttons[board_index]:
                b.config(bg="#005500")
        elif all(self.boards[board_index][r][c] != "" for r in range(3) for c in range(3)):
            self.winner_board[board_index] = "D"

        if self.check_win_on_macroboard(self.current_player):
            self.status_label.config(text=f"Player {self.current_player} wins the game!")
            return

        self.active_board = row * 3 + col
        if self.winner_board[self.active_board] != "":
            self.active_board = -1

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s Turn")

        if self.current_player == "O":
            self.after(500, self.ai_move)

    def ai_move(self):
        board_choices = [i for i in range(9) if self.winner_board[i] == ""]
        board_index = self.active_board if self.active_board in board_choices else random.choice(board_choices)

        empty_cells = [(r, c) for r in range(3) for c in range(3)
                       if self.boards[board_index][r][c] == ""]
        if not empty_cells:
            self.active_board = -1
            return

        row, col = random.choice(empty_cells)
        self.make_move(board_index, row, col)

    def check_win(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2-i] == player for i in range(3)):
            return True
        return False

    def check_win_on_macroboard(self, player):
        macro = [self.winner_board[i] for i in range(9)]
        for i in range(3):
            if all(macro[i*3+j] == player for j in range(3)) or \
               all(macro[j*3+i] == player for j in range(3)):
                return True
        if all(macro[i] == player for i in [0,4,8]) or \
           all(macro[i] == player for i in [2,4,6]):
            return True
        return False
        




def open_linux_terminal():
    system = platform.system()
    if system != "Linux":
        terminal.insert("This feature is Linux-only.")
        return

    # List of common Linux terminal emulators to try
    terminals = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "xterm", "lxterminal"]

    for term in terminals:
        if shutil.which(term):
            subprocess.Popen([term])
            return

    terminal.insert("No supported terminal emulator found.")

class WidgetPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Widget Picker")
        self.root.geometry("800x600")
        self.root.configure(bg=bg_color)

        self.widgets = {
            "Label": self.add_label,
            "Button": self.add_button,
            "Entry": self.add_entry,
            "Super Tic Tac Toe": self.add_game,
            "Vault Terminal Emulator": self.add_terminal,
            "Mini Calculator": self.add_calculator
}


        self.create_ui()

    def create_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, width=160, bg="#111")
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Widgets", bg="#111", fg=text_color, font=("Courier", 12, "bold")).pack(pady=10)

        for name in self.widgets:
            btn = tk.Button(sidebar, text=name, command=self.widgets[name],
                            bg="#003300", fg=text_color, font=font_style)
            btn.pack(pady=5, fill="x", padx=10)

        # Main preview area
        self.preview = tk.Frame(self.root, bg=bg_color)
        self.preview.pack(side="right", fill="both", expand=True)

    def clear_preview(self):
        for widget in self.preview.winfo_children():
            widget.destroy()

    def add_label(self):
        self.clear_preview()
        tk.Label(self.preview, text="This is a Label", font=font_style,
                 bg=bg_color, fg=text_color).pack(pady=20)

    def add_button(self):
        self.clear_preview()
        tk.Button(self.preview, text="Click Me", font=font_style,
                  bg="#004400", fg=text_color).pack(pady=20)

    def add_entry(self):
        self.clear_preview()
        tk.Entry(self.preview, font=font_style, fg=text_color,
                 bg="#111", insertbackground=text_color).pack(pady=20)

    def add_game(self):
        self.clear_preview()
        game = SuperTicTacToe(self.preview)
        game.pack(expand=True, fill="both", padx=10, pady=10)
        

    def add_terminal(self):
        self.clear_preview()

        terminal = tk.Text(self.preview,
                           bg="#001100",
                           fg="#00FF00",
                           insertbackground="#00FF00",
                           font=("Courier", 10),
                           width=80, height=20,
                           wrap="word", borderwidth=0)
        terminal.pack(expand=True, fill="both", padx=10, pady=10)

        terminal.insert("end", "ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL\n")
        terminal.insert("end", "TYPE 'open terminal' TO LAUNCH A TERMINAL EMULATOR\n\n> ")
        terminal.focus_set()

        def on_enter(event):
            line_start = terminal.search(">", "end-2l linestart", "end")
            command = terminal.get(line_start + " + 2c", "end-1c").strip().lower()

            if command == "open terminal":
                terminal.insert("end", "\nBOOTING TERMINAL...\n\n> ")
                open_linux_terminal()
            else:
                terminal.insert("end", f"\nUNKNOWN COMMAND: {command}\n\n> ")

            terminal.see("end")
            return "break"

        terminal.bind("<Return>", on_enter)

   
    def add_calculator(self):
        self.clear_preview()
        calc_frame = tk.Frame(self.preview, bg=bg_color)
        calc_frame.pack(pady=20)

        entry = tk.Entry(calc_frame, font=font_style, fg=text_color, bg="#111", width=25, justify="right")
        entry.grid(row=0, column=0, columnspan=4, pady=5)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        def click(btn):
            if btn == "=":
                try:
                    result = str(eval(entry.get()))
                    entry.delete(0, "end")
                    entry.insert("end", result)
                except:
                    entry.delete(0, "end")
                    entry.insert("end", "ERROR")
            else:
                entry.insert("end", btn)

        for i, b in enumerate(buttons):
            tk.Button(calc_frame, text=b, width=5, height=2, font=font_style,
                      bg="#003300", fg=text_color, command=lambda b=b: click(b)).grid(
                row=(i//4)+1, column=i%4, padx=2, pady=2)


# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = WidgetPicker(root)
    root.mainloop()
