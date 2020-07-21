from .token import *
from .parser import *
from .errors import *

class Number:
    def __init__(self, value):
        self.value = value

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def dived_by(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def __repr__(self):
        return str(self.value)


class Interpreter:
    def __init__(self):
        self.current_var = None
        self.variables = {}

    def __repr__(self):
        return f"(current: {self.current_var})"

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        if type(node).__name__ != "NoneType":
            raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_ReferenceNode(self, node):
        ref = self.variables.get(node.name)
        if ref:
            print(f"Creating vaw {node.var} with reference to {node.name}")
            self.current_var = ref
            self.variables[node.var] = self.current_var

            return ref[1]
        else:
            return UndefinedReferenceError(node.pos_start, node.pos_end, node.name)

    def visit_VariableNode(self, node):
        if(isinstance(node.value, BinOpNode)):
            value = self.visit(node.value)
            print(f"creating vaw {node.name} with value: {value}")
            self.current_var = [node, value]
            self.variables = self.variables.setdefault(node.name, self.current_var)
            return value
            
    def visit_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        result = Number(0)

        if node.op_tok.type == TT_PLUS:
            result = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result = left.dived_by(right)

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)

        if node.op_tok == TT_MINUS:
            number = number.multed_by(NUmber(-1))

        return number.set_pos(node.pos_start, node.pos_end)
