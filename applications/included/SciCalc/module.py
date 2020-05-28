from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import packages.typemathtext as typemathtext
import warnings
try:
    from .defs import *
except:
    from defs import *
import os.path

class init:
    current_string = ""

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

        input_box = Label(self.frame, background = "#FFFFFF")
        input_box.grid(row = 0, column = 0, columnspan = 9, sticky = E+W)
        Grid.columnconfigure(self.frame, 0, weight = 1)
        self.input_text = Label(self.frame, text = "", background = "#FFFFFF", anchor = E)
        self.input_text.grid(row = 0, column = 0, columnspan = 9, sticky = N+S+E+W)
        separator_1 = Separator(self.frame, orient = HORIZONTAL)
        separator_1.grid(column = 0, row = 0, columnspan = 9, sticky = N+E+W)
        separator_2 = Separator(self.frame, orient = HORIZONTAL)
        separator_2.grid(column = 0, row = 0, columnspan = 9, sticky = S+E+W)

        i = 1
        for y in range(5):
            Grid.rowconfigure(self.frame, y + 1, weight = 1)
            for x in range(8):
                Grid.columnconfigure(self.frame, x + 1, weight = 1)

                latex_text = typemathtext.to_latex(buttons_dict[i][0], 15)
                button = Button(self.frame, image = latex_text, compound = CENTER,
                command = lambda i=i: self.button_clicked(buttons_dict[i][1]))
                button.img = latex_text
                button.grid(row = y + 1, column = x + 1, sticky = N+S+E+W)
                i += 1
        self.frame.grid(sticky = S)

    def button_clicked(self, button_text):
        self.input_text["text"] += button_text # need to add to this


if __name__ == "__main__":
    root = Tk()
    init(root)
    new = typemathtext.text()
    new.edit("hi", 3, 4)
    root.mainloop()