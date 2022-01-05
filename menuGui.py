import tkinter
from functools import partial
from tkinter import *

from gameGUI import GameGui


class MenuGUI:

    def __init__(self):
        self.menu = Tk()
        self.enable_var = tkinter.IntVar()
        menu = self.menu
        # menu.eval('tk::PlaceWindow . center ')
        menu.geometry("350x350+500+100")
        menu.config(bg="snow")
        menu.title("Bord Wars")
        entry_frame = self.initialize_entries()
        level = self.initialize_level_entry()
        head = Label(menu, text="Welcome to Bord Wars Game", bg="snow", fg="black", font='Times 15', height=3)
        B1 = self.make_button(menu, "Single Player", partial(self.play, "Computer"))
        B2 = self.make_button(menu, "Multi Player", partial(self.play, "Player 2"))
        B3 = self.make_button(menu, "Exit", menu.quit)

        head.pack(side='top')
        entry_frame.pack(side='top', pady=5)
        level.pack(side='top', fill=BOTH, pady=8)
        Checkbutton(menu, text="enable alpha-beta cut", variable=self.enable_var, font='Times 15', ) \
            .pack(side=TOP)
        B1.pack(side='top')
        B2.pack(side='top', pady=5)
        B3.pack(side='top')
        menu.mainloop()

    def make_button(self, tk, text, command) -> Button:
        color_bg, color_fg, size, font = "cornflowerblue", "navy", 12, 'helvetica'  # summer font '#fe3e77', 'white'

        button = Button(tk, text=text, command=command,
                        activeforeground=color_fg,
                        activebackground=color_bg, bg=color_bg,
                        fg=color_fg, width=15, font=(font, size, 'bold'), bd=5)
        return button

    # main function
    def play(self, second_player):
        width = self.e1.get()
        width = int(width) if width != "" and width.isdecimal() else 10

        height = self.e2.get()
        height = int(height) if height != "" and height.isdecimal() else 10

        level = self.e3.get()
        level = int(level) if level != "" and level.isdecimal() else 1
        enable = self.enable_var.get()
        self.menu.destroy()
        game = GameGui(width, height, second_player, level,enable)
        game.initialize()

    def initialize_entries(self):
        entry_frame = Frame(self.menu, bg='snow')
        self.e1 = Entry(entry_frame, width=5)
        self.e2 = Entry(entry_frame, width=5)
        text = Label(entry_frame, text="Enter width and height ", bg="snow", fg="black", font='Times 15')
        text.pack(side='left')
        self.e1.pack(side='left', padx=15)
        self.e2.pack(side='left')
        return entry_frame

    def initialize_level_entry(self):
        canvas = Canvas(self.menu, height=30, bg='snow', highlightthickness=0)
        text = Label(text="Enter The Game Level ", bg="snow", fg="black", font='Times 15')
        canvas.create_window(125, 5, window=text)
        self.e3 = Entry(width=5)
        canvas.create_window(275, 5, window=self.e3)
        return canvas


# Call main function
if __name__ == '__main__':
    menu = MenuGUI()
