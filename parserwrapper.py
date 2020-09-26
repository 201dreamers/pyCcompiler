from rply import ParserGenerator

from lexwrapper import LexWrapper
from nodes import Function, Return, Number


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

        @self.pg.production("functionbody : RETURN NUMBER semicolons")
        def fucntionbody(parsed):
            return Return(value=Number(parsed[1].value))

        @self.pg.production("semicolons : ;")
        @self.pg.production("semicolons : semicolons ;")
        def semicolons(parsed):
            pass

        @self.pg.error
        def error_handler(token):
            raise ValueError(
                f"Ran into a {token.gettokentype()} where it wasn't expected")

    def build_parser(self):
        return self.pg.build()
