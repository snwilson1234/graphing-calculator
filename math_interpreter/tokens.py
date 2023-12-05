from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    NUMBER      = 0
    PLUS        = 1
    MINUS       = 2
    MULT        = 3
    DIV         = 4
    LPAREN      = 5
    RPAREN      = 6
    SIN         = 7
    COS         = 8
    TAN         = 9
    LOG         = 10
    NLOG        = 11

@dataclass
class Token:
    type: TokenType
    value: any

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")
