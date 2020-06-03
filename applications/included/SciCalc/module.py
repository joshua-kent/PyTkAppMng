import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import warnings
import os.path
if __name__ == "__main__":
    raise Exception("This module cannot be run directly. Please run from PyTkAppMng/main.py")
else:
    import packages.typemathtext as tmt
    from .defs import *

class init:
    current_string = ""

    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("300x600+20+20")
        self.icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png")
        self.root.iconphoto(False, ImageTk.PhotoImage(file = self.icon))
        tk.Grid.rowconfigure(self.root, 0, weight = 1)
        tk.Grid.columnconfigure(self.root, 0, weight = 1)
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("calc_frame.TFrame", theme = "winnative")
        style.configure("calc_buttons.TButton", theme = "winnative", relief = "flat")
        self.frame = ttk.Frame(self.root, style = "calc_frame.TFrame")

        input_box = tk.Label(self.frame, background = "#FFFFFF")
        input_box.grid(row = 0, column = 0, columnspan = 9, sticky = "ew")
        tk.Grid.columnconfigure(self.frame, 0, weight = 1)
        self.input_text = tk.Label(self.frame, text = "", background = "#FFFFFF", anchor = "e")
        self.input_text.grid(row = 0, column = 0, columnspan = 9, sticky = "nsew")
        separator_1 = ttk.Separator(self.frame, orient = tk.HORIZONTAL)
        separator_1.grid(column = 0, row = 0, columnspan = 9, sticky = "new")
        separator_2 = ttk.Separator(self.frame, orient = tk.HORIZONTAL)
        separator_2.grid(column = 0, row = 0, columnspan = 9, sticky = "sew")

        i = 1
        for y in range(5):
            tk.Grid.rowconfigure(self.frame, y + 1, weight = 1)
            for x in range(8):
                tk.Grid.columnconfigure(self.frame, x + 1, weight = 1)

                latex_text = tmt.to_latex(buttons_dict[i][0], 15)
                button = ttk.Button(self.frame, image = latex_text, compound = tk.CENTER,
                                    command = lambda i=i: self.button_clicked(buttons_dict[i][1]))
                button.img = latex_text
                button.grid(row = y + 1, column = x + 1, sticky = "nsew")
                i += 1
        self.frame.grid(sticky = "s")

    def button_clicked(self, button_text):
        self.input_text["text"] += button_text # need to add to this


if __name__ == "__main__":
    root = tk.Tk()
    init(root)
    root.mainloop()