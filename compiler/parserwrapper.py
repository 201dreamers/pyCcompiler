"""Module contains ParseWrapper for ParserGenerator from 'rply'"""

from rply import ParserGenerator

from compiler.lexwrapper import LexWrapper
from compiler.nodes import (Function, Return, UnaryOperation,
                            BinaryOperation)
from compiler.errors import CodeError


class ParserWrapper:
    """Class for defining grammar rules of 'C' language and parsing it's source
    code

    It uses tokens configured in LexWrapper
    """

    def __init__(self):
        self.tokens = [token for token, regexp in LexWrapper.tokens]
        self.pg = ParserGenerator(self.tokens)

    def parse(self):

        @self.pg.production(
            "program : TYPE MAIN ( ) { functionbody }")
        def program(parsed):
            # if parsed[0].value == 'float':
            #     parsed[5].argument.value = float(parsed[5].argument.value)
            # elif parsed[0].value == 'int':
            #     parsed[5].argument.value = int(parsed[5].argument.value)

            main_func = Function(
                name=parsed[1].value,
                type_=parsed[0].value,
                body=parsed[5]
            )

            return main_func

        @self.pg.production("functionbody : RETURN expression semicolons")
        def fucntionbody(parsed):
            return Return(expression=parsed[1])

        @self.pg.production("expression : number")
        @self.pg.production("expression : - number")
        @self.pg.production("expression : number / number")
        def expression(parsed):
            if len(parsed) == 2:
                return UnaryOperation(operand=parsed[1])
            elif len(parsed) == 3:
                return BinaryOperation(left_operand=parsed[0],
                                       right_operand=parsed[2])
            return parsed[0]

        @self.pg.production("number : HEX")
        @self.pg.production("number : DECIMAL")
        def number(parsed):
            if parsed[0].name == 'DECIMAL':
                parsed[0].value = float(parsed[0].value)
            elif parsed[0].name == 'HEX':
                parsed[0].value = int(parsed[0].value, base=16)
            return parsed[0].value

        @self.pg.production("semicolons : ;")
        @self.pg.production("semicolons : semicolons ;")
        def semicolons(parsed):
            pass

        @self.pg.error
        def error_handler(token):
            raise CodeError(token)

    def build_parser(self):
        return self.pg.build()
