"""Module that contains wrapper for LexerGenerator from 'rply'"""

from rply import LexerGenerator
from rply.lexer import Lexer


class LexWrapper:
    """Class that contains all tokens and its regular expressions for 'C'
    language.

    Also generates lexer and lexems from 'C' source code.
    """

    tokens = (
        ('MAIN', r'\bmain\b'),
        ('TYPE', r'\bint\b|\bfloat\b'),
        ('RETURN', r'\breturn\b'),
        ('HEX', r'0[xX][a-fA-F\d]+'),
        ('DECIMAL', r'\d+(\.?\d*)'),
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


if __name__ == '__main__':
    PATH_TO_SOURCE_FILE = 'source_files/source.c'
    with open(PATH_TO_SOURCE_FILE, 'r') as file:
        source_code = file.read()

    lex_wrapper = LexWrapper()
    lexer = lex_wrapper.build_lexer()
    tokens = lexer.lex(source_code)

    for token in tokens:
        print(token)
