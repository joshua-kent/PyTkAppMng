# Important information:
# If user defaults need to be imported, do so by changing setup_defaults()
# Imported modules should have an info.json file that contains title, version, author anddefault arguments
# Imported modules must be placed in useropts or included
# If the init() function requires arguments, put the defaults in a variable "default_args" in its __init__.py


import os.path
import inspect
from .defs import *
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from functools import partial

global frame
__version__ = "prerelease3 2020-05-26 20:42 BST"

if not os.path.isfile(user_defaults):
    file = open(user_defaults, "w+") # if the file does not exist, it is opened (creating it)
    file.close()

def init(root):
    global frame # frame refers to global frame (so other functions can access it)

    # set up (for after an application)
    root.title("PyTk Application Manager {}".format(__version__))
    icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png")
    root.iconphoto(False, ImageTk.PhotoImage(file = icon))
    root.geometry("800x600+20+20")
    Grid.rowconfigure(root, 0, weight = 0)
    Grid.columnconfigure(root, 0, weight = 0)
    for item in root.winfo_children(): # for each frame, widget etc in root
        item.destroy() # destroy it (to clear the window)

    # creates menubar
    menu = Menu(root)
    root.config(menu = menu)

    # creates file menu
    file = Menu(menu, tearoff = 0) # creates a new menu called file
    file.add_command(label = "Import")
    file.add_command(label = "Return to selection screen", command = lambda: init(root))
    file.insert_separator(2) # adds a separator after second command
    file.add_command(label = "Exit", command = exit) # adds command to "File"
    menu.add_cascade(label = "File", menu = file) # Creates "File" on window

    # creates settings menu
    settings = Menu(menu, tearoff = 0)
    settings.add_command(label = "Change colour", command = lambda: recolour(root, style))
    settings.add_command(label = "Save current colour as default",
                        command = lambda: edit_settings(user_defaults, "background", root.cget("background")))
    settings.insert_separator(2)
    settings.add_command(label = "Reset all to default", command = lambda: reset_all_defaults(root, style))
    menu.add_cascade(label = "Settings", menu = settings)

    # ttk style
    style = Style()
    style.configure("frame.TFrame", theme = "winnative") # frame
    style.configure("defEnv.TButton", theme = "winnative", relief = "flat") # buttons

    setup_defaults(root, style) # sets up all needed info and sets them accordingly

    # create frame
    frame = Frame(root, style = "frame.TFrame")

    # Add included apps buttons
    x = 0
    y = 0
    for key, value in included_apps_info.items():
        title = value["title"]
        version = value["version"]
        author = value["author"]
        directory = value["directory"]
        icon = value["icon"]
        default_args = value["default_args"]
        if icon != None: # if icon is not equal to None 
            icon = Image.open(icon)
            icon = icon.resize((66, 66), Image.ANTIALIAS)

        # add buttons
        btn = Button(frame, style = "defEnv.TButton")
        if icon == 'None':
            btn.img = PhotoImage()
        else:
            btn.img = ImageTk.PhotoImage(icon) 
        btn.config(image = btn.img, compound = CENTER, command =
                    partial(run_module, key, root, frame))
        btn.grid(padx = 2, column = x, row = y, sticky = "nswe")
        # add label below
        lbl = Label(frame, text = title)
        lbl.config(anchor = CENTER)
        lbl.grid(column = x, row = y + 1, pady = 2, sticky = "nswe") # ipady adds padding inside of the button, adding height
        # makes sure all the squares are at least size 30x30 (labels are always 1 above y, so are excluded)
        frame.grid_columnconfigure(x, minsize = 60)
        frame.grid_rowconfigure(y, minsize = 76)
        frame.grid(sticky = "nw")
        
        # makes sure they are in the right order (when x becomes 4, it becomes 0 and y adds one)
        x = (x + 1) % 4
        if x == 0:
            y += 2
    del x, y, title, version, author, directory, default_args, icon, key, value # optimised cleanup