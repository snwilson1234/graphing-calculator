from math_interpreter.lexer import Lexer
from math_interpreter.parser_ import Parser
from math_interpreter.interpreter import Interpreter

def evaluate_expr(expression):
    lexer = Lexer(expression)
    tokens = lexer.make_tokens()

    parser = Parser(tokens)

    ast = parser.parse()

    interpreter = Interpreter()

    result = interpreter.visit(ast.node)

    print(result.value, result.error)
    return result.value, result.error
