"""Module contains ParseWrapper for ParserGenerator from 'rply'"""

from rply import ParserGenerator
from rply.token import Token

from compiler import lexer_wrapper
from compiler.nodes import (Function, Return, UnaryExpression,
                            BinaryExpression, Variable, TernaryExpression,
                            Program, FunctionCall)
from compiler import errors


token_names = [token_name for token_name, _ in lexer_wrapper.tokens]
precedence = (
    ('left', ['=', '/=']),
    ('left', ['COLON']),
    ('left', ['?']),
    ('left', ['==']),
    ('left', ['*', '/']),
    ('left', ['-']),
    ('left', ['('])
)
parser_generator = ParserGenerator(token_names, precedence=precedence)


@parser_generator.production('program : contents')
def program(parsed):
    if 'main' not in Program.all_functions.keys():
        # TODO: Raise here error that main function is not exists
        pass

    return Program(contents=parsed[0])


@parser_generator.production('contents : function')
@parser_generator.production('contents : contents function')
def contents(parsed):
    _contents = []
    if (_len_of_parsed := len(parsed)) == 1:
        _contents.append(parsed[0])
    elif _len_of_parsed == 2:
        parsed[0].append(parsed[1])
        _contents.extend(parsed[0])

    return _contents


@parser_generator.production(
    'function : TYPE IDENTIFIER ( arguments ) { function_body }')
@parser_generator.production(
    'function : TYPE IDENTIFIER ( arguments ) semicolons')
def function(parsed):
    _function = Program.all_functions.get(parsed[1].value)
    if _function is None:
        _function = Function(
            name=parsed[1].value,
            type_=parsed[0].value,
            arguments=parsed[3]
        )

    if (len_of_parsed := len(parsed)) == 8:
        has_return_statement = False
        for line_of_code in parsed[6]:
            if isinstance(line_of_code, Return):
                has_return_statement = True
                break

        if not has_return_statement:
            raise errors.NoReturnStatementInFunctionError(
                parsed[1].value)

        _function.body = parsed[6]
    elif len_of_parsed == 6:
        return

    return _function


@parser_generator.production('arguments : ')
def arguments(parsed):
    return []


@parser_generator.production('function_body : instruction semicolons')
@parser_generator.production(
    'function_body : function_body instruction semicolons')
def function_body(parsed):
    _function_body = []
    if (len_of_parsed := len(parsed)) == 2:
        _function_body.append(parsed[0])
    elif len_of_parsed == 3:
        _function_body.extend(parsed[0])
        _function_body.append(parsed[1])

    return _function_body


@parser_generator.production('instruction : RETURN expression')
@parser_generator.production('instruction : IDENTIFIER = expression')
@parser_generator.production('instruction : IDENTIFIER /= expression')
@parser_generator.production('instruction : TYPE IDENTIFIER')
@parser_generator.production('instruction : TYPE IDENTIFIER = expression')
def instruction(parsed):
    # BUG: Variable generation when reassign exists
    if parsed[0].name == 'TYPE':
        if parsed[1].value in Function.all_variables:
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


@parser_generator.production('expression : number | variable | - expression')
@parser_generator.production('expression : function_call')
@parser_generator.production('expression : expression == expression')
@parser_generator.production(
    'expression : expression * expression | expression / expression')
@parser_generator.production(
    'expression : expression ? expression COLON expression')
@parser_generator.production('expression : ( expression )')
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


@parser_generator.production('function_call : IDENTIFIER ( ) ')
def function_call(parsed):
    func = Program.all_functions.get(parsed[0].value)
    if func is None:
        # TODO: Raise error that no such function
        pass

    return FunctionCall(function_name=func.name)


@parser_generator.production('variable : IDENTIFIER')
def variable(parsed):
    var = Function.all_variables.get(parsed[0].value)
    if var is None:
        raise errors.VariableDoesNotExistsError(parsed[0])

    if var.expression is None:
        raise errors.VariableIsNotInitializedError(parsed[0])

    return var


@parser_generator.production('number : DECIMAL | HEX')
def number(parsed):
    if parsed[0].name == 'DECIMAL':
        parsed[0].value = int(parsed[0].value)
    elif parsed[0].name == 'HEX':
        parsed[0].value = int(parsed[0].value, base=16)
    return parsed[0].value


@parser_generator.production('semicolons : ; | semicolons ;')
def semicolons(parsed):
    pass


@parser_generator.error
def error_handler(token):
    raise errors.CodeError(token)
