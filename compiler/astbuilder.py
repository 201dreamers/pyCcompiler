"""Module, contains Abstract Syntax Tree builder"""

from __future__ import annotations

import json
from dataclasses import asdict

from rply.errors import LexingError

from compiler.lexwrapper import LexWrapper
from compiler.parserwrapper import ParserWrapper
from compiler import errors
from compiler.miscellaneous import exit_compiler


class ASTBuilder:
    """Class for building Abstract Syntax Tree from main node

    It creates lexer and parser, runs them and gets ready AST.
    Also it could pretty print AST to console.
    AST - abstract syntax tree
    """

    def __init__(self, source_file_name: str):
        self.source_file_name = source_file_name
        self.ast = None
        try:
            with open(source_file_name, 'r') as source_file:
                self.source_code = source_file.read()
        except FileNotFoundError:
            print(f"ERROR: no source file '{self.source_file_name}'")
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
            self.program = parser.parse(self.tokens)
        except (errors.CodeError,
                errors.VariableIsNotInitializedError,
                errors.VariableDoesNotExistsError,
                errors.DivisionByZeroError,
                errors.VariableAlreadyExistsError,
                errors.NoReturnStatementInFunctionError) as err:
            print(err.message)
            exit_compiler(1)
        except LexingError as l_err:
            l_err = errors.CodeError(l_err)
            print(l_err.message)
            exit_compiler(1)

    def build_tree(self):
        self.__build_lexer()
        self.__build_parser()

        self.ast = asdict(self.program)

    def print_ast(self):
        print(json.dumps(self.ast, indent=4))
