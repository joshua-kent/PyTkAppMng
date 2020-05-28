import json

class typemathtextError(Exception):
    pass

class text:
    latex_text = ""
    parsed_latex_text = []
    pointer = 0

    def __init__(self):
        self.parse_latex("\int4x+\int2dx-3dx+\int4+\int2dxdx")

    def edit(self, text, moveby = 1, moveto = None):
        if moveby == moveto == None or None not in [moveby, moveto]:
            raise typemathtextError("moveby and moveto cannot be set simultaneously")

    def concatenate_chars(self, chars, *args): # for a list, this will combine characters together
        # ie. concatenate_chars(["a", "b", "c", "d"], "abc") returns ["abc", "d"]
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
        with open("parse_info.json", "r") as f:
            keywords = json.load(f)["keywords"]
        for word in keywords:
            self.concatenate_chars(output, word)
        print(output)

if __name__ == "__main__":
    txt = text()