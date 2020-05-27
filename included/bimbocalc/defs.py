from io import BytesIO
from PIL import ImageTk, Image
from matplotlib.mathtext import math_to_image
#import sympy as sp

buttons_dict = {1: [r"$|a|$", "abs"], 2: [r"$\sqrt{a}$", "sqrt"], 3: [r"$\log$", "log"],
                    4: [r"$\ln$", "ln"], 5: [r"$a^b$", "power"], 6: [r"$()$", "brackets"],
                    7: [r"%", "percent"], 8: [r"$=$", "equals"], 9: [r"$\lfloor{a}\rfloor$", "floor"],
                    10: [r"$f(x)$", "func"], 11: [r"$\cot$", "cot"], 12: [r"$\tan$", "tan"],
                    13: [r"$7$", "7"], 14: [r"$8$", "8"], 15: [r"$9$", "9"], 16: [r"$\div$", "div"],
                    17: [r"$\lceil{a}\rceil$", "ceil"], 18: [r"$\frac{d}{dx}$", "derivative"],
                    19: [r"$\sec$", "sec"], 20: [r"$\cos$", "cos"], 21: [r"$4$", "4"], 22: [r"$5$", "5"],
                    23: [r"$6$", "6"], 24: [r"$\times$", "times"], 25: [r"$x$", "x"],
                    26: [r"$\int$", "integral"], 27: [r"$\csc$", "csc"], 28: [r"$\sin$", "sin"],
                    29: [r"$1$", "1"], 30: [r"$2$", "2"], 31: [r"$3$", "3"], 32: [r"$-$", "minus"],
                    33: [r"$y$", "y"], 34: [r"$\int^a_b$", "def_integral"], 35: [r"$e$", "e"],
                    36: [r"$\pi$", "pi"], 37: [r"$\frac{a}{b}$", "fraction"], 38: [r"$0$", "0"],
                    39: [r"$.$", "decimal_point"], 40: [r"$+$", "plus"]}
                    # these are the buttons in LaTeX maths mode format

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