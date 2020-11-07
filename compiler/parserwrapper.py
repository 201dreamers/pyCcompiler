"""Module contains ParseWrapper for ParserGenerator from 'rply'"""

from rply import ParserGenerator
from rply.token import Token

from compiler.lexwrapper import LexWrapper
from compiler.nodes import (Function, Return, UnaryExpression,
                            BinaryExpression, Variable)
from compiler import errors
from config import logger


class ParserWrapper:
    """Class for defining grammar rules of 'C' language and parsing it's source
    code

    It uses tokens configured in LexWrapper
    """

    def __init__(self):
        self.tokens = [token for token, regexp in LexWrapper.tokens]
        self.precedence = (
            ('left', ['=']),
            ('left', ['==']),
            ('left', ['*', '/']),
            ('left', ['-']),
            ('left', ['('])
        )
        self.pg = ParserGenerator(self.tokens, precedence=self.precedence)

    def parse(self):

        @self.pg.production(
            'program : TYPE MAIN ( ) { function_body }')
        def program(parsed):
            main_func = Function(
                name=parsed[1].value,
                type_=parsed[0].value,
                body=parsed[5]
            )

            return main_func

        @self.pg.production('function_body : instruction semicolons')
        @self.pg.production(
            'function_body : function_body instruction semicolons')
        def function_body(parsed):
            body = []
            if (_len_of_parsed := len(parsed)) == 2:
                body.append(parsed[0])
            elif _len_of_parsed == 3:
                body.extend(parsed[0])
                body.append(parsed[1])

            return body

        @self.pg.production('instruction : RETURN expression | variable')
        @self.pg.production('instruction : IDENTIFIER = expression')
        @self.pg.production('instruction : TYPE IDENTIFIER')
        @self.pg.production('instruction : TYPE IDENTIFIER = expression')
        def instruction(parsed):
            if parsed[0].name == 'IDENTIFIER':
                if parsed[0].value in Variable.all_variables:
                    _var = Variable.all_variables[parsed[0].value]
                    _var.expression = parsed[2]
                else:
                    raise errors.VariableDoesNotExistsError(parsed[0])
                return _var
            elif parsed[0].name == 'TYPE':
                var = Variable(type_=parsed[0].value, name=parsed[1].value)
                if len(parsed) == 4:
                    var.expression = parsed[3]
                    return var
                return
            elif parsed[0].name == 'RETURN':
                return Return(argument=parsed[1])

        @self.pg.production('expression : number | variable')
        @self.pg.production('expression : expression == expression | - expression')
        @self.pg.production('expression : expression / expression | expression * expression')
        @self.pg.production('expression : ( expression )')
        def expression(parsed):
            if (_len_of_parsed := len(parsed)) == 2:
                return UnaryExpression(parsed[1])
            elif _len_of_parsed == 3:
                if isinstance(parsed[0], Token) and parsed[0].value == '(':
                    return expression([parsed[1]])
                elif parsed[1].name == '/' and\
                        BinaryExpression.operand_is_zero(parsed[2]):
                    raise errors.DivisionByZeroError(parsed[1])
                else:
                    return BinaryExpression(left_operand=parsed[0],
                                            right_operand=parsed[2],
                                            operator=parsed[1].value)
            return parsed[0]

        @self.pg.production('variable : IDENTIFIER')
        def variable(parsed):
            if parsed[0].value in Variable.all_variables:
                _var = Variable.all_variables[parsed[0].value]
                if _var.expression is None:
                    raise errors.VariableIsNotInitializedError(parsed[0])
            else:
                raise errors.VariableDoesNotExistsError(parsed[0])
            return _var

        @self.pg.production('number : DECIMAL | HEX')
        def number(parsed):
            if parsed[0].name == 'DECIMAL':
                parsed[0].value = int(parsed[0].value)
            elif parsed[0].name == 'HEX':
                parsed[0].value = int(parsed[0].value, base=16)
            return parsed[0].value

        @self.pg.production('semicolons : ; | semicolons ;')
        def semicolons(parsed):
            pass

        @self.pg.error
        def error_handler(token):
            logger.debug(f'{token=}')
            raise errors.CodeError(token)

    def build_parser(self):
        return self.pg.build()
