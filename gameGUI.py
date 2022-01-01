# importing all necessary libraries
from functools import partial
from tkinter import *
from tkinter import messagebox

from bordWars import BordWars

turn = 0
COLORX = "hotpink"
COLORO = "cyan"
COLOR = "lavender"
PRESSED_X = "deeppink"
PRESSED_O = "turquoise2"
COLOR_BORDER2 = "lightgray"
COLOR_BORDER1 = "#AAAAAA"


class GameGui:
    def __init__(self, width, height, second_player):
        self.bordWars = BordWars(width, height, "X")
        self.width = width
        self.height = height
        self.second_player = second_player
        self.pressed_cell = None
        self.buttons = []

    # checking how is the winner
    def check_win(self, gui):
        text = "", ""
        check_win = self.bordWars.check_win()
        if check_win == 1:
            text = "Winner", f"Player {COLORX} won the match"
        elif check_win == 2:
            text = "Winner", f"Player {COLORO} won the match"
        elif check_win == 3:
            text = "Tie Game", "Tie Game"
        if text[0] != "":
            # gui.destroy()
            messagebox.showinfo(text[0], text[1])

    # Configure text on button while playing with another player
    def get_move(self, i, j, gui, p1, p2):

        self.update_gui(i, j, p2, p1, gui)

    def update_gui(self, i, j, p1, p2, gui):
        button = self.buttons
        player = self.bordWars.player
        pressed_color = PRESSED_X if player == "X" else PRESSED_O
        color_player = COLORX if player == "X" else COLORO
        if self.bordWars.board[i][j] == player:
            if not self.pressed_cell:
                self.pressed_cell = (i, j)
                first_boarder = self.bordWars.get_boarder(i, j, 1)
                for cell in first_boarder:
                    self.set_color(cell[0], cell[1], COLOR_BORDER1)
                second_border = self.bordWars.get_boarder(i, j, 2)
                for cell in second_border:
                    self.set_color(cell[0], cell[1], COLOR_BORDER2)
                button[i][j].config(bg=pressed_color, activebackground=pressed_color)

            elif self.pressed_cell == (i, j):
                self.pressed_cell = None
                self.delete_first_border(i, j)
                self.delete_second_border(i, j)
                self.pressed_cell = None
                button[i][j].config(bg=color_player, activebackground=color_player)
        elif self.pressed_cell:
            n, m = self.pressed_cell
            try:
                updated = self.bordWars.move(n, m, i, j)
            # if (i, j) in first_border:
            #     second_pressed = True
            # elif (i, j) in second_border:
            #     second_pressed = True
            #     self.bordWars.move(n, m)
                self.delete_first_border(n, m)
                self.delete_second_border(n, m)
                self.pressed_cell = None
                button[i][j].config(bg=color_player, activebackground=color_player)
                for (n, m) in updated + [(i,j),(n,m)]:
                    self.update_color_at(n,m)

                p1.config(state=DISABLED)
                p2.config(state=ACTIVE)
                self.check_win(gui)
            except:
                print("error")
                pass

    # returning to default color
    def delete_first_border(self, i, j, color=COLOR):
        start_x, end_x, start_y, end_y = self.bordWars.calc_indexes(i, j, 1)

        self.first_border = []
        for c in range(start_y, end_y + 1):
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        self.set_color(i, start_y, color)
        self.set_color(i, end_y, color)

    # coloring second border of chosen cell

    # returning to default color
    def delete_second_border(self, i, j, color=COLOR):
        start_x, end_x, start_y, end_y = self.bordWars.calc_indexes(i, j, 2)
        self.second_border = []
        for c in range(start_y, end_y + 1):
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        for r in range(start_x, end_x):
            self.set_color(r, start_y, color)
            self.set_color(r, end_y, color)

    # changing color in gui
    def set_color(self, i, j, color):
        button = self.buttons
        if self.bordWars.board[i][j] == "-":
            if (
                button[i][j].cget("bg") == COLOR
            ):  # this is for setting colors for first && second border correctly
                button[i][j].config(bg=color, activebackground=color)
            if color == COLOR:  # this is for deleting color
                button[i][j].config(bg=color, activebackground=color)

    # Decide the next move of system
    def update_color_at(self,i,j):
        if self.bordWars.board[i][j] == "X":
            color = COLORX
        elif self.bordWars.board[i][j] == "O":
            color = COLORO
        else:
            color = COLOR
        self.buttons[i][j]["bg"] = color 
    def pc(self):
        pass

    # Initialize the game board to play with system / another player
    def initialize(self):

        game_board = Tk()
        # game_board.eval('tk::PlaceWindow . center')
        game_board.title("Bord Wars")

        p1 = Button(game_board, text=f"Player : pink", width=10, bg=COLOR)
        p1.pack(side="top")

        p2 = Button(
            game_board,
            text=f"{self.second_player} : {COLORO}",
            width=10,
            state=DISABLED,
            bg=COLOR,
        )
        p2.pack(side="top")

        self.game_board(game_board, p1, p2)
        game_board.geometry("+200+20")
        game_board.config(bg=COLOR)
        game_board.mainloop()

    # Create the GUI of game board for play along with system / another player
    def game_board(self, game_board, p1, p2):
        button = self.buttons
        width = self.width
        height = self.height
        grid = Frame(game_board)
        for i in range(height):
            button.append(i)
            button[i] = []
            for j in range(width):
                button[i].append(j)
                get_m = partial(self.get_move, i, j, game_board, p1, p2)
                color = COLOR
                if self.bordWars.board[i][j] == "X":
                    color = COLORX
                elif self.bordWars.board[i][j] == "O":
                    color = COLORO

                button[i][j] = Button(
                    grid,
                    bd=5,
                    command=get_m,
                    height=2,
                    width=5,
                    bg=color,
                    activebackground=color,
                )
                button[i][j].grid(row=i, column=j)
        grid.pack(side="top")