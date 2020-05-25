from tkinter import *
from tkinter.ttk import *
from io import BytesIO
from PIL import ImageTk, Image
from matplotlib.mathtext import math_to_image
import sympy as sp

def init(root):
    root.title("Scientific Calculator")
    root.geometry("300x600+20+20")
    Grid.rowconfigure(root, 0, weight = 1) # makes sure rows take up all space (in root)
    Grid.columnconfigure(root, 0, weight = 1)
    root.resizable(False, False) # cannot resize in any dimension

    style = Style()
    style.configure("TFrame", theme = "winnative")
    style.configure("TButton", theme = "winnative", relief = "flat", padding = 2)
    frame = Frame(root)

    # maybe add loading screen

    i = 1
    for y in range(5):
        Grid.rowconfigure(frame, y, weight = 1) # makes sure that this row takes up all space

        for x in range(8):
            Grid.columnconfigure(frame, x, weight = 1) #likewise

            q = to_latex("$\\frac{{d}}{{dx}}$", 20) # turns text to LaTeX
            btn = Button(frame, image = q, compound = CENTER) # creates button
            btn.img = q # makes sure the buffer is not lost
            btn.grid(row = y, column = x, sticky = "nsew") # sets its position in grid, sticks to south
            i += 1
    del i, x, y, q
    frame.grid()

def to_latex(text, height):
    buffer = BytesIO() # creates buffer
    math_to_image(text, buffer, dpi = 1000, format = "png") # turns text into LaTeX format
    buffer.seek(0) # sets buffer pointer to 0
    pillow_image = Image.open(buffer) # opens created image
    x, y = pillow_image.size # gets x and y dimensions of image
    aspect_ratio = x/y # aspect ratio (x/y), this needs to be maintained

    y = height # resets y
    x = int(y * aspect_ratio) # changes x that reserves aspect ratio (must be integer)
    pillow_image = pillow_image.resize((x, y), Image.ANTIALIAS) # resizes

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