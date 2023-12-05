from enum import Enum
from dataclasses import dataclass
from math_interpreter.tokens import Token,TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0
        self.expr_length = len(self.expression)
        self.current_char = self.expression[0] if self.expr_length > 0 else None
    
    def advance(self):
        if self.pos < self.expr_length:
            self.pos += 1
            self.current_char = self.expression[self.pos] if self.pos < self.expr_length else None
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, None))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS, None))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MULT, None))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV, None))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN, None))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN, None))
                self.advance()
            elif self.current_char in ALPHABET:
                tokens.append(self.make_function())
            elif self.current_char is None:
                return "invalid"

        print("THESE ARE THE TOKENS!!!: ",tokens)
        return tokens
            

    def make_number(self):
        num_str = self.current_char
        decimal_pt_count = 1 if num_str == "." else 0
        self.advance()

        while self.current_char is not None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_pt_count += 1
                if decimal_pt_count > 1:
                    print("error: invalid decimal pts")
                    break
            
            num_str += self.current_char
            self.advance()
        
        if num_str.startswith('.'):
            num_str = '0' + num_str
        
        if num_str.endswith('.'):
            num_str += '0'
        
        return Token(TokenType.NUMBER,float(num_str))

    def make_function(self):
        fun_str = self.current_char
        self.advance()

        while self.current_char is not None and (self.current_char in ALPHABET):
            fun_str += self.current_char
            self.advance()
        
        # Built-in Function types
        if fun_str == "sin":
            result = Token(TokenType.SIN,None)
        elif fun_str == "cos":
            result = Token(TokenType.COS,None)
        elif fun_str == "tan":
            result = Token(TokenType.TAN,None)
        elif fun_str == "log":
            result = Token(TokenType.LOG,None)
        elif fun_str == "ln":
            result = Token(TokenType.NLOG,None)
        else:
            print("invalid function")
        
        
        return result