from tkinter import *
from tkinter.ttk import *
try:
    from .defs import *
except:
    from defs import *
import os.path

class init:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("300x600+20+20")
        self.icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png")
        self.root.iconphoto(False, ImageTk.PhotoImage(file = self.icon))
        Grid.rowconfigure(self.root, 0, weight = 1)
        Grid.columnconfigure(self.root, 0, weight = 1)
        self.root.resizable(False, False)

        style = Style()
        style.configure("calc_frame.TFrame", theme = "winnative")
        style.configure("calc_buttons.TButton", theme = "winnative", relief = "flat")
        self.frame = Frame(self.root, style = "calc_frame.TFrame")

        # maybe add loading screen

        input_box = Label(self.frame, background = "#FFFFFF")
        input_box.grid(row = 0, column = 0, columnspan = 9, sticky = E+W)
        Grid.columnconfigure(self.frame, 0, weight = 1)
        input_text = Label(self.frame, text = "in place", background = "#FFFFFF")
        input_text.grid(row = 0, column = 8, sticky = N+S+E)
        separator_1 = Separator(self.frame, orient = HORIZONTAL)
        separator_1.grid(column = 0, row = 0, columnspan = 9, sticky = N+E+W)
        separator_2 = Separator(self.frame, orient = HORIZONTAL)
        separator_2.grid(column = 0, row = 0, columnspan = 9, sticky = S+E+W)

        i = 1
        for y in range(5):
            Grid.rowconfigure(self.frame, y + 1, weight = 1)
            for x in range(8):
                Grid.columnconfigure(self.frame, x + 1, weight = 1)

                latex_text = to_latex(buttons_dict[i][0], 15)
                button = Button(self.frame, image = latex_text, compound = CENTER)
                button.img = latex_text
                button.grid(row = y + 1, column = x + 1, sticky = N+S+E+W)
                i += 1
        self.frame.grid(sticky = S)

if __name__ == "__main__":
    root = Tk()
    init(root)
    root.mainloop()