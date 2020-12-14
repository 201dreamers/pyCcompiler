"""Module contains ParseWrapper for ParserGenerator from 'rply'"""

from rply import ParserGenerator
from rply.token import Token

from compiler import lexer_wrapper
from compiler.nodes import (DoWhileLoop, Function, Return, UnaryExpression,
                            BinaryExpression, TernaryExpression,
                            Program, FunctionCall, VariableInitialization,
                            Variable)
from compiler import errors


token_names = [token_name for token_name, _ in lexer_wrapper.tokens]
precedence = (
    ('left', ['/=', '=']),
    ('left', ['COLON']),
    ('left', ['?']),
    ('left', ['&&']),
    ('left', ['==']),
    ('left', ['*', '/']),
    ('left', ['-']),
    ('left', ['('])
)
parser_generator = ParserGenerator(token_names, precedence=precedence)


@parser_generator.production('program : contents')
def program(parsed):
    if 'main' not in Program.get_functions().keys():
        raise errors.MainFunctionDoesNotExistsError()
    return Program(contents=parsed[0])


@parser_generator.production('contents : function')
@parser_generator.production('contents : contents function')
def contents(parsed):
    _contents = []
    if (_len_of_parsed := len(parsed)) == 1:
        _contents.append(parsed[0])
    elif _len_of_parsed == 2:
        _contents.extend(parsed[0])
        _contents.append(parsed[1])
    return _contents


@parser_generator.production(
    'function : function_initializer ( arguments ) { body }')
@parser_generator.production(
    'function : function_initializer ( arguments ) semicolons')
def function(parsed):
    _function, prev_declared_arguments = parsed[0]
    if prev_declared_arguments is not None:
        declared_arguments = tuple(
            [argument.type for argument in parsed[2]])
        if declared_arguments != prev_declared_arguments:
            raise errors.ArgumentsDidNotMatchError(
                function_name=_function.name,
                token=parsed[1]
            )
            pass
    _function.arguments = parsed[2]
    if (len_of_parsed := len(parsed)) == 7:
        has_return_statement = False
        for line_of_code in parsed[5]:
            if isinstance(line_of_code, Return):
                has_return_statement = True
                break

        if not has_return_statement:
            raise errors.NoReturnStatementInFunctionError(_function.name)
        _function.body = parsed[5]
    elif len_of_parsed == 5:
        return
    return _function


@parser_generator.production('function_initializer : TYPE IDENTIFIER')
def function_initializer(parsed):
    prev_declaration = Program.get_function(parsed[1].value)
    declared_arguments = None
    if prev_declaration is not None:
        if prev_declaration.body != []:
            raise errors.FunctionAlreadyExistsError(parsed[1])
        declared_arguments = tuple(
            [argument.type for argument in prev_declaration.arguments])
    _function = Function(
        name=parsed[1].value,
        type_=parsed[0].value,
    )
    return _function, declared_arguments


@parser_generator.production('arguments : ')
@parser_generator.production('arguments : TYPE IDENTIFIER')
@parser_generator.production('arguments : arguments , TYPE IDENTIFIER')
def arguments(parsed):
    _arguments = []
    if (len_of_parsed := len(parsed)) in (2, 3):
        argument = Variable(type_=parsed[0].value, name=parsed[1].value,
                            is_function_argument=True)
        if len_of_parsed == 3:
            _arguments.extend(parsed[0])
        _arguments.append(argument)
    return _arguments


@parser_generator.production('body : instruction semicolons')
@parser_generator.production('body : body instruction semicolons')
def body(parsed):
    _body = []
    if (len_of_parsed := len(parsed)) == 2:
        _body.append(parsed[0])
    elif len_of_parsed == 3:
        _body.extend(parsed[0])
        _body.append(parsed[1])
    return _body


@parser_generator.production('instruction : RETURN expression')
@parser_generator.production('instruction : IDENTIFIER = expression')
@parser_generator.production('instruction : IDENTIFIER /= expression')
@parser_generator.production('instruction : TYPE IDENTIFIER')
@parser_generator.production('instruction : TYPE IDENTIFIER = expression')
@parser_generator.production('instruction : DO { body } WHILE ( expression )')
def instruction(parsed):
    current_function = Program.get_current_function()

    if parsed[0].name == 'TYPE':
        if current_function.variable_exists(parsed[1].value):
            raise errors.VariableAlreadyExistsError(parsed[1])

        var_assignment = VariableInitialization(type_=parsed[0].value,
                                                name=parsed[1].value)
        if len(parsed) == 4:
            var_assignment.expression = parsed[3]
            return var_assignment
        return

    elif parsed[0].name == 'IDENTIFIER':
        var_assignment = VariableInitialization(name=parsed[0].value)
        if parsed[1].name == '=':
            var_assignment.expression = parsed[2]
        elif parsed[1].name == '/=':
            var = variable([parsed[0]])
            var_assignment.expression = BinaryExpression(
                left_operand=var,
                right_operand=parsed[2],
                operator='/'
            )
        return var_assignment

    elif parsed[0].name == 'RETURN':
        return Return(argument=parsed[1])

    elif parsed[0].name == 'DO':
        return DoWhileLoop(body=parsed[2], expression=parsed[6])


@parser_generator.production('expression : number | variable | - expression')
@parser_generator.production('expression : function_call')
@parser_generator.production('expression : expression == expression')
@parser_generator.production('expression : expression && expression')
@parser_generator.production('expression : expression * expression')
@parser_generator.production('expression : expression / expression')
@parser_generator.production(
    'expression : expression ? expression COLON expression')
@parser_generator.production('expression : ( expression )')
def expression(parsed):
    if (_len_of_parsed := len(parsed)) == 2:
        return UnaryExpression(parsed[1])
    elif _len_of_parsed == 3:
        if isinstance(parsed[0], Token) and parsed[0].value == '(':
            return expression([parsed[1]])
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


@parser_generator.production('function_call : IDENTIFIER ( passed_arguments )')
def function_call(parsed):
    func = Program.get_function(parsed[0].value)
    if func is None:
        raise errors.FunctionDoesNotExistsError(parsed[0])

    return FunctionCall(function_name=func.name, arguments=parsed[2])


@parser_generator.production('passed_arguments : ')
@parser_generator.production('passed_arguments : expression')
@parser_generator.production(
    'passed_arguments : passed_arguments , expression')
def passed_arguments(parsed):
    _passed_arguments = []
    if (len_of_parsed := len(parsed)) == 1:
        _passed_arguments.append(parsed[0])
    elif len_of_parsed == 2:
        _passed_arguments.extend(parsed[0])
        _passed_arguments.append(parsed[1])
    return _passed_arguments


@parser_generator.production('variable : IDENTIFIER')
def variable(parsed):
    var = Program.get_current_function().get_variable(parsed[0].value)
    if var is None:
        raise errors.VariableDoesNotExistsError(parsed[0])

    if not var.is_initialized and not var.is_function_argument:
        raise errors.VariableIsNotInitializedError(parsed[0])

    return var


@parser_generator.production('number : DECIMAL | HEX')
def number(parsed):
    if parsed[0].name == 'DECIMAL':
        parsed[0].value = int(float(parsed[0].value))
    elif parsed[0].name == 'HEX':
        parsed[0].value = int(parsed[0].value, base=16)
    return parsed[0].value


@parser_generator.production('semicolons : ; | semicolons ;')
def semicolons(parsed):
    pass


@parser_generator.error
def error_handler(token):
    raise errors.CodeError(token)
