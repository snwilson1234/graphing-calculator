from _ast import BinOp, Expression, UnaryOp
import ast
import math
from typing import Any

class Interpreter(ast.NodeVisitor):
    def visit_BinOp(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return left_value + right_value
        elif isinstance(node.op, ast.Sub):
            return left_value - right_value
        elif isinstance(node.op, ast.Mult):
            return left_value * right_value
        elif isinstance(node.op, ast.Div):
            if right_value == 0:
                #raise ValueError("Division by zero!")
                return "ERROR"
            return left_value / right_value
        else:
            return "ERROR"
            #raise ValueError("Invalid expression!")
        
    def visit_Num(self, node):
        return node.n
    
    def visit_UnaryOp(self, node: UnaryOp):
        operand_value = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand_value
        elif isinstance(node.op, ast.USub):
            return -operand_value
        else:
            return "ERROR"
            #raise ValueError("Invalid Unary Operand!")
        
    def evaluate_expression(self, expression):
        try:
            tree = ast.parse(expression, mode='eval')
            interpreter = Interpreter()
            return interpreter.visit(tree.body)
        except SyntaxError:
            return "ERROR"
            #raise ValueError("Invalid expression syntax!")
        
# my_interpreter = Interpreter()
# expression = "4 //0 "
# res = my_interpreter.evaluate_expression(expression)
# print(res)

OPERATORS = {

    '(': 'LPAR',
    ')': 'RPAR',
    '^': 'EXP',
    '*': 'MUL',
    '/': 'DIV',
    '+': 'ADD',
    '-': 'SUB',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',

}

DIGITS = ['0','1','2','3','4','5','6','7','8','9']

class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = self.tokenize()
    
    def tokenize(self):
        
        # make sure parantheses match
        if self.expression.count('(') != self.expression.count(')'):
            print("error: parantheses don't match")
            return None
        
        tokens = []
        i = 0
        length = len(self.expression)
        prev = '#'

        while i < length:
            curr = self.expression[i]
            trig = ''
            if i < length - 2:
                trig = self.expression[i: i + 3].lower()
            pi = ''
            if i < length - 1:
                pi = self.expression[i: i + 2].lower()
            if curr in OPERATORS:
                if (prev in OPERATORS or i == 0) and curr == '-':
                    tokens.append(('NEG', curr))
                else:
                    tokens.append((OPERATORS[curr], curr))
            elif trig in OPERATORS:
                tokens.append((OPERATORS[trig], trig))
                i += 2
            elif pi == 'pi':
                tokens.append(('NUM', math.pi))
                i += 1
            elif curr in DIGITS:
                while i + 1 < length and self.expression[i + 1] in DIGITS:
                    i += 1
                    curr += self.expression[i]
                tokens.append(('NUM', curr))
            i += 1
            prev = curr
        return tokens