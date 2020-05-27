'''
Information:
If user defaults need to be imported, do so by changing setup_defaults()
Imported modules should have an info.json file that contains title, version, author anddefault arguments
Imported modules must be placed in useropts or included
If the init() function requires arguments, put the defaults in a variable "default_args" in its __init__.py
As functions are likely to have a lot of temporary variables, this can be avoided in functions, unless it helps avoid confusion.
such as 'key' or 'value', are excluded)
This is to avoid overrided needed variables and avoid confusion
Use snake_case
del _this_variable should be used to delete these temporary variables if you wish
'''

import os.path
import sys
import json
import inspect
from tkinter import *
from tkinter import colorchooser
from tkinter.ttk import *
from PIL import Image, ImageTk
from functools import partial

__version__ = "prerelease2.5.1 2020-05-27 17:16 BST"

class init:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    env_icon = os.path.join(current_dir, "icon.png")
    pytkappmng_dir = os.path.dirname(current_dir)
    included = os.path.join(pytkappmng_dir, "included")
    added = os.path.join(pytkappmng_dir, "added")
    user_defaults = os.path.join(current_dir, "user_defaults.json")
    
    included_apps_dirs = []
    included_apps_info = {}
    amount_of_included_apps = 0

    added_apps_dirs = []
    added_apps_info = {}
    amount_of_added_apps = 0

    def __init__(self, root):

        for files in os.walk(self.included):
            _root = files[0] # this will always be a directory, see os.walk()
            if os.path.dirname(_root) == self.included:
                split_list = _root.split("\\")
                if "__pycache__" not in split_list:
                    self.included_apps_dirs.append(_root)
        self.amount_of_included_apps = len(self.included_apps_dirs)

        for files in os.walk(self.added):
            _root = files[0]
            if os.path.dirname(_root) == self.added:
                split_list = _root.split("\\")
                if "__pycache__" not in split_list:
                    self.added_apps_dirs.append(_root)
        self.amount_of_added_apps = len(self.added_apps_dirs)

        for i in range(self.amount_of_included_apps + self.amount_of_added_apps):
            if i < self.amount_of_included_apps:
                split_dir = self.included_apps_dirs[i].split("\\")
                module = split_dir[len(split_dir) - 1]
                info_json_directory = os.path.join(self.included_apps_dirs[i], "info.json")
            else:
                split_dir = self.added_apps_dirs[i - self.amount_of_included_apps].split("\\")
                module = split_dir[len(split_dir) - 1]
                info_json_directory = os.path.join(self.added_apps_dirs[i - self.amount_of_included_apps])
            
            try:
                with open(info_json_directory, "r") as f:
                    info = json.load(f)
            except:
                info = {}
            try:
                title = info["title"]
            except:
                title = None
            try:
                version = info["version"]
            except:
                version = None
            try:
                author = info["author"]
            except:
                author = None
            try:
                default_args = info["default_args"]
            except:
                default_args = None
            try:
                hidden = info["hidden"]
            except:
                hidden = False
            try:
                icon_antialiasing = info["icon-antialiasing"]
            except:
                icon_antialiasing = True
            
            if os.path.isfile(os.path.join(self.included, module, "icon.png")):
                icon = os.path.join(self.included, module, "icon.png")
            elif os.path.isfile(os.path.join(self.added, module, "icon.png")):
                icon = os.path.join(self.added, module, "icon.png")
            else:
                icon = None
            
            info_dictionary = {"title": title, "version": version,
                "author": author, "directory": self.included_apps_dirs[i],
                "icon": icon, 'default_args': default_args, "hidden": hidden,
                "icon-antialiasing": icon_antialiasing}
            
            if i < self.amount_of_included_apps:
                self.included_apps_info[module] = info_dictionary
            else:
                self.added_apps_info[module] = info_dictionary

        self.root = root
        self.root.title("PyTk Application Manager {}".format(__version__))
        self.root.iconphoto(False, ImageTk.PhotoImage(file = self.env_icon))
        self.root.geometry("800x600+20+20")
        self.root.resizable(True, True)
        self.root.deiconify()
        Grid.rowconfigure(self.root, 0, weight = 0)
        Grid.columnconfigure(self.root, 0, weight = 0)

        for item in self.root.winfo_children():
            item.destroy()
        
        self.menu = Menu(self.root)
        self.root.config(menu = self.menu)

        # ttk style
        self.style = Style()
        self.style.configure("frame.TFrame", theme = "winnative")
        self.style.configure("defEnv.TButton", theme = "winnative", relief = "flat")

        self.setup_defaults(self.root, self.style)

        # create file menu
        file = Menu(self.menu, tearoff = 0)
        file.add_command(label = "Import")
        file.add_command(label = "Return to selection screen", command = partial(init, root))
        file.insert_separator(2)
        file.add_command(label = "Exit", command = exit)
        self.menu.add_cascade(label = "File", menu = file)

        # creates settings menu
        settings = Menu(self.menu, tearoff = 0)
        settings.add_command(label = "Change background colour", command = lambda: self.recolour(root, self.style))
        settings.add_command(label = "Change accent colour")
        settings.add_command(label = "Save current colour as default",
                                command = lambda: self.edit_settings(self.user_defaults, "background", self.root.cget("background")))
        settings.insert_separator(2)
        settings.add_command(label = "Reset all to default", command = lambda: self.reset_all_defaults(self.root, self.style))
        self.menu.add_cascade(label = "Settings", menu = settings)

        # create frame
        self.frame = Frame(self.root, style = "frame.TFrame")
        self.frame.grid_forget()

        separator = Separator(self.frame, orient = VERTICAL)
        separator.grid(row = 0, column = 4, rowspan = 32, sticky = N+S+W)

        for i in range(32):
            self.frame.grid_columnconfigure(i, minsize = 60)
            self.frame.grid_rowconfigure(2 * i, minsize = 76)
        self.frame.grid()

        # add included apps buttons
        x = 0
        y = 0
        for key, value in self.included_apps_info.items():
            title = value["title"]
            version = value["version"]
            author = value["author"]
            directory = value["directory"]
            icon = value["icon"]
            default_args = value["default_args"]
            icon_antialiasing = value["icon-antialiasing"]
            hidden = value["hidden"]
            if not hidden:
                if icon != None:
                    icon = Image.open(icon)
                    if icon_antialiasing:
                        icon = icon.resize((66, 66), Image.ANTIALIAS)
                    else:
                        icon = icon.resize((66, 66))

                # add buttons
                btn = Button(self.frame, style = "defEnv.TButton")
                if icon == "None":
                    btn.img = PhotoImage() 
                else:
                    btn.img = ImageTk.PhotoImage(icon)
                btn.config(image = btn.img, compound = CENTER,
                command = partial(self.run_module, key, self.root, self.frame))
                btn.grid(padx = 2, column = x, row = y, sticky = N+S+W+E)

                # add label below
                lbl = Label(self.frame, text = title)
                lbl.config(anchor = CENTER)
                lbl.grid(column = x, row = y + 1, padx = 2, sticky = N+S+W+E)

                # makes sure they are in the right order
                x = (x + 1) % 4
                if x == 0:
                    y += 2
        
    def run_module(self, module, root, frame):
        for i in self.root.winfo_children():
            if i.winfo_children():
                if repr(i) != "<tkinter.Menu object .!menu>":
                    for k in i.winfo_children():
                        k.destroy()
        self.root.deiconify()

        if module in self.included_apps_info.keys():
            location = "included"
        elif module in self.added_apps_info.keys():
            location = "added"
        
        if module not in sys.modules:
            try:
                exec("import {0}.{1} as {1}".format(location, module))
            except:
                raise Exception("Could not import module \'{}\'".format(module))
        try:
            default_args = self.included_apps_info[module]["default_args"]
        except:
            default_args = self.added_apps_info[module]["default_args"]
        
        args_string = ""
        i = 1
        for key, value in default_args.items():
            if args_string == "":
                if len(default_args) == i:
                    args_string += "{} = {}".format(key, value)
                else:
                    args_string += "{} = {},".format(key, value)
            elif len(default_args) == i:
                args_string += " {} = {}".format(key, value)
            else:
                args_string += " {} = {},".format(key, value)
            i += 1
        
        try:
            exec("{}.init({})".format(module, args_string)) # need to update to obj-oriented
        except:
            if "init" not in dir(module):
                raise Exception("\'{}.init()\' does not exist".format(module))
            else:
                raise Exception("Could not run \'{}.init({})\'."
                "Its default arguments may be incorrect".format(module, args_string))

    def edit_settings(self, file, setting, new):
        with open(file, "r+") as f:
            try:
                contents = json.load(f)
            except json.decoder.JSONDecodeError:
                contents = {}
            contents[setting] = new
            f.seek(0)
            json.dump(contents, f, indent = 4)
            f.truncate()

    def get_current(self, file, setting):
        with open(file, "r+") as f:
            try:
                contents = json.load(f)
            except json.decoder.JSONDecodeError:
                return None
            if setting in contents:
                return contents[setting]
            else:
                return None

    def setup_defaults(self, root, style):
        if self.get_current(self.user_defaults, "background") == None:
            self.edit_settings(self.user_defaults, "background", "SystemButtonFace")
        root.config(background = self.get_current(self.user_defaults, "background"))
        style.configure("TButton", background = self.get_current(self.user_defaults, "background"))
        style.configure("TLabel", background = self.get_current(self.user_defaults, "background"))
        style.configure("TFrame", background = self.get_current(self.user_defaults, "background"))


    def reset_all_defaults(self, root, style):
        with open(self.user_defaults, "r+") as f:
            f.seek(0)
            f.truncate()
            json.dump({}, f)
        self.setup_defaults(root, style)
    
    def recolour(self, root, style):
        colour = colorchooser.askcolor(title = "Choose background colour",
        initialcolor = "SystemButtonFace")
        root.config(background = colour[1])
        style.configure("TFrame", background = colour[1])
        style.configure("TButton", background = colour[1])
        style.configure("TLabel", background = colour[1])