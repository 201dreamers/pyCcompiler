from rply import ParserGenerator

from lexwrapper import LexWrapper
from nodes import Function, Return, Number
from errors import CodeError


class ParserWrapper:

    def __init__(self):
        tokens = [token for token, regexp in LexWrapper.tokens]
        self.pg = ParserGenerator(tokens)

    def parse(self):

        @self.pg.production(
            "program : TYPE MAIN ( ) { functionbody }")
        def program(parsed):
            return Function(name=parsed[1].value, type_=parsed[0].value,
                            children=parsed[5])

        @self.pg.production("functionbody : RETURN number semicolons")
        def fucntionbody(parsed):
            return Return(value=parsed[1])

        @self.pg.production("number : HEX")
        @self.pg.production("number : DECIMAL")
        def number(parsed):
            return Number(int(parsed[0].value))

        @self.pg.production("semicolons : ;")
        @self.pg.production("semicolons : semicolons ;")
        def semicolons(parsed):
            pass

        @self.pg.error
        def error_handler(token):
            raise CodeError(token)

    def set_line_number(self, parsed):
        print('\n\n')
        print(f'PARSED - {parsed}')
        for token in parsed:
            print(f'TOKEN: {token}')
            if token:
                pass
                # print(f'{token.getsourcepos()}')

    def build_parser(self):
        return self.pg.build()
