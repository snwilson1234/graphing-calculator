from math_interpreter.tokens import TokenType
import numpy as np

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return RTResult().success(node.tok.value)
    
    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left))
        if res.error: return res
        right = res.register(self.visit(node.right))

        if node.op_tok.type == TokenType.PLUS:
            result = left + right
        elif node.op_tok.type == TokenType.MINUS:
            result = left - right
        elif node.op_tok.type == TokenType.MULT:
            result = left * right
        elif node.op_tok.type == TokenType.DIV:
            if right != 0:
                result = left / right
            else:
                result = "div by 0"
        
        # if error:
        #     return res.failure(error)
        # else:
        return res.success(result)

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        val = res.register(self.visit(node.node))

        if res.error: return res

        if node.op_tok.type == TokenType.MINUS:
            result = (-1) * val
        elif node.op_tok.type == TokenType.SIN:
            result = np.sin(val)
        elif node.op_tok.type == TokenType.COS:
            result = np.cos(val)
        elif node.op_tok.type == TokenType.TAN:
            result = np.tan(val)
        elif node.op_tok.type == TokenType.LOG:
            result = np.log10(val)
        elif node.op_tok.type == TokenType.NLOG:
            result = np.log(val)
        
        return res.success(result)

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self,value):  
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self 