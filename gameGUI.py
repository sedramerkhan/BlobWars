# importing all necessary libraries
import time
from functools import partial
from tkinter import *
from tkinter import messagebox

from bordWars import BordWars
from minmax import minmax

COLORX = "hotpink"
COLORO = "cyan"
COLOR = "lavender"
PRESSED_X = "deeppink"
PRESSED_O = "turquoise2"
COLOR_BORDER2 = "lightgray"
COLOR_BORDER1 = "#AAAAAA"


class GameGui:
    def __init__(self, width, height, second_player, level):
        self.bordWars = BordWars(width, height, "X")
        self.width = width
        self.height = height
        self.second_player = second_player
        self.pressed_cell = None
        self.buttons = []
        self.level = level

    # checking how is the winner
    def check_win(self, gui,p1,p2):
        text = "", ""
        check_win,count1,count2 = self.bordWars.check_win()
        if check_win == 1:
            text = "Winner", f"Player {COLORX} won the match"
        elif check_win == 2:
            text = "Winner", f"Player {COLORO} won the match"
        elif check_win == 3:
            text = "Tie Game", "Tie Game"
        if text[0] != "":
            # gui.destroy()
            messagebox.showinfo(text[0], text[1])
        p2.config(text=f'Player: {count1} pink')
        p1.config(text=f'{self.second_player}: {count2} cyan')

    # Configure button color while playing with another player
    def get_move(self, i, j, gui, p1, p2):
        self.update_gui(i, j, p2, p1, gui)

    def update_gui(self, i, j, p1, p2, gui):
        button = self.buttons
        player = self.bordWars.player
        pressed_color = PRESSED_X if player == "X" else PRESSED_O
        color_player = COLORX if player == "X" else COLORO
        p11 = p1 if player == 'O' else p2
        p22 = p2 if player == 'O' else p1

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
                self.delete_first_border(n, m)
                self.delete_second_border(n, m)
                self.pressed_cell = None

                for (n, m) in updated + [(i, j), (n, m)]:
                    self.update_color_at(n, m)

                self.check_win(gui,p1,p2)

                if self.second_player == 'Computer':
                    minax_res = minmax(self.bordWars, self.level, self.bordWars.player, True)
                    print("this is minmax_res",minax_res)
                    fromm, to = minax_res[0]
                    print("this is from , to ", fromm, to)
                    (n, m), (i, j) = fromm, to
                    updated = self.bordWars.move(n, m, i, j)
                    for (n, m) in updated + [(i, j), (n, m)]:
                        self.update_color_at(n, m)
                    self.check_win(gui,p1,p2)
                else:
                    p11.config(state=DISABLED)
                    p22.config(state=ACTIVE, activebackground=COLOR)

            except ValueError as e:
                print("error", e)
                pass

    # returning to default color
    def delete_first_border(self, i, j, color=COLOR):
        first_boarder = self.bordWars.get_boarder(i, j, 1)
        for cell in first_boarder:
            self.set_color(cell[0], cell[1], color)

    # returning to default color
    def delete_second_border(self, i, j, color=COLOR):
        second_border = self.bordWars.get_boarder(i, j, 2)
        for cell in second_border:
            self.set_color(cell[0], cell[1], color)

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
    def update_color_at(self, i, j):
        if self.bordWars.board[i][j] == "X":
            color = COLORX
        elif self.bordWars.board[i][j] == "O":
            color = COLORO
        else:
            color = COLOR
        self.buttons[i][j].config(bg=color, activebackground=color)

    # Initialize the game board to play with system / another player
    def initialize(self):

        game_board = Tk()
        # game_board.eval('tk::PlaceWindow . center')
        game_board.title("Bord Wars")

        p1 = Button(game_board, text=f"Player: pink", width=13, bg=COLOR)
        p1.pack(side="top")

        p2 = Button(
            game_board,
            text=f"{self.second_player}: {COLORO}",
            width=13,
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
