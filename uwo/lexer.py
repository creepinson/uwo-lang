import re
from .errors import *
from .pos import *
from .utils import *
from .token import *


class Lexer():
    def __init__(self, fn, text):
        self.current_char = None
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.advance(1)

    def advance(self, amount):
        self.pos.advance(self.current_char, amount)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def tokenize(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t\n\r':
                self.advance(1)
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "(":
                tokens.append(createToken(self.pos, self.current_char))
                self.advance(1)
            elif self.current_char == ")":
                tokens.append(createToken(self.pos, self.current_char))
                self.advance(1)
            elif(self.text[self.pos.idx:self.pos.idx+3] == "vaw"):
                if(self.current_char and self.current_char.isalpha()):
                    name = self.text[self.pos.idx:len(
                        self.text)-1].split()[1:][0]
                    tokens.append(createToken(self.pos, f"vaw {name}"))
                    self.advance(4 + len(name))
            elif(self.text[self.pos.idx:self.pos.idx+4] == "pwus"):
                tokens.append(createToken(self.pos, "pwus"))
                self.advance(4)
            elif(self.text[self.pos.idx:self.pos.idx+3] == "sub"):
                tokens.append(createToken(self.pos, "sub"))
                self.advance(3)
            elif(self.text[self.pos.idx:self.pos.idx+5] == "pwint"):
                tokens.append(createToken(self.pos, "pwint"))
                self.advance(5)
            elif(self.current_char == "="):
                if(self.text[self.pos.idx+1] != "="):
                    tokens.append(createToken(self.pos, self.current_char))
                    self.advance(1)
                else:
                    tokens.append(createToken(self.pos, "=="))
                    self.advance(2)
            elif self.current_char and self.current_char.isalpha():
                res = ""
                while self.current_char and self.current_char.isalpha():
                    res += self.current_char
                    self.advance(1)
                if res != "":
                    tokens.append(createToken(self.pos, res))
            elif self.current_char == ";":
                tokens.append(createToken(self.pos, self.current_char))
                self.advance(1)
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance(1)
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance(1)

        if dot_count == 0:
            return createToken(self.pos, int(num_str))
        else:
            return createToken(self.pos, float(num_str))
