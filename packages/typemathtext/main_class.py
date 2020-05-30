import math
import os
import json
import sympy as sy

class typemathtextError(Exception):
    pass

class typemath:
    """Creates an object that can be used for easy-to-use methods to create calculators.
    
    It does this by creating methods to convert between Python (sympy) and LaTeX.
    Furthermore, it creates a pointer that can be used to insert new text (in the
    custom typemath format) in different places in the text.


    Parameters:
    
        latex_text (str) -- a string written with LaTeX format.
                            (e.g. "\int 4x^2 dx")
    

    Attributes ():
    
        pointer (int) -- the current position of the pointer

                            : This determines where the string will be edited

        pparsed (list) -- a list containing the parsed version of latex_text

                            : This is only updated when primary_parse() is called

        sparsed (str) -- a string containing the fully converted version of latex_text
                         into standard Python/sympy format

                            : This is only updated when secondary_parse() is called



    Written by Joshua Kent, last updated 29/05/2020.
    github.com/joshua-kent/PyTkAppMng"""
    
    _current_dir = os.path.dirname(os.path.realpath(__file__))
    _parse_info_dir = os.path.join(_current_dir, "parse_info.json")
    _x, _y = sy.symbols("x y")

    def __init__(self, latex_text): # edit this to support multiple initial formats
        self.latex_text = latex_text
        self.pointer = 0
        self.pparsed = []
        self.sparsed = []
        self.parse()
        self.compile()

    def edit(self, text, insert = None, moveby = 1, moveto = None):
        """Edits latex text by parsing, editing, repositioning the pointer, recompiling.


        Parameters:

            text (str) -- a string of LaTeX text (usually in format r"$[text]$")

            moveby (int/None) -- how many items the pointer should move by [default: 1]
                                 (if moveby = 1: move pointer one item to right in parsed text,
                                 if moveby = -2: move pointer two items to left in parsed text)
                                    
                                    : This cannot have the same type as moveto

            moveto (int/None) -- move pointer to an specific place in list [default: None]
                                 (if moveto = 2: place pointer after second item)
                                    
                                    : This cannot have the same type as moveby
                                    : This cannot be a negative integer.
        
        
        Example:

            [insert later]

        
        
        Written by Joshua Kent, last updated 29/05/2020.
        github.com/joshua-kent/PyTkAppMng"""

        # make sure moveby is only relative to what the new text is, also check
        # that the new text is readable to the parser

        if moveby == moveto == None or None not in (moveby, moveto):
            raise typemathtextError("'moveby' and 'moveto' must be of different types.")

    def concatenate_chars(self, chars, *args):
        """Connects items in a string into one item if they concatenate to some given value(s).


        Parameters:

            chars (list) -- the list to be edited
            
            *args (str) -- list strings that need to be concatenated (in that order)


        Returns:

            Returns a new list with the given concatenations


        Example:

            concatenate_chars(["h", "e", "l", "l", "o"], "he", "ll")

            As in the list, there are two consecutive items that together create "he",
            these are concatenated. Likewise for "ll".

            This returns the list: ["he", "ll", o]

        

        Written by Joshua Kent, last updated 29/05/2020.
        github.com/joshua-kent/PyTkAppMng"""

        for item in args:
            i = 0
            while i <= len(chars) - len(item):
                place_check = ""
                for k in range(len(item)):
                    place_check += chars[i + k]
                if place_check == item:
                    chars[i] = item
                    q = len(item) - 1
                    while q > 0:
                        chars.pop(i + q)
                        q -= 1
                i += 1
    
    @staticmethod
    def concatenate_ints(lst):
        output = []
        numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        tuple_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'x', 'y', "math.e", "math.pi")
        for i in range(len(lst)):
            try:
                if lst[i] in tuple_list and lst[i - 1] in tuple_list:
                    if lst[i] in ("x", "y"):
                        output.append("*")
                        output.append(lst[i])
                    else:
                        output[-1] += lst[i]
                else:
                    output.append(lst[i])
            except:
                output.append(lst[i])
        return output
    
    def swap(self, lst, old, new):
        i = 0
        for item in lst:
            if item == old:
                lst[i] = new
            i += 1
        return lst

