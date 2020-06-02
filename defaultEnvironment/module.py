'''
This module is only intended to be used internally, so its
documentation may not be totally clear.
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

__version__ = "0.2.6b7"

class init:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    env_icon = os.path.join(current_dir, "icon.png")
    pytkappmng_dir = os.path.dirname(current_dir)
    applications_dir = os.path.join(pytkappmng_dir, "applications")
    included = os.path.join(applications_dir, "included")
    added = os.path.join(applications_dir, "added")
    user_settings = os.path.join(current_dir, "user_settings.json")
    
    included_apps_dirs = []
    included_apps_info = {}
    amount_of_included_apps = 0

    added_apps_dirs = []
    added_apps_info = {}
    amount_of_added_apps = 0

    def __init__(self, root):
        # initiates the window and adds everything

        # set up window
        self.root = root
        self.root.title("PyTk Application Manager {}".format(__version__))
        self.root.iconphoto(False, ImageTk.PhotoImage(file = self.env_icon))
        self.root.geometry("800x600+20+20")
        self.root.resizable(True, True)
        self.root.deiconify()
        Grid.rowconfigure(self.root, 0, weight = 0)
        Grid.columnconfigure(self.root, 0, weight = 0)
        
        # gets the directories of modules in 'included' and 'added'
        for files_ in os.walk(self.included):
            root_ = files_[0] # this will always be a directory, see os.walk()
            if os.path.dirname(root_) == self.included:
                split_list_ = root_.split("\\")
                if "__pycache__" not in split_list_:
                    self.included_apps_dirs.append(root_)
        self.amount_of_included_apps = len(self.included_apps_dirs)
        for files_ in os.walk(self.added):
            root_ = files_[0]
            if os.path.dirname(root_) == self.added:
                split_list_ = root_.split("\\")
                if "__pycache__" not in split_list_:
                    self.added_apps_dirs.append(root_)
        self.amount_of_added_apps = len(self.added_apps_dirs)

        # gets info from info.json in modules, and appends it to (included/added)_apps_info
        self.get_json_info()

        # clears all widgets other than menu
        self.clear_widgets()

        # ttk style
        self.style = Style()
        self.style.configure("frame.TFrame", theme = "winnative")
        self.style.configure("defEnv.TButton", theme = "winnative", relief = "flat")

        # setup window attributes in accordance to user_settings.json
        self.setup_user_defaults()

        # setup menu
        self.create_menu()

        # creates frame
        self.frame = Frame(self.root, style = "frame.TFrame")
        self.frame.grid_forget()

        separator = Separator(self.frame, orient = VERTICAL)
        separator.grid(row = 0, column = 4, rowspan = 32, sticky = N+S+W)

        for i in range(32):
            self.frame.grid_columnconfigure(i, minsize = 60)
            self.frame.grid_rowconfigure(2 * i, minsize = 76)
        self.frame.grid()

        self.create_included_buttons()

    def create_included_buttons(self):
        # creates buttons for included apps

        # add included apps buttons
        x = 0
        y = 0
        for key, value in self.included_apps_info.items():
            
            # all of these values are set to make functionality for additional info in future
            title = value["title"]
            version = value["version"]
            author = value["author"]
            directory = value["directory"]
            icon = value["icon"]
            default_args = value["default-args"]
            icon_antialiasing = value["icon-antialiasing"]
            hidden = value["hidden"]

            # creates icon (but not if it's hidden)
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
    
    def get_json_info(self):
        # gets info about each module from their info.json file

        for i in range(self.amount_of_included_apps + self.amount_of_added_apps):

            # sets details based on if it is getting an app from 'included' or 'added'
            if i < self.amount_of_included_apps:
                mod_dir = self.included_apps_dirs[i]
            else:
                mod_dir = self.added_apps_dirs[i - self.amount_of_included_apps]
            
            split_dir = mod_dir.split("\\")
            module = split_dir[len(split_dir) - 1]
            info_json_directory = os.path.join(mod_dir, "info.json")

            # gets settings from the info.json file (None if doesn't exist), puts them in info
            info = {}
            info["title"] = self.get_setting(info_json_directory, "title", "Unnamed app")
            info["version"] = self.get_setting(info_json_directory, "version")
            info["author"] = self.get_setting(info_json_directory, "author", "Unknown")
            info["directory"] = mod_dir
            info["default-args"] = self.get_setting(info_json_directory, "default-args")
            info["hidden"] = self.get_setting(info_json_directory, "hidden", "False")
            info["icon-antialiasing"] = self.get_setting(info_json_directory, "icon-antialiasing", "True")

            # gets icon from the icon.png file (None if doesnt exist)
            if os.path.isfile(os.path.join(self.included, module, "icon.png")):
                info["icon"] = os.path.join(self.included, module, "icon.png")
            elif os.path.isfile(os.path.join(self.added, module, "icon.png")):
                info["icon"] = os.path.join(self.added, module, "icon.png")
            else:
                info["icon"] = None
            
            # sets the respective apps_info dictionary key (module) to (info)
            if i < self.amount_of_included_apps:
                self.included_apps_info[module] = info
            else:
                self.added_apps_info[module] = info

    def create_menu(self):
        # creates a menu for the window

        # creates menu object
        # if the menu does not already exist
        if not "<tkinter.Menu object .!menu>" in repr(self.root.winfo_children()):
            self.menu = Menu(self.root)
            self.root.config(menu = self.menu)

            # creates file menu
            file = Menu(self.menu, tearoff = 0)
            file.add_command(label = "Import")
            file.add_command(label = "Return to selection screen", command = partial(init, self.root))
            file.insert_separator(2)
            file.add_command(label = "Exit", command = exit)
            self.menu.add_cascade(label = "File", menu = file)

            # creates settings menu
            settings = Menu(self.menu, tearoff = 0)
            settings.add_command(label = "Change background colour", command = self.recolour_background)
            settings.add_command(label = "Save current colour as default",
                                    command = lambda: self.set_setting(self.user_settings, "background", self.root.cget("background")))
            settings.insert_separator(2)
            settings.add_command(label = "Reset all to default", command = self.reset_all_user_defaults)
            self.menu.add_cascade(label = "Settings", menu = settings)

    def run_module(self, module, root, frame):
        # runs a module in /applications

        self.clear_widgets()

        # set location to whichever folder it's in
        # (this could return an error, but shouldn't as this method is only used internally)
        if module in self.included_apps_info.keys():
            location = "applications.included"
        elif module in self.added_apps_info.keys():
            location = "applications.added"
        
        ## this needs to be changed to a more direct method ('command' in info.json) -- [[

        # imports the module if not already imported
        if module not in sys.modules:
            exec("import {0}.{1} as {1}".format(location, module))

        # sets default_args
        try:
            default_args = self.included_apps_info[module]["default-args"]
        except:
            default_args = self.added_apps_info[module]["default-args"]
        
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
            exec("{}.init({})".format(module, args_string))
        except:
            if "init" not in dir(module):
                raise Exception("\'{}.init()\' does not exist".format(module))
            else:
                raise Exception("Could not run \'{}.init({})\'."
                "Its default arguments may be incorrect".format(module, args_string))
        
        ## ]]
    
    def clear_widgets(self):
        # clears current window (other than its menu)

        for i in self.root.winfo_children():
            if repr(i) != "<tkinter.Menu object .!menu>":
                if i.winfo_children():
                    for k in i.winfo_children():
                        k.destroy()
                i.destroy()
        self.root.deiconify()

    @staticmethod
    def set_setting(file, setting, value = None):
        # sets a setting in a json file to a value
        # (file and setting created if does not exist)

        with open(file, "w+") as f:
            try:
                contents = json.load(f)
            except:
                contents = {}
            contents[setting] = value
            f.seek(0)
            json.dump(contents, f, indent = 4)
            f.truncate()

    @staticmethod
    def get_setting(file, setting, not_exist = None):
        # gets the value of a setting in a json file 
        # (if the file or setting does not exists, returns not_exist)

        with open(file, "r+") as f:
            try:
                contents = json.load(f)
            except:
                return not_exist
            
            if setting in contents:
                return contents[setting]
            else:
                return not_exist

    # self.__class__ acts like cls
    def setup_user_defaults(self):
        # sets up 'root' (Tk obj) and 'style' (Tkk style obj) to match user_defaults.json

        if self.get_setting(self.user_settings, "background") == None:
            self.set_setting(self.user_settings, "background", "SystemButtonFace")
        self.root.config(background = self.get_setting(self.__class__.user_settings, "background"))
        self.style.configure("TButton", background = self.__class__.get_setting(self.__class__.user_settings, "background"))
        self.style.configure("TLabel", background = self.__class__.get_setting(self.__class__.user_settings, "background"))
        self.style.configure("TFrame", background = self.__class__.get_setting(self.__class__.user_settings, "background"))

    def reset_all_user_defaults(self):
        # resets the user_settings.json folder to an empty file

        with open(self.__class__.user_settings, "w+") as f:
            f.seek(0)
            f.truncate()
            json.dump({}, f)
        self.setup_user_defaults()

    def recolour_background(self):
        # recolours the background

        colour = colorchooser.askcolor(title = "Choose background colour",
        initialcolor = "SystemButtonFace")
        self.root.config(background = colour[1])
        self.style.configure("TFrame", background = colour[1])
        self.style.configure("TButton", background = colour[1])
        self.style.configure("TLabel", background = colour[1])