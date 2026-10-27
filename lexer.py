from re import compile
from dataclasses import dataclass
from sys import exit

def _err(code, line, column, err="", msg="", siz=1):
    cl = code.splitlines()
    e = cl[line - 1]
    l = len(f"Linea {line} | ")
    clc = (" " * l) + (" " * (column - 1))
    t = clc + ("^" * siz)
    return f"Linea {line} | {e}\n{t}\n{clc}{err if err else ''}{': ' if err and msg else ''}{msg if msg else ''}"

@dataclass
class Token:
    type: str
    value: str
    line: int = 1
    column: int = 1
    
    def __repr__(self):
        return f"Token(type={self.type!r}, value={self.value!r})"
    
    def __lrepr__(self):
        return f"Token(type={self.type!r}, value={self.value!r}, line={self.line}, column={self.column})"
    
    def __str__(self):
        return self.value


class Lexer:
    def __init__(self):
        self.term = {
            "WS": r"\s+",
            "LKEY": r"\{",
            "RKEY": r"\}",
            "NUMBER": r"\d+(\.\d+)?",
            "STRING": r'"([^"\n\\]|\\.)*"',
            "BOOL": r"(true)|(false)",
            "NULL": r"null",
            "LBRA": r"\[",
            "RBRA": r"\]",
            
            "COLON": r":",
            "COMMA": r",",
            
            "MM": r"."
        }
        self.re = compile("|".join(f"(?P<{t}>{r})" for t, r in self.term.items()))
    
    def tokenize(self, text):
        line = 1
        column = 1
        for m in self.re.finditer(text):
            term = m.lastgroup
            match = m.group()
            absp = m.start()
            line = text.count("\n", 0, absp) + 1
            
            ultj = text.rfind("\n", 0, absp)
            column = absp if ultj < 0 else absp - ultj
            
            if term == "WS":
                continue
            elif term == "MM":
                print(_err(text, line, column, "InvalidToken", f"Token invalido {match!r}"))
                exit(1)
            yield Token(term, match, line, column)
        yield Token("EOF", " ", line, column + 1)