# THIS IS MESSY CODE, TAMPERING COULD EASILY BREAK IT --[

    def parse(self):
        r"""Splits a LaTeX math string into its parsed format.

        This parsed form can be used as a midway point between LaTex
        and normal Python (sympy) formats. It is also useful for pointers.
        (e.g \frac{1}{2} (LaTeX) --> (parse) --> ['\FRAC{', '1', '}', '{', '2', '}']
        --> (compile) --> '(1)/(2)' --> (evaluate) --> 0.5
        )

        
        Returns:

            Returns self.pparsed, which is the list that 'primary_parse' has generated.

        
        
        Written by Joshua Kent, last updated 29/05/2020.
        github.com/joshua-kent/PyTkAppMng"""

        # isolate keywords into list
        output = []
        for char in self.latex_text:
            if char != " ":
                output.append(char)
        with open(self._parse_info_dir, "r") as f:
            doc_ = json.load(f)
            specials = doc_["specials"]
            specials_get = [item[0] for item in specials]
            specials_set = [item[1] for item in specials]

            keywords = doc_["keywords"]
            keywords_get = [item[0] for item in keywords]
            keywords_set = [item[1] for item in keywords]

            pointouts = doc_["pointouts"]
            pointouts_get = [item[0] for item in pointouts]
            pointouts_set = [item[1] for item in pointouts]


        for i in range(len(specials)):
            self.concatenate_chars(output, specials_get[i])
            self.swap(output, specials_get[i], specials_set[i])
        for i in range(len(keywords)):
            self.concatenate_chars(output, keywords_get[i])
        for i in range(len(pointouts)):
            self.concatenate_chars(output, pointouts_get[i])
            self.swap(output, pointouts_get[i], pointouts_set[i])
        
        # connect consecutive numbers, multiply consecutive numbers & variables to create terms
        output = self.concatenate_ints(output)

        self.pparsed = output
        return self.pparsed

    def compile(self):
        """Fully converts the parsed text list into a sympy-readable format as a
        string to be executed.

        Only the current parsed LaTeX text is compiled. Instead of directly
        calling this function, it is automatically called when a new typemath
        instance is initiated, and is also called automatically when the 'typemath.edit'
        method is called.
        

        Returns:

            This returns the new string and also puts it in the attribute 'sparsed'.



        Written by Joshua Kent, last updated 30/05/2020.
        github.com/joshua-kent/PyTkAppMng
        """

        output = self.pparsed.copy() # setting a variable to a list only creates a new reference, not id
        with open(self._parse_info_dir, "r") as f:
            doc_ = json.load(f)
            keywords = doc_["keywords"]
            keywords_get = [item[0] for item in keywords]
            keywords_set = [item[1] for item in keywords]

            specials = doc_["specials"]
            specials_get = [item[0] for item in specials]
            specials_set =[item[1] for item in specials]
        
        for i in range(len(keywords)):
            self.swap(output, keywords_get[i], keywords_set[i])

        # Creates tokens for each special value (that need more work to change)
        # In format:
        # {"token_number": (token's value, position)}
        # token_numbers gives a list of the keys of tokens in order
        # token_values gives the value that the token represents
        # token_positions gives a list of the positions of each token in output
        current_token_number = 1
        tokens = {}
        for i in range(len(output)):
            if output[i] == "}":
                tokens[f"{current_token_number}a"] = ("}", i)
                for k in range(len(output)):
                    t = len(output) - k - 1
                    token_positions = [item[1] for item in tokens.values()]
                    if (output[t] == "{" or output[t] in specials_set) and t < i:
                        if not token_positions.__contains__(t):
                            tokens[f"{current_token_number}b"] = (output[t], t)
                            break
                current_token_number += 1
        token_numbers = [key for key in tokens.keys()]
        token_values = [item[0] for item in tokens.values()]
        token_positions = [item[1] for item in tokens.values()]

        # convert \frac{a}{b} to (a)/(b)
        for i in range(len(tokens)):
            if token_values[i] == "FRAC{": # first {
                token_1_number = token_numbers[i]
                token_1 = tokens[token_1_number]
                token_1_pos = token_1[1]
                corresponding_token_1_number = token_1_number.replace("b", "a")
                corresponding_token_1 = tokens[corresponding_token_1_number] # first }
                corresponding_token_1_pos = corresponding_token_1[1]
                for k in range(len(token_positions)):
                    if token_positions[k] == corresponding_token_1[1] + 1:
                        if token_values[k] == "{": # second {
                            token_2_number = token_numbers[k]
                            token_2  = tokens[token_2_number]
                            token_2_pos = token_2[1]
                            corresponding_token_2_number = token_2_number.replace("b", "a")
                            corresponding_token_2 = tokens[corresponding_token_2_number] # second }
                            corresponding_token_2_pos = corresponding_token_2[1]
                            break
                if "corresponding_token_2" in locals():
                    output[token_1_pos] = "("
                    output[corresponding_token_1_pos] = ")/"
                    output[token_2_pos] = "("
                    output[corresponding_token_2_pos] = ")"
        
        output = "".join(output)

        self.sparsed = output
        return self.sparsed

# ]--
    
    def evaluate(self):
        """Evaluates the current math text and returns its value.
        
        
        
        Written by Joshua Kent, last updated 30/05/2020.
        """

        self.parse()
        self.compile()
        return eval("".join(self.sparsed))

if __name__ == "__main__":
    txt = typemath(r"\frac{5}{2}")