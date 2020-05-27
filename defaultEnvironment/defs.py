import os.path
import sys
import json
from tkinter import colorchooser

current_dir = os.path.dirname(os.path.realpath(__file__)) # gets current directory of this module
included = os.path.join(os.path.dirname(current_dir), "included")
useropts = os.path.join(os.path.dirname(current_dir), "useropts")
user_defaults = os.path.join(current_dir, "user_defaults.json")

included_apps_dirs = [] # create empty list of directories of included apps
included_apps_info = {}
# included_app_info[module] = {'title': 'ex', 'version': '3.8.2', 'author': 'am', 'directory': 'pl\e.py', 'icon': 'icon.png'}
amount_of_included_apps = 0

# do the same, but for useropts
useropts_apps_dirs = []
useropts_apps_info = {}
amount_of_useropts_apps = 0


# Sets up included_apps_dirs (a list of the directories of included apps)
# root is called root_1 to avoid confusion with tkinter root
for root_1, dirs, files in os.walk(included): # scans through every directory/file in "included" folder
    if os.path.dirname(root_1) == (included): # if the root's (directories with things in them) parent is included
        split_list = root_1.split("\\") # create temporary list of this directory's parts (separating by a \)
        if split_list[len(split_list) - 1] not in ["__pycache__"]: # if the last part of this directory is not __pycache__ (autogenerated folder)
            included_apps_dirs.append(root_1) # add the entire directory of this file to included_apps_dir
amount_of_included_apps = len(included_apps_dirs) # sets amount_of_included_apps to the amount of included apps

# Sets up useropts_apps (does same as above for useropts)
for root_1, dirs, files in os.walk(useropts):
    if os.path.dirname(root_1) == (useropts):
        split_list = root_1.split("\\") 
        if split_list[len(split_list) - 1] not in ["__pycache__"]:
            useropts_apps_dirs.append(root_1)
amount_of_useropts_apps = len(useropts_apps_dirs)
del root_1

# Sets up included_apps_info and useropts_apps_info (a dictionary containing information on each app)
sys.path.append(included) # temporarily adds included to path (to allow import)
for i in range(amount_of_included_apps + amount_of_useropts_apps):
    # the loop will first go through included apps, then useropts
    if i < amount_of_included_apps:
        split_dir = included_apps_dirs[i].split("\\") # splits each part of directory
        module = split_dir[len(split_dir) - 1] # app name will be the last folder in that directory
        info_json_directory = os.path.join(included_apps_dirs[i], "info.json") # gets info.json file
    else:
        split_dir = useropts_apps_dirs[i - amount_of_included_apps].split("\\")
        # i - am_incl_apps will let us go through useropts apps after included apps
        module = split_dir[len(split_dir) - 1]
        info_json_directory = os.path.join(useropts_apps_dirs[i - amount_of_included_apps], "info.json")

    try:
        with open(info_json_directory, "r") as f: # tries to open the info.json file
            info = json.load(f) # loads its contents into info
    except:
        info = {}
    try:
        title = info["title"] # get the value of the title key
    except:
        title = None #  if it doesnt exist set it to none
    # this repeats from now on:
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

    # checks if [directory of included]\[module]\icon.png exists
    if os.path.isfile(os.path.join(included, module, "icon.png")):
        icon = os.path.join(included, module, "icon.png") # if it does, set icon to that file
    elif os.path.isfile(os.path.join(useropts, module, "icon.png")):
        icon = os.path.join(useropts, module, "icon.png")
    else: # if not, set to None
        icon = None
    
    # contains all the information
    info_dictionary = {"title": title, "version": version,
            "author": author, "directory": included_apps_dirs[i],
            "icon": icon, 'default_args': default_args, "hidden": hidden,
            "icon-antialiasing": icon_antialiasing}

    # this information is then put in whichever dictionary depending on i
    if i < amount_of_included_apps:
        included_apps_info[module] = info_dictionary
    else:
        useropts_apps_info[module] = info_dictionary

