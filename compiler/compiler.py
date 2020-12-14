import json

from rply.errors import LexingError

from compiler.lexer_wrapper import lexer_generator
from compiler.parser_wrapper import parser_generator
from compiler.asm_code_generator import AsmCodeGenerator
from compiler import errors
from compiler.nodes import Program
from compiler.miscellaneous import exit_compiler


class Compiler():

    def __init__(self, path_to_source_file: str = 'source.c',
                 path_to_output_file: str = 'generated.asm'):
        self.path_to_source_file = path_to_source_file
        self.path_to_output_file = path_to_output_file

        self.parsed_program: Program
        self.ast: dict
        self.tokens: list
        self.source_code: str
        self.generated_code: str

    def __read_source_file(self):
        try:
            with open(self.path_to_source_file, 'r') as source_file:
                self.source_code = source_file.read()
        except FileNotFoundError:
            print(f"ERROR: no source file '{self.path_to_source_file}'")
            exit_compiler(1)

    def __do_lexing(self):
        lexer = lexer_generator.build()
        self.tokens = lexer.lex(self.source_code)

    def __do_parsing(self):
        parser = parser_generator.build()
        try:
            self.parsed_program = parser.parse(self.tokens)
        except (errors.CodeError,
                errors.VariableIsNotInitializedError,
                errors.VariableDoesNotExistsError,
                errors.DivisionByZeroError,
                errors.VariableAlreadyExistsError,
                errors.NoReturnStatementInFunctionError,
                errors.FunctionDoesNotExistsError,
                errors.MainFunctionDoesNotExistsError,
                errors.FunctionAlreadyExistsError,
                errors.ArgumentsDidNotMatchError) as err:
            print(err.message)
            exit_compiler(1)
        except LexingError as l_err:
            l_err = errors.CodeError(l_err)
            print(l_err.message)
            exit_compiler(1)

    def __build_abstract_syntax_tree(self):
        stringified_ast = self.parsed_program.generate_ast_representation()
        self.ast = json.loads(stringified_ast)

    def __generate_asm_code(self):
        code_generator = AsmCodeGenerator(self.parsed_program)
        self.generated_code = code_generator.generate_asm_code()

    def __write_generated_code_to_file(self):
        with open(self.path_to_output_file, 'w') as asm_file:
            asm_file.write(self.generated_code)

    def compile(self):
        self.__read_source_file()
        self.__do_lexing()
        self.__do_parsing()
        self.__build_abstract_syntax_tree()
        self.__generate_asm_code()
        self.__write_generated_code_to_file()

    def print_abstract_syntax_tree(self):
        print(json.dumps(self.ast, indent=4))
