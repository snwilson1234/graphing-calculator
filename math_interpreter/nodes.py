

class NumberNode:
    def __init__(self,tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self,left,op_tok,right):
        self.left = left
        self.op_tok = op_tok
        self.right = right
    
    def __repr__(self):
        return f'{self.left},{self.op_tok},{self.right}'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'