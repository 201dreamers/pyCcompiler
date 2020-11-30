"""Module contains ParseWrapper for ParserGenerator from 'rply'"""

from rply import ParserGenerator
from rply.token import Token

from compiler.lexwrapper import LexWrapper
from compiler.nodes import (Function, Return, UnaryExpression,
                            BinaryExpression, Variable, TernaryExpression,
                            Program, FunctionCall)
from compiler import errors


class ParserWrapper:
    """Class for defining grammar rules of 'C' language and parsing it's source
    code

    It uses tokens configured in LexWrapper
    """

    def __init__(self):
        self.tokens = [token for token, regexp in LexWrapper.tokens]
        self.precedence = (
            ('left', ['/=', '=']),
            ('left', ['COLON']),
            ('left', ['?']),
            ('left', ['==']),
            ('left', ['*', '/']),
            ('left', ['-']),
            ('left', ['('])
        )
        self.pg = ParserGenerator(self.tokens, precedence=self.precedence)

    def parse(self):

        @self.pg.production('program : contents')
        def program(parsed):
            if 'main' not in Function.all_functions.keys():
                # TODO: Raise here error that main function is not exists
                pass

            return Program(contents=parsed[0])

        @self.pg.production('contents : function')
        @self.pg.production('contents : contents function')
        def contents(parsed):
            _contents = []
            if (_len_of_parsed := len(parsed)) == 1:
                _contents.append(parsed[0])
            elif _len_of_parsed == 2:
                parsed[0].append(parsed[1])
                _contents.extend(parsed[0])

            return _contents

        @self.pg.production('function : TYPE IDENTIFIER ( ) { function_body }')
        @self.pg.production('function : TYPE IDENTIFIER ( ) semicolons')
        def function(parsed):
            _function = Function.all_functions.get(parsed[1].value)
            if _function is None:
                _function = Function(
                    name=parsed[1].value,
                    type_=parsed[0].value,
                )

            if (len_of_parsed := len(parsed)) == 7:
                has_return_statement = False
                for line_of_code in parsed[5]:
                    if isinstance(line_of_code, Return):
                        has_return_statement = True
                        break

                if not has_return_statement:
                    raise errors.NoReturnStatementInFunctionError(
                        parsed[1].value)

                _function.body = parsed[5]
            elif len_of_parsed == 5:
                return

            return _function

        @self.pg.production('function_body : instruction semicolons')
        @self.pg.production(
            'function_body : function_body instruction semicolons')
        def function_body(parsed):
            _function_body = []
            if (len_of_parsed := len(parsed)) == 2:
                _function_body.append(parsed[0])
            elif len_of_parsed == 3:
                _function_body.extend(parsed[0])
                _function_body.append(parsed[1])

            return _function_body

        @self.pg.production('instruction : RETURN expression')
        @self.pg.production('instruction : IDENTIFIER = expression')
        @self.pg.production('instruction : IDENTIFIER /= expression')
        @self.pg.production('instruction : TYPE IDENTIFIER')
        @self.pg.production('instruction : TYPE IDENTIFIER = expression')
        def instruction(parsed):
            if parsed[0].name == 'TYPE':
                if parsed[1].value in Variable.all_variables:
                    raise errors.VariableAlreadyExistsError(parsed[1])
                var = Variable(type_=parsed[0].value, name=parsed[1].value)
                if len(parsed) == 4:
                    var.expression = parsed[3]
                    return var
                return
            elif parsed[0].name == 'IDENTIFIER':
                var = variable([parsed[0]])
                if parsed[1].name == '=':
                    var.expression = parsed[2]
                elif parsed[1].name == '/=':
                    var.expression = BinaryExpression(
                        left_operand=var,
                        right_operand=parsed[2],
                        operator='/'
                    )
                return var
            elif parsed[0].name == 'RETURN':
                return Return(argument=parsed[1])

        @self.pg.production('expression : number | variable | - expression')
        @self.pg.production('expression : function_call')
        @self.pg.production('expression : expression == expression')
        @self.pg.production(
            'expression : expression * expression | expression / expression')
        @self.pg.production(
            'expression : expression ? expression COLON expression')
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
            elif _len_of_parsed == 5:
                return TernaryExpression(
                    condition=parsed[0],
                    left_operand=parsed[2],
                    right_operand=parsed[4]
                )
            return parsed[0]

        @self.pg.production('function_call : IDENTIFIER ( ) ')
        def function_call(parsed):
            func = Function.all_functions.get(parsed[0].value)
            if func is None:
                # TODO: Raise error that no such function
                pass

            return FunctionCall(function_name=func.name)

        @self.pg.production('variable : IDENTIFIER')
        def variable(parsed):
            var = Variable.all_variables.get(parsed[0].value)
            if var is None:
                raise errors.VariableDoesNotExistsError(parsed[0])

            if var.expression is None:
                raise errors.VariableIsNotInitializedError(parsed[0])

            return var

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
            raise errors.CodeError(token)

    def build_parser(self):
        return self.pg.build()
