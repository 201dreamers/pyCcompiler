from rply import LexerGenerator
from rply.lexer import Lexer


class LexWrapper:

    tokens = (
        ('MAIN', r'\bmain\b'),
        ('TYPE', r'\bint\b|\bfloat\b'),
        ('RETURN', r'\breturn\b'),
        ('NUMBER', r'\d+(\.?\d*)'),
        # ('IDENTIFIER', r'[a-z]\w*'),
        ('(', r'\('),
        (')', r'\)'),
        ('{', r'\{'),
        ('}', r'\}'),
        (';', r';'),
    )

    def __init__(self):
        self.lex_generator = LexerGenerator()

    def __add_rules(self):
        for token, regexp in self.tokens:
            self.lex_generator.add(token, regexp)

        self.lex_generator.ignore(r'//.*|\s+')

    def build_lexer(self) -> Lexer:
        self.__add_rules()

        return self.lex_generator.build()
