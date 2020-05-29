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
        """Edits latex text by parsing, editing, repositioning the pointer, recompiling


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

        if moveby == moveto == None or None not in (moveby, moveto):
            raise typemathtextError("'moveby' and 'moveto' must be of different types.")

    def concatenate_chars(self, chars, *args):
        """Connects items in a string into one item if they concatenate to some given value(s)


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
        current_list = lst
        old_list = []
        tuple_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'x', 'y', "math.e", "math.pi")
        while current_list != old_list:
            old_list = current_list
            try:
                for i in range(len(current_list)):
                    if current_list[i] in tuple_list and current_list[i + 1] in tuple_list:
                        if current_list[i + 1] in ('x', 'y'):
                            current_list[i] += "*{}".format(current_list[i + 1])
                        else:
                            current_list[i] += current_list[i + 1]
                        current_list.pop(i + 1)
            except:
                pass
        return current_list
    
    def swap(self, lst, old, new):
        i = 0
        for item in lst:
            if item == old:
                lst[i] = new
            i += 1
        return lst

    def parse(self):
        r"""Splits a LaTeX math string into its parsed format.

        This parsed form can be used as a midway point between LaTex
        and normal Python (sympy) formats. It is also useful for pointers.
        (e.g \frac{1}{2} (LaTeX) --> (parse) --> ['\FRAC{', '1', '}', '{', '2', '}']
        --> (compile) --> '(1)/(2)' --> 1/2 --> 0.5
        )

        
        Returns:

            Returns self.pparsed, which is the list that 'primary_parse' has generated.

        
        
        Written by Joshua Kent, last updated 29/05/2020.
        github.com/joshua-kent/PyTkAppMng"""

        # isolate keywords into list
        output = []
        for char in self.latex_text:
            output.append(char)
        with open(self._parse_info_dir, "r") as f:
            doc_ = json.load(f)
            specials = doc_["specials"]
            keywords = doc_["keywords"]
            pointouts = doc_["pointouts"]
        for lst_ in specials:
            self.concatenate_chars(output, lst_[0])
            self.swap(output, lst_[0], lst_[1])
        for lst_ in keywords:
            self.concatenate_chars(output, lst_[0])
        for lst_ in pointouts:
            self.concatenate_chars(output, lst_[0])
            self.swap(output, lst_[0], lst_[1])
        
        # connect consecutive numbers, multiply consecutive numbers & variables to create terms
        old_list = []
        tuple_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'x', 'y')
        while output != old_list:
            old_list = output
            try:
                for i in range(len(output)):
                    if output[i] in tuple_list and output[i + 1] in tuple_list:
                        if output[i + 1] in ('x', 'y'):
                            output[i] += "*{}{}".format("typemath._", output[i + 1])
                        else:
                            output[i] += output[i + 1]
                        output.pop(i + 1)
            except:
                pass

        self.pparsed = output
        return self.pparsed

    def compile(self):
        output = self.pparsed.copy() # setting a variable to a list only creates a new reference, not id
        with open(self._parse_info_dir, "r") as f:
            doc_ = json.load(f)
            keywords = doc_["keywords"]
            specials = doc_["specials"]
        for lst_ in keywords:
            self.swap(output, lst_[0], lst_[1])

        # Complete (needs to convert pparsed list to a sympy/Python readable format)
        # do this by creating a way for sorting nested curly brackets and converting
        # ie \frac{a}{b} --> (a)/(b) -- needs to have brackets to avoid miscalculations.
        # This also edits self.pparsed, it should not do that.

        self.sparsed = output
        return self.sparsed
    
    def eval(self):
        self.parse()
        self.compile()
        return eval("".join(self.sparsed))

if __name__ == "__main__":
    txt = typemath("\int(4x^2)")