from math_interpreter.tokens import TokenType
from math_interpreter.nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.num_toks = len(self.tokens)
        self.current_tok = tokens[0] if self.num_toks > 0 else None
    
    def advance(self):
        if self.idx < self.num_toks:
            self.idx += 1
            self.current_tok = self.tokens[self.idx] if self.idx < self.num_toks else None

    def parse(self):
        res = self.expr()
        # if not res.error and self.current_tok.type != TT_EOF: #still code not parsed but error not yet detected
            
            # return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected '+', '-', '*' or '/'"))
            
        return res

    def bin_op(self, func, ops): #shared by both term() and expr()
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        
        
        while self.current_tok is not None and self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.PLUS, TokenType.MINUS,TokenType.SIN,TokenType.COS,TokenType.TAN,TokenType.LOG,TokenType.NLOG):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type == TokenType.NUMBER:
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == (TokenType.LPAREN):
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TokenType.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            # else:
            #     return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        
        return res.failure("expected int or float")
        # return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float"))

    def term(self):
        return self.bin_op(self.factor, (TokenType.MULT, TokenType.DIV))

    def expr(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self