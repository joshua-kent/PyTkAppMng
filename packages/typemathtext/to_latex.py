# This function was inspired by MannyC's answer on stackoverflow:
# https://stackoverflow.com/questions/36636185/is-it-possible-for-python-to-display-latex-in-real-time-in-a-text-box

from io import BytesIO
from PIL import ImageTk, Image
from matplotlib.mathtext import math_to_image

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