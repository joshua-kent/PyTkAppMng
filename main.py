import defaultEnvironment as defEnv
from tkinter import Tk, Menu, ttk

__version__ = defEnv.__version__
print("PyTk Application Manager {}".format(__version__))

# Set up root window
root = Tk()
root.geometry("800x600+20+20")
root.resizable(True, True)
root.title("PyTk Application Manager {}".format(__version__))

# Launch default environment
defEnv.init(root)

root.mainloop()