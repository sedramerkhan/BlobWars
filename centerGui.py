import tkinter  # Python 3

def center(root):
    """
    centers a tkinter window
    :param root: the main window or Toplevel window to center
    """
    root.update_idletasks()
    width = root.winfo_width()
    frm_width = root.winfo_rootx() - root.winfo_x()
    win_width = width + 2 * frm_width
    height = root.winfo_height()
    titlebar_height = root.winfo_rooty() - root.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = root.winfo_screenwidth() // 2 - win_width // 2
    y = root.winfo_screenheight() // 2 - win_height // 2 - 200
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.deiconify()

if __name__ == '__main__':
    root = tkinter.Tk()
    root.attributes('-alpha', 0.0)
    menubar = tkinter.Menu(root)
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    frm = tkinter.Frame(root, bd=4, relief='raised')
    frm.pack(fill='x')
    lab = tkinter.Label(frm, text='Hello World!', bd=4, relief='sunken')
    lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
    center(root)
    root.attributes('-alpha', 1.0)
    root.mainloop()