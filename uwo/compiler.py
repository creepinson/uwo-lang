from .lexer import Lexer
from .parser import *
from .interpreter import Interpreter


def read(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.tokenize()

    if error:
        return None, error
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return tokens, error, ast


def readScript(file_name):
    content = ""
    with open(file_name, "r") as file:
        content = file.read()

    return read(file_name, content)


def run(result):
    interpreter = Interpreter()
    return (interpreter, interpreter.visit(result[2].node))