def run_module(module, root, frame):
    # Clean up defaultEnvironment's frame
    for i in root.winfo_children(): # NEED TO TEST THIS OUT MORE, MENU DOES NOT STAY
        if i.winfo_children():
            for k in i.winfo_children():
                k.destroy()
        i.destroy()
    root.deiconify()

    if module in included_apps_info.keys(): # if the module is in included
        location = "included"
    elif module in useropts_apps_info.keys(): # if it is in useropts
        location = "useropts"

    # Checks if function will run correctly
    if module not in sys.modules: # checks if the module is currently imported
        try:
            exec("import {0}.{1} as {1}".format(location, module))
        except:
            raise Exception("Could not import module \'{}\'".format(module))
    try: # first test if its in included
        default_args = included_apps_info[module]["default_args"]
    except: # next test if its in useropts
        default_args = useropts_apps_info[module]["default_args"]
    # one of these should succeed as if default_args does not exist in the .json, it equals None


    args_string = ""
    current_iteration = 1
    for key, value in default_args.items(): # gets each key and value in default_args term by term
        if args_string == "": # if on first value
            if len(default_args) == current_iteration: # if also on last value
                args_string += "{} = {}".format(key, value)
            else:
                args_string += "{} = {},".format(key, value)
        elif len(default_args) == current_iteration: # if on last value (but not first)
            args_string += " {} = {}".format(key, value)
        else: # if in the middle
            args_string += " {} = {},".format(key, value)
        current_iteration += 1

    try:
        exec("{}.init({})".format(module, args_string)) # executes [module].init([args])
    except:
        if not eval("\"init\" in dir(\'{}\')".format(module)): # if [module].init() does not exist
            raise Exception("\'{}.init()\' does not exist.".format(module))
        else: # if it does, the arguments are likely to be incorrect
            raise Exception("Could not run \'{}.init({})\'. "
            "Its default arguments may be incorrect".format(module, args_string))

def edit_settings(file, setting, new): # replaces a setting in user_defaults.txt with new value
    with open(file, "r+") as f: # opens file
        try:
            contents = json.load(f) # tries to retrieve all data and put in contents
        except json.decoder.JSONDecodeError: # if a decode error occurred, the file is probably empty
            contents = {} # so, set contents to an empty dictionary
        contents[setting] = new # add/edit the value of the setting key to new
        f.seek(0) # go to the beginning of the file
        json.dump(contents, f, indent = 4) # dump all new info into the file, indent for values is 4
        f.truncate() # if anything else is still there, get rid of it

def get_current(file, setting): # gets current value of setting based on its name
    with open(file, "r+") as f: # opens user_defaults.json, if it doesn't exist it is created
        try:
            contents = json.load(f) # tries to load its information into contents (as a dictionary)
        except json.decoder.JSONDecodeError: # if there was a decoding error (likely due to it being empty)
            return None
        if setting in contents: # if the setting is in contents
            return contents[setting]
        else:
            return None

def setup_defaults(root, style):
    # Setup background
    if get_current(user_defaults, "background") == None: # if there is no current setting for "background"
        edit_settings(user_defaults, "background", "SystemButtonFace") # create it and set it to default
    root.config(background = get_current(user_defaults, "background")) # sets actual background to correct colour
    style.configure("TButton", background = get_current(user_defaults, "background")) # sets button backgrounds to correct
    style.configure("TLabel", background = get_current(user_defaults, "background"))
    style.configure("TFrame", background = get_current(user_defaults, "background"))

def reset_all_defaults(root, style):
    with open(user_defaults, "r+") as file:
        file.seek(0)
        file.truncate()
        json.dump({}, file)
    setup_defaults(root, style) # applies defaults

def recolour(root, style):
    colour = colorchooser.askcolor(title = "Choose background colour", # creates colour picker [rgb, hex]
                        initialcolor = "SystemButtonFace") # initial colour is default system colour
    root.config(background = colour[1]) # sets the background colour to the hex value
    style.configure("TFrame", background = colour[1])
    style.configure("TButton", background = colour[1]) # sets the buttons' background to that colour
    style.configure("TLabel", background = colour[1])