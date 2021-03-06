from .errors import *
from .token import *


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class ReferenceNode:
    def __init__(self, name, var, pos_start, pos_end):
        self.name = name
        self.var = var

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'(reference:{self.name})'


class VariableNode:
    def __init__(self, name, value, pos_start, pos_end):
        self.name = name
        self.value = value

        self.pos_start = pos_start

    def __repr__(self):
        return f'({self.name} = {self.value})'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_start = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

#######################################
# PARSE RESULT
#######################################


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# PARSER
#######################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.curr_name = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.var(self.expr())
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected " + formatPossibleValues()
            ))

        return self.ref(res)

    ###################################

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
        ))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def ref(self, res):
        if self.current_tok.type == TT_REF:       
            og = self.current_tok    
            res.register(self.advance())
            self.advance()  
            ref_node = ReferenceNode(og.value, self.curr_name, og.pos_start, og.pos_end)
            return res.success(ref_node)
        return res
    def var(self, res):
        if self.current_tok.type == TT_VAR:
            self.curr_name = self.current_tok.value.replace("vaw ", "")
            res.register(self.advance())
            self.advance()
            
            value = res.register(self.expr())
            if isinstance(value, NumberNode):
                value = value.node

            left = VariableNode(self.curr_name, value, self.current_tok.pos_start, self.current_tok.pos_end)

            return res.success(left)

        return res

    def expr(self):
        res = self.bin_op(self.term, (TT_PLUS, TT_MINUS))

        return res
    ###################################

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
