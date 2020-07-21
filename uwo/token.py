W_PLUS = "pwus"
W_MINUS = "sub"
W_MUL = "muw"
W_DIV = "div"
W_VAR = "vaw"
W_END_STATMENT = ";"

TT_EOF = "eof"
TT_LPAREN = "left_paren"
TT_RPAREN = "right_paren"
TT_PLUS = "addition"
TT_MINUS = "subtraction"
TT_MUL = "multiplicaton"
TT_DIV = "division"
TT_VAR = "declaration"
TT_END_STATMENT = "eos"
TT_INT = "int"
TT_FLOAT = "float"
TT_PRINT = "print"
TT_REF = "ref"

possible_values = [W_PLUS, W_MINUS, W_MUL, W_DIV]


def formatPossibleValues():
    return "{} or {}".format(", ".join(possible_values[:-1]),  possible_values[-1])

def createToken(pos_start, word):
        type=None
        if(W_VAR in str(word)):
            type=TT_VAR
        elif(isinstance(word, int)):
            type="int"
        elif(isinstance(word, float)):
            type="float"
        elif(word == W_END_STATMENT):
            type=TT_END_STATMENT
        elif(word == "="):
            type="assignment"
        elif(word == "=="):
            type="comparison"
        elif(word == "pwint"):
            type=TT_PRINT
        elif(word == W_MUL):
            type=TT_MUL
        elif(word == W_DIV):
            type=TT_DIV
        elif(word == W_PLUS):
            type=TT_PLUS
        elif(word == W_MINUS):
            type=TT_MINUS
        elif(word == "("):
            type=TT_LPAREN
        elif(word == ")"):
            type=TT_RPAREN
        else:
            type=TT_REF
        return Token(type, word, pos_start)

class Token:
    def __init__(self, type_, value = None, pos_start = None, pos_end = None):
        self.type=type_
        self.value=value

        if pos_start:
            self.pos_start=pos_start.copy()
            self.pos_end=pos_start.copy()
            self.pos_end.advance("", 1)

        if pos_end:
            self.pos_end=pos_end
    def __repr__(self):
        if self.value:
            return f'{self.type}:"{self.value}"'
        return f'{self.type}'
