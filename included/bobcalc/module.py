from tkinter import *
from tkinter.ttk import *
try: # when module.py is run directly, .defs does not work, so defs must be tried
    from .defs import *
except:
    from defs import *
import os.path

def init(root): # This will be run when its button is clicked on the main window, root is the Tk() window
    root.title("Scientific Calculator")
    root.geometry("300x600+20+20")
    icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png") # gets icon directory
    root.iconphoto(False, ImageTk.PhotoImage(file = icon)) # sets the icon
    Grid.rowconfigure(root, 0, weight = 1) # makes sure rows take up all space (in root)
    Grid.columnconfigure(root, 0, weight = 1)
    root.resizable(False, False) # cannot resize in any dimension

    style = Style() # creates style sheet
    style.configure("calc_frame.TFrame", theme = "winnative") # style sheet for frames, uses windows theme
    style.configure("calc_buttons.TButton", theme = "winnative", relief = "flat", padding = 2)
    frame = Frame(root, style = "calc_frame.TFrame") # creates a frame

    # maybe add loading screen

    # create white column for input:
    input_box = Label(frame, background = "#FFFFFF")
    input_box.grid(row = 0, column = 0, columnspan = 9, sticky = E+W) # goes from east to west
    Grid.columnconfigure(frame, 0, weight = 1)
    # add input text
    input_text = Label(frame, text = "[]", background = "#FFFFFF")
    input_text.grid(row = 0, column = 8, sticky = N+S+E) # centres text and puts it on east
    # add separators
    separator_1 = Separator(frame, orient = HORIZONTAL)
    separator_1.grid(column = 0, row = 0, columnspan = 9, sticky = N+E+W) # goes from east to west, & north
    separator_2 = Separator(frame, orient = HORIZONTAL)
    separator_2.grid(column = 0, row = 0, columnspan = 9, sticky = S+E+W) # goes from east to west, & south

    # adds buttons
    i = 1
    for y in range(5):
        Grid.rowconfigure(frame, y + 1, weight = 1) # makes sure that this row takes up all space

        for x in range(8):
            Grid.columnconfigure(frame, x + 1, weight = 1) #likewise

            latex_text = to_latex(buttons_dict[i][0], 15) # turns text to LaTeX
            # creates button
            button = Button(frame, image = latex_text, compound = CENTER, style = "calc_buttons.TButton")
            button.img = latex_text # makes sure the buffer is not lost
            button.grid(row = y + 1, column = x + 1, sticky = N+S+E+W) # sets its position in grid
            i += 1
    del i, x, y, latex_text # clean-up
    frame.grid(sticky = S)

if __name__ == "__main__":
    root = Tk()
    init(root)
    root.mainloop()