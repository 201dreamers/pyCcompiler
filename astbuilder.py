from __future__ import annotations

import json
from dataclasses import asdict
from lexwrapper import LexWrapper
from parserwrapper import ParserWrapper


class ASTBuilder:
    """Class for building Abstract Syntax Tree from main node

    AST - abstract syntax tree
    """

    def __init__(self, source_file: str):
        self.source_file = source_file

        with open(source_file, 'r') as file:
            self.source_code = file.read()

    def __build_lexer(self):
        lexwrapper = LexWrapper()
        lexer = lexwrapper.build_lexer()
        self.tokens = lexer.lex(self.source_code)

    def __build_parser(self):
        parser_wrapper = ParserWrapper()
        parser_wrapper.parse()

        parser = parser_wrapper.build_parser()
        self.parsed = parser.parse(self.tokens)

    def build_tree(self):
        self.__build_lexer()
        self.__build_parser()

        self.ast = asdict(self.parsed)

    def print_ast(self):
        print(json.dumps(self.ast, indent=4))
