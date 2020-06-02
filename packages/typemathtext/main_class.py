# To test, run in the terminal 'ipython -i main_class.py'

import warnings
import math
import os
import json
import sympy

class typemathtextError(Exception):
    pass

class typemath:
    """Creates an object that can be used for easy-to-use methods to create calculators.
    
    It does this by creating methods to convert between Python (sympy) and LaTeX.
    Furthermore, it creates a pointer that can be used to insert new text (in the
    custom typemath format) in different places in the text.


    Parameters:
    
        latex_input (str) -- a string written with LaTeX format.
                            (e.g. "\int 4x^2 dx")
    

    Attributes:
    
        pointer (int) -- the current position of the pointer

                                This determines where the string will be edited

        parsed (list) -- a list containing the parsed version of latex_input

                                This is only updated when primary_parse() is called

        compiled (str) -- a string containing the fully converted version of latex_input
                         into standard Python/sympy format

                                This is only updated when secondary_parse() is called"""
    
    _current_dir = os.path.dirname(os.path.realpath(__file__))
    _parse_info_dir = os.path.join(_current_dir, "parse_info.json")

    def __init__(self, latex): # edit this to support multiple initial formats
        self.latex = latex
        self.parsed = []
        self.compiled = ""
        self.parse()
        self.compile()
        try:
            self.evaluate = eval(self.compile())
        except: # the compiled form may currently be incomplete and return an error
            self.evaluate = None
        self.pointer = len(self.parsed)

    def parse(self, text = None, require_dollars = True):
        r"""Splits a LaTeX math string into its parsed format.

        This parsed form can be used as a midway point between LaTex
        and normal Python (sympy) formats. It is also useful for pointers.
        (e.g '\$frac{1}{2}$' (LaTeX) --> (parse) --> ['\FRAC{', '1', '}', '{', '2', '}']
        --> (compile) --> '(1)/(2)' --> (evaluate) --> 0.5)

        
        Returns:

            Returns self.parsed, which is the list that 'primary_parse' has generated."""

        original_text = text # this will not change, which lets us determine if the argument was None later on
        if text == None:
            text = self.latex

        # check if the text starts and ends with $ (to confirm it is a LaTeX string)
        if (text[0], text[-1]) != ("$", "$") and require_dollars:
            raise typemathtextError("The input text must begin and end with a '$' symbol")

        # isolate keywords into list
        output = []
        for char in text:
            if char not in (" ", "$"):
                output.append(char)

        # uses parse_info.json to properly combine characters into term
        output = self.__fixup(output)
        
        # connect consecutive numbers, multiply consecutive numbers & variables to create terms
        output = self.__concatenate_ints(output)

        # if the original argument for 'text' was None (which means to edit 'parsed' argument instead)
        if original_text is None:
            self.parsed = output

        return output

    def compile(self, text = None):
        """Fully converts the parsed text list into a sympy-readable format as a
        string to be executed.

        Only the current parsed LaTeX text is compiled. Instead of directly
        calling this function, it is automatically called when a new typemath
        instance is initiated, and is also called automatically when the 'typemath.edit'
        method is called.
        

        Returns:

            This returns the new string and also puts it in the attribute 'compiled'."""

        # if text is not set, automatically compile attribute 'parsed' instead
        if text is None:
            output = self.parsed.copy() # setting a variable to a list only creates a new reference, not id
        else:
            output = text
        
        with open(self._parse_info_dir, "r") as f:
            doc_ = json.load(f)
            keywords = doc_["keywords"]
            keywords_get = [item[0] for item in keywords]
            keywords_set = [item[1] for item in keywords]

            specials = doc_["specials"]
            specials_get = [item[0] for item in specials]
            specials_set =[item[1] for item in specials]
        
        for i in range(len(keywords)):
            output = self.__swap(output, keywords_get[i], keywords_set[i])

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

        # join together output and return
        output = "".join(output)
        if text is None:
            self.compiled = output
        return self.compiled

    def edit(self, latex_input = None, parsed_input = None,
            latex_insert = None, parsed_insert = None, abs_pointer = None):
        """Edits latex text by parsing, editing, repositioning the pointer, recompiling.


        Parameters:
        
            latex_input (str/None) -- the LaTeX string that is to be edited. (default: None)

                                    If this and 'parsed_input' are both None, then the
                                    instance's 'parsed' attribute will automatically be
                                    edited.
                                    If both this and 'parsed_input' are set, then 'parsed_input'
                                    will automatically be used, rather than this.

            parsed_input (list/None) -- the already parsed list that is to be edited. (default: None)

                                    If this and 'latex_input' are both None, then the
                                    instance's 'parsed' attribute will automatically be
                                    edited.
                                    If both this and 'latex_input' are set, then this
                                    will automatically be used, rather than 'latex_input'.

            latex_insert (str/None) -- the LaTeX string to be inserted in. (default: None)

                                    If this and 'parsed_insert' are both None, then an error
                                    will occur. If you wish to only change the pointer attribute,
                                    then use the 'set_pointer' method.
                                    If both this and 'parsed_insert' are set, then 'parsed_insert'
                                    will automatically be used, rather than this.

            parsed_insert (list/None) -- the already parsed list that is to be edited. (default: None)

                                    If this and 'latex_insert' are both None, then an error
                                    will occur. If you wish to only change the pointer attribute,
                                    then use the 'set_pointer' method.
                                    If both this and 'latex_insert' are set, then this will
                                    automatically be used, rather than 'latex_insert'.
            
            abs_pointer (int/None) -- the absolute position in the parsed list where the pointer
                                      will move to. (default: None)

                                    If this value is equal to none, the default will become the
                                    'pointer' attribute of the instance.


        Returns:

                The new value of the text in the parsed list format. If no input arguments
                ('latex_input' and 'parsed_input') are given, then the instance's attributes
                are also updated, and self.parsed is returned.

        
        Example:

            my_integral = typemath("$\int 4x^2 dx$") -> This gets parsed to ["\int", "4", "*", "x", "**", "2", "dx"]
            my_integral.edit(latex_insert = "$+4$")

            As typemath() automatically sets its instance attribute 'pointer' to the length of the parsed text, it will
            edit the end. In this example, 'pointer' will first equal 7. When edit() is called, "8" will be appended
            to the end of the 'parsed' attribute, and its 'pointer' attribute will increase by one. All other attributes
            will be automatically updated with it, which is why this method is useful.

            Hence, this method results in:
            my_integral.parsed = ["\int", "4", "*", "x", "**", "2", "dx", "+", "4"]
            my_integral.compiled = "sympy.integrate(4*sympy.symbols("x")**2, sympy.symbols("x"))+4"
            my_integral.pointer = 9"""

        # check value types
        if latex_input is not None:
            if not isinstance(latex_input, str):
                raise typemathtextError("'latex_input' must be either a string or None")
        if parsed_input is not None:
            if not isinstance(parsed_input, list):
                raise typemathtextError("'parsed_input' must be either a list or None")
        if latex_insert is not None:
            if not isinstance(latex_insert, str):
                raise typemathtextError("'latex_insert' must be either a string or None")
        if parsed_insert is not None:
            if not isinstance(parsed_insert, list):
                raise typemathtextError("'parsed_insert' must be either a list or None")
        if abs_pointer is not None:
            if not isinstance(abs_pointer, int):
                raise typemathtextError("'abs_pointer' must be either an integer or None")

        # equal value warnings
        if latex_input is not None and parsed_input is not None:
            warnings.warn("typemathtext: 'latex_input' and 'parsed_input' are both set. Automatically using 'parsed_input'.")
            latex_input = None
        if latex_insert is not None and parsed_insert is not None:
            warnings.warn("typemathtext: 'latex_insert' and 'parsed_insert' are both set. Automatically using 'parsed_insert'.")
            latex_insert = None
        if latex_insert is None and parsed_insert is None:
            raise typemathtextError("Something must be inserted to edit. If you wish to move the pointer, use the 'set_pointer' method.")

        # set values
        reference_self = False

        if latex_input is not None:
            parsed_input = self.parse(latex_input)
        if (latex_input, parsed_input) == (None, None):
            reference_self = True
            parsed_input = self.parsed
            pointer = self.pointer
        else:
            if abs_pointer is None:
                pointer = len(parsed_input)
            else:
                pointer = abs_pointer

        # If a LaTeX string is inserted, parse it first
        if latex_insert is not None:
            parsed_insert = self.parse(latex_insert)
        
        # As parsed_insert will be a list, insert each of its item to the main list and adjust the pointer
        for i in parsed_insert:
            parsed_input.insert(pointer, i)
            pointer += 1
            if abs_pointer is None:
                self.pointer += 1

        # if it is the instance that is edited, adjust accordingly
        if reference_self:
            self.parsed = parsed_input
            self.refresh(self.parsed)

        return parsed_insert

    def remove(self, removals, pointer_pos = None): # rename removals

        # pointer_pos defaults sets it automatically
        if pointer_pos == None:
            pointer_pos = self.pointer

        i = 1
        while i <= removals:
            self.parsed.pop(pointer_pos - 1)
            pointer_pos -= 1
            i += 1

        self.pointer = pointer_pos

        self.refresh(self.parsed)

        return self.parsed

    def deparse(self):
        pass
    
    def decompile(self):
        pass

    def refresh(self, origin):
        # adjust other values (for when one changes, so attributes are not desynced)

        if origin is self.parsed:
            origin = self.__fixup(origin)
            self.deparse()
            self.compile()
            try:
                self.evaluate = eval(self.compiled)
            except: # self.compiled may not have correct syntax and return an error
                self.evaluate = None
    
    # dunders

    def __add__(self, other):
        r"""returns a new instance of typemath that adds the value of one typemath
        object and either another typemath object or a LaTeX string (shown with
        wrapping dollar signs)
        
        If you are looking to reassign a function when adding, use += or edit()
        
        
        Example:
            expr_1 = typemath(r"$\int 4x dx$")
            expr_2 = typemath(r"\frac{82}{2}")
            
            Input:
                expr_1 + expr_2

            Returns:
                r"$\int 4x dx + \frac{82}{2}$"
            
            However, this is not a string, but the represented (__repr__) version
            of a new typemath() object, returning its 'latex' attribute."""

        if type(other) is str: # when added to a string (presumed LaTeX string)
            temp_typemath_object = typemath(self.latex)
            temp_typemath_object.edit(latex_insert = f"+{other}")
            return temp_typemath_object
        if type(other) is typemath: # when added to another typemath object
            temp_typemath_object = typemath(self.latex)
            temp_typemath_object.edit(latex_insert = "$+$")
            temp_typemath_object.edit(latex_insert = f"{other.latex}")
            return temp_typemath_object


    def __pe__(self, other):
        """Does the same as __add__, but stores the new object into the
        first typemath() object, rather than creating a new object
        
        See the __add__() method's help page for how this will behave."""

        self = self + other

    def __repr__(self):
        """Returns the 'compiled' attribute of the typemath object."""
        return self.compiled

    def __concatenate_chars(self, chars, string):
        # concatenates consecutive items in a string if they match some string
        # e.g. __concatenate_chars(["h", "e", "l", "l", "o"], "he") returns ["he", "l", "l", "o"]

        output = chars.copy()
        for i in range(len(chars)):
            place_check = ""
            for k in range(len(string)):
                try:
                    place_check += output[i + k]
                except:
                    break
            if place_check == string:
                output[i] = string
                q = len(string) - 1
                if len(string) > 2:
                    while q > 0:
                        output.pop(i + 1)
                        q -= 1
        return output
    
    @staticmethod
    def __concatenate_ints(lst):
        # concatenates consecutive numbers, and automatically inserts * for variables next to numbers
        # e.g. __concatenate_ints(["5", "4", "x"]) returns ["54", "*", "x"]

        output = []
        numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        tuple_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'x', 'y', "math.e", "math.pi")
        for i in range(len(lst)):
            try:
                if lst[i] in tuple_list and lst[i - 1] in tuple_list:
                    if lst[i] in ("x", "y", "math.e", "math.pi"):
                        output.append("*")
                        output.append(lst[i])
                    else:
                        output[-1] += lst[i]
                else:
                    output.append(lst[i])
            except:
                output.append(lst[i])
        return output
    
    def __swap(self, lst, old, new):
        # __swaps some value with a new one in a list for all instances of that value
        # e.g. __swap([5, 4, 2, 5], 5, 1) returns [1, 4, 2, 5] - the 5's get replaced with 1

        lst = lst.copy()
        i = 0
        for item in lst:
            if item == old:
                lst[i] = new
            i += 1
        return lst
    
    def __fixup(self, lst):
        # internal function to join together special values as defined in parse_info.json
        # this does most of the parsing

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
            lst = self.__concatenate_chars(lst, specials_get[i])
            lst = self.__swap(lst, specials_get[i], specials_set[i])
        for i in range(len(keywords)):
            lst = self.__concatenate_chars(lst, keywords_get[i])
        for i in range(len(pointouts)):
            lst = self.__concatenate_chars(lst, pointouts_get[i])
            lst = self.__swap(lst, pointouts_get[i], pointouts_set[i])
        
        return lst