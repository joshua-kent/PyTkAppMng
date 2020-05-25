from tkinter import *
from tkinter.ttk import *

def init(root):
    root.title("Scientific Calculator")
    root.geometry("400x600+20+20")
    root.resizable(False, False)
    style = Style()
    style.configure("TFrame", theme = "winnative")
    style.configure("TButton", theme = "winnative")
    frame = Frame(root)
    
    for i in range(10):
        btn = Button(frame, style = "TButton", text = (i + 1))
        btn.grid()
    frame.grid()

if __name__ == "__main__":
    root = Tk()
    init(root)
    root.mainloop()