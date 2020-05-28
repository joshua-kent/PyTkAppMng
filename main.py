import defaultEnvironment as defEnv
from tkinter import Tk, Menu, ttk
import sys

if sys.version_info.major == 3:
    # Set up root window
    root = Tk()
    root.geometry("800x600+20+20")
    root.resizable(True, True)

    # Launch default environment
    env = defEnv.init(root)
    root.mainloop()
else:
    raise Exception("Your Python version is out of date. Please update to a newer release (recommended: 3.8)")