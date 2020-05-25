import defaultEnvironment as defEnv
from tkinter import Tk, Menu, ttk

# Set up root window
root = Tk()
root.geometry("800x600+20+20")
root.resizable(True, True)

# Launch default environment
defEnv.init(root)

root.mainloop()