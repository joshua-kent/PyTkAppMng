import json
import os

class typemathtextError(Exception):
    pass

class text:
    latex_text = ""
    parsed_latex_text = []
    pointer = 0
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parse_info_dir = os.path.join(current_dir, "parse_info.json")

    def __init__(self):
        self.parse_latex(r"\int4x+\int2dx-3dx+\int4+\int2dxdx")

    def edit(self, text, moveby = 1, moveto = None):
        if moveby == moveto == None or None not in (moveby, moveto):
            raise typemathtextError("moveby and moveto cannot be set simultaneously")

    def concatenate_chars(self, chars, *args):
        """
        Add this in!!
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
