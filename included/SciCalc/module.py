from tkinter import *
from tkinter.ttk import *
try: # when module.py is run directly, .defs does not work, so defs must be tried
    from .defs import *
except:
    from defs import *
import os.path
from io import BytesIO
from PIL import ImageTk, Image
from matplotlib.mathtext import math_to_image
import sympy as sp

def init(root): # This will be run when its button is clicked on the main window, root is the Tk() window
    root.title("Scientific Calculator")
    root.geometry("300x600+20+20")
    icon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png") # gets icon directory
    root.iconphoto(False, ImageTk.PhotoImage(file = icon)) # sets the icon
    Grid.rowconfigure(root, 0, weight = 1) # makes sure rows take up all space (in root)
    Grid.columnconfigure(root, 0, weight = 1)
    root.resizable(False, False) # cannot resize in any dimension

    style = Style() # creates style sheet
    style.configure("TFrame", theme = "winnative") # style sheet for frames, uses windows theme
    style.configure("TButton", theme = "winnative", relief = "flat", padding = 2) # likewise for buttons
    frame = Frame(root) # creates a frame

    # maybe add loading screen

    i = 1
    for y in range(5):
        Grid.rowconfigure(frame, y, weight = 1) # makes sure that this row takes up all space

        for x in range(8):
            Grid.columnconfigure(frame, x, weight = 1) #likewise

            q = to_latex(buttons_dict[i][0], 15) # turns text to LaTeX
            btn = Button(frame, image = q, compound = CENTER) # creates button
            btn.img = q # makes sure the buffer is not lost
            btn.grid(row = y, column = x, sticky = N+S+E+W) # sets its position in grid
            i += 1
    del i, x, y, q # clean-up
    frame.grid(sticky = S)

def to_latex(text, size): # converts text to LaTeX and gives it a size
    buffer = BytesIO() # creates buffer
    math_to_image(text, buffer, dpi = 1000, format = "png") # turns text into LaTeX format
    buffer.seek(0) # sets buffer pointer to 0
    pillow_image = Image.open(buffer) # opens created image
    x, y = pillow_image.size # gets x and y dimensions of image
    aspect_ratio = y / x # aspect ratio (x/y), this needs to be maintained

    # This makes sure the proportions of the images are all similar:
    if aspect_ratio > 1: # if y is greater than x, set y to size and adjust x to retain aspect ratio
        y = size
        x = int(size / aspect_ratio)
        pillow_image = pillow_image.resize((x, y), Image.ANTIALIAS)
    else: # if x is greater than y, set x to size and adjust y to retain aspect ratio
        x = size
        y = int(x * aspect_ratio)
        pillow_image = pillow_image.resize((x, y), Image.ANTIALIAS)

    pillow_image = pillow_image.convert("RGBA") # converts to RGBA (includes opacity)
    img_data = pillow_image.getdata() # gets data in image
    new_data = [] # creates new list to contain new data
    for data in img_data:
        if (255 - data[0], 255 - data[1], 255 - data[2]) < (20, 20, 20): # if the pixel near white (each colour R,G,B is less than 20 units away from 255)
            new_data.append((255, 255, 255, 0)) # make it opaque
        else:
            new_data.append(data) # keep it as is
    pillow_image.putdata(new_data) # replace pillow_image's data with new data

    return ImageTk.PhotoImage(pillow_image) # returns the image in a tkinter readable format

if __name__ == "__main__":
    root = Tk()
    init(root)
    root.mainloop()