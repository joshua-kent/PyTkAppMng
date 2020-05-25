from tkinter import *
from tkinter.ttk import *

def init(root):
    print(root)
    style = Style()
    style.configure("TFrame", theme = "winnative")
    style.configure("TButton", theme = "winnative")
    frame = Frame(root)
    btn = Button(frame, text = "hello!", style = "TButton").grid()
    frame.grid()