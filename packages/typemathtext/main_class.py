import os
import json

class typemathtextError(Exception):
    pass

class text:
    """Creates an object that can be used for easy-to-use methods to create calculators."""
    
    latex_text = ""
    parsed_latex_text = [] # LaTeX text separated into a list
    pointer = 0
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parse_info_dir = os.path.join(current_dir, "parse_info.json")

    def __init__(self):
        self.parse_latex(r"\int4x+\int2dx-3dx+\int4+\int2dxdx")

    def edit(self, text, insert = None, moveby = 1, moveto = None):
        """Edits latex text by parsing, editing, repositioning the pointer, recompiling


        KEYWORDS

            text (str) -- a string of LaTeX text (usually in format r"$[text]$")

            moveby (int/None) -- how many items the pointer should move by [default: 1]
                                 (if moveby = 1: move pointer one item to right in parsed text,
                                 if moveby = -2: move pointer two items to left in parsed text)
                                 
                                 Notes:
                                       This cannot have the same type as moveto

            moveto (int/None) -- move pointer to an specific place in list [default: None]
                                 (if moveto = 2: place pointer after second item)
                                 
                                 Notes:
                                       This cannot have the same type as moveby
                                       This cannot be a negative integer.
        
        
        EXAMPLE

            [insert later]
        """

        if moveby == moveto == None or None not in (moveby, moveto):
            raise typemathtextError("'moveby' and 'moveto' must be of different types.")

    def concatenate_chars(self, chars, *args):
        """Connects items in a string into one item if they concatenate to some given value(s)


        KEYWORDS

            chars (list) -- the list to be edited
            
            *args (str) -- list strings that need to be concatenated (in that order)


        RETURNS

            Returns a new list with the given concatenations


        EXAMPLE

            concatenate_chars(["h", "e", "l", "l", "o"], "he", "ll")

            As in the list, there are two consecutive items that together create "he",
            these are concatenated. Likewise for "ll".

            This returns the list: ["he", "ll", o]
        """

        output = chars
        for item in args:
            i = 0
            while i <= len(output) - len(item):
                place_check = ""
                for k in range(len(item)):
                    place_check += output[i + k]
                if place_check == item:
                    output[i] = item
                    q = len(item) - 1
                    while q > 0:
                        output.pop(i + q)
                        q -= 1
                i += 1
        return output

    def parse_latex(self, text):
        output = []
        for char in text:
            output.append(char)
        with open(self.parse_info_dir, "r") as f:
            keywords = json.load(f)["keywords"]
        for word in keywords:
            self.concatenate_chars(output, word)
        print(output)

if __name__ == "__main__":
    txt = text()