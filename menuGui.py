from functools import partial
from tkinter import *

from gameGUI import GameGui


class MenuGUI:

    def __init__(self):
        self.menu = Tk()
        menu = self.menu
        # menu.eval('tk::PlaceWindow . center ')
        menu.geometry("350x350+500+100")
        menu.config(bg="snow")
        menu.title("Bord Wars")
        entry_frame = self.initialize_enties()

        head = Label(menu, text="Welcome to Bord Wars Game", bg="snow", fg="black", font='Times 15', height=3)
        B1 = self.make_button(menu, "Single Player", partial(self.play, "Compter"))
        B2 = self.make_button(menu, "Multi Player", partial(self.play, "Player 2"))
        B3 = self.make_button(menu, "Exit", menu.quit)

        head.pack(side='top')
        entry_frame.pack(side='top')
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
        self.menu.destroy()

        game = GameGui(width, height, second_player)
        game.initialize()

    def initialize_enties(self):
        entry_frame = Frame(self.menu, bg='snow')
        self.e1 = Entry(entry_frame, width=5)
        self.e2 = Entry(entry_frame, width=5)
        text = Label(entry_frame, text="Enter width and height ", bg="snow", fg="black", font='Times 15', height=3)
        text.pack(side='left')
        self.e1.pack(side='left', padx=15, pady=5)
        self.e2.pack(side='left')
        return entry_frame


# Call main function
if __name__ == '__main__':
    menu = MenuGUI()
