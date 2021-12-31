# importing all necessary libraries
from tkinter import *
from functools import partial
from tkinter import messagebox

from bordWars import BordWars

turn = 0
COLORX = 'hotpink'
COLORO = 'cyan'
COLOR = 'lavender'
PRESSED_X = 'deeppink'
PRESSED_O = 'turquoise2'
COLOR_BORDER2 = 'lightgray'
COLOR_BORDER1 = '#AAAAAA'


class GameGui:

    def __init__(self, width, height, second_player):
        self.bordWars = BordWars(width, height)
        self.width = width
        self.height = height
        self.second_player = second_player
        self.pressed_cell = (-1, -1)
        self.first_border = []
        self.second_border = []

    # checking how is the winner
    def check_win(self, gui):
        text = '', ''
        check_win = self.bordWars.check_win()
        if check_win == 1:
            text = "Winner", f"Player {COLORX} won the match"
        elif check_win == 2:
            text = "Winner", f"Player {COLORO} won the match"
        elif check_win == 3:
            text = "Tie Game", "Tie Game"
        if text[0] != '':
            # gui.destroy()
            messagebox.showinfo(text[0], text[1])

    # Configure text on button while playing with another player
    def get_move(self, i, j, gui, p1, p2):
        if turn % 2 == 0:
            self.update_gui(i, j, 'X', p1, p2, gui)
        else:
            if self.second_player != 'Computer':
                self.update_gui(i, j, 'O', p2, p1, gui)

    def update_gui(self, i, j, player, p1, p2, gui):
        global turn
        first_pressed = False
        pressed_color = PRESSED_X if player == 'X' else PRESSED_O
        color_player = COLORX if player == 'X' else COLORO
        if self.bordWars.board[i][j] == player:
            if self.pressed_cell == (-1, -1):
                first_pressed = True
                self.get_first_border(i, j, COLOR_BORDER1)
                self.get_second_border(i, j, COLOR_BORDER2)
                self.pressed_cell = (i, j)
                button[i][j].config(bg=pressed_color, activebackground=pressed_color)

            elif self.pressed_cell == (i, j):
                first_pressed = True
                self.delete_first_border(i, j)
                self.delete_second_border(i, j)
                self.pressed_cell = (-1, -1)
                button[i][j].config(bg=color_player, activebackground=color_player)

        if not first_pressed:
            if self.pressed_cell != (-1, -1):
                n, m = self.pressed_cell
                second_pressed = False
                if (i, j) in self.first_border:
                    second_pressed = True
                    button[n][m].config(bg=color_player, activebackground=color_player)
                elif (i, j) in self.second_border:
                    second_pressed = True
                    button[n][m].config(bg=COLOR, activebackground=COLOR)
                    self.bordWars.move(n, m)

                if second_pressed:
                    self.delete_first_border(n, m)
                    self.delete_second_border(n, m)
                    self.pressed_cell = (-1, -1)
                    button[i][j].config(bg=color_player, activebackground=color_player)
                    self.get_new_army(i, j, player)
                    turn += 1
                    p1.config(state=DISABLED)
                    p2.config(state=ACTIVE)
                    self.check_win(gui)

    # searching for neighboring opponents
    def get_new_army(self, i, j, player):
        updated = self.bordWars.update_board(i, j, player)
        color = COLORX if player == 'X' else COLORO
        for (n, m) in updated:
            button[n][m].config(bg=color, activebackground=color)

    # coloring first border of chosen cell
    def get_first_border(self, i, j, color):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j, 1)

        l = self.first_border
        # print(start_x,start_y,end_x,end_y)
        for c in range(start_y, end_y + 1):
            self.append(l, start_x, c)
            self.append(l, end_x, c)
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        self.append(l, i, start_y)
        self.append(l, i, end_y)
        self.set_color(i, start_y, color)
        self.set_color(i, end_y, color)

    # returning to default color
    def delete_first_border(self, i, j, color=COLOR):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j, 1)

        self.first_border = []
        for c in range(start_y, end_y + 1):
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        self.set_color(i, start_y, color)
        self.set_color(i, end_y, color)

    # coloring second border of chosen cell
    def get_second_border(self, i, j, color):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j, 2)
        l = self.second_border
        for c in range(start_y, end_y + 1):
            self.append(l, start_x, c)
            self.append(l, end_x, c)
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        for r in range(start_x , end_x):
            self.append(l, r, start_y)
            self.append(l, r, end_y)
            self.set_color(r, start_y, color)
            self.set_color(r, end_y, color)

    # returning to default color
    def delete_second_border(self, i, j, color=COLOR):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j, 2)
        self.second_border = []
        for c in range(start_y, end_y + 1):
            self.set_color(start_x, c, color)
            self.set_color(end_x, c, color)

        for r in range(start_x , end_x):
            self.set_color(r, start_y, color)
            self.set_color(r, end_y, color)

    # changing color in gui
    def set_color(self, i, j, color):
        if self.bordWars.board[i][j] == '-':
            if button[i][j].cget('bg') == COLOR:  # this is for setting colors for first && second border correctly
                button[i][j].config(bg=color, activebackground=color)
            if color == COLOR:  # this is for deleting color
                button[i][j].config(bg=color, activebackground=color)

    # storing available moves for 2 borders
    def append(self, l: list, i, j):
        if self.bordWars.board[i][j] == '-':
            l.append((i, j))

    # getting border indexes
    def calc_indexes(self, i, j, num):

        start_x = i - num if i - num >= 0 else 0
        end_x = i + num if i + num < self.height else self.height-1
        start_y = j - num if j - num >= 0 else 0
        end_y = j + num if j + num < self.width else self.width-1

        return start_x, end_x, start_y, end_y

    # Decide the next move of system
    def pc(self):
        pass

    # Initialize the game board to play with system / another player
    def initialize(self):

        game_board = Tk()
        # game_board.eval('tk::PlaceWindow . center')
        game_board.title("Bord Wars")

        p1 = Button(game_board, text=f"Player : pink", width=10, bg=COLOR)
        p1.pack(side='top')

        p2 = Button(game_board, text=f"{self.second_player} : {COLORO}", width=10, state=DISABLED, bg=COLOR)
        p2.pack(side='top')

        self.game_board(game_board, p1, p2)
        game_board.geometry("+200+20")
        game_board.config(bg=COLOR)
        game_board.mainloop()

    # Create the GUI of game board for play along with system / another player
    def game_board(self, game_board, p1, p2):
        global button
        button = []
        width = self.width
        height = self.height
        grid = Frame()
        for i in range(height):
            button.append(i)
            button[i] = []
            for j in range(width):
                button[i].append(j)
                get_m = partial(self.get_move, i, j, game_board, p1, p2)
                color = COLOR
                if self.bordWars.board[i][j] == 'X':
                    color = COLORX
                elif self.bordWars.board[i][j] == 'O':
                    color = COLORO

                button[i][j] = Button(grid, bd=5, command=get_m, height=2, width=5, bg=color, activebackground=color)
                button[i][j].grid(row=i, column=j)
        grid.pack(side='top')

    # def make_button(self, tk, text, command) -> Button:
    #     color_bg, color_fg, size, font = "cornflowerblue", "navy", 12, 'helvetica'  # summer font '#fe3e77', 'white'
    #
    #     button = Button(tk, text=text, command=command,
    #                     activeforeground=color_fg,
    #                     activebackground=color_bg, bg=color_bg,
    #                     fg=color_fg, width=15, font=(font, size, 'bold'), bd=5)
    #     return button
