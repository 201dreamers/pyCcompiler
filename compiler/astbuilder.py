"""Module, contains Abstract Syntax Tree builder"""

from __future__ import annotations

import json
from dataclasses import asdict

from rply.errors import LexingError

from compiler.lexwrapper import LexWrapper
from compiler.parserwrapper import ParserWrapper
from compiler.errors import CodeError
from compiler.miscellaneous import exit_compiler


class ASTBuilder:
    """Class for building Abstract Syntax Tree from main node

    It creates lexer and parser, runs them and gets ready AST.
    Also it could pretty print AST to console.
    AST - abstract syntax tree
    """

    def __init__(self, source_file: str):
        self.source_file = source_file
        self.ast = None
        try:
            with open(source_file, 'r') as file:
                self.source_code = file.read()
        except FileNotFoundError:
            print("ERROR: no source file '1-3-Python-IO-81-Hakman.txt")
            exit_compiler(1)

    def __build_lexer(self):
        lexwrapper = LexWrapper()
        lexer = lexwrapper.build_lexer()
        self.tokens = lexer.lex(self.source_code)

    def __build_parser(self):
        parser_wrapper = ParserWrapper()
        parser_wrapper.parse()

        parser = parser_wrapper.build_parser()
        try:
            self.parsed = parser.parse(self.tokens)
        except CodeError as c_err:
            print(c_err.message)
            exit_compiler(1)
        except LexingError as l_err:
            l_err = CodeError(l_err)
            print(l_err.message)
            exit_compiler(1)

    def build_tree(self):
        self.__build_lexer()
        self.__build_parser()

        self.ast = asdict(self.parsed)

    def print_ast(self):
        print(json.dumps(self.ast, indent=4))
