"""Module contains classes for all errors that could be raised in my project"""

from rply.errors import LexingError


class CodeError(Exception):

    def __init__(self, err):
        self.err = err
        err_pos = err.getsourcepos()

        if isinstance(self.err, LexingError):
            self.message = ('ERROR: no such reserved lexeme'
                            f'\n[line: {err_pos.lineno} |'
                            f' column: {err_pos.colno}]')
        else:
            self.message = (f'ERROR: ran into <{err.value}> where it was not'
                            f' expected\n[line: {err_pos.lineno} |'
                            f' column: {err_pos.colno}]')
        super().__init__(self.message)


class VariableDoesNotExistsError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: Variable <{token.value}> does not exists'
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)


class VariableIsNotInitializedError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: You should initialize variable '
                        f'<{token.value}> before usage'
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)


class VariableAlreadyExistsError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: Variable <{token.value}> already exists.'
                        ' Remove second declaration '
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)


class DivisionByZeroError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = ('ERROR: You can\'t divide by zero'
                        f'\n[line: {token_position.lineno}]')
        super().__init__(self.message)


class NoReturnStatementInFunctionError(Exception):

    def __init__(self, function_name):
        self.message = (f'ERROR: Function <{function_name}> should return '
                        'something. Add return statement.')
        super().__init__(self.message)


class FunctionDoesNotExistsError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: No such function <{token.value}>'
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)


class FunctionAlreadyExistsError(Exception):

    def __init__(self, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: Function <{token.value}> already exists,\n'
                        'remove repetition'
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)


class MainFunctionDoesNotExistsError(Exception):

    def __init__(self):
        self.message = ('ERROR: No entry point in program. '
                        'Create main function')
        super().__init__(self.message)


class ArgumentsDidNotMatchError(Exception):

    def __init__(self, function_name, token):
        token_position = token.getsourcepos()
        self.message = (f'ERROR: Arguments, declared in function'
                        f' <{function_name}> did not match'
                        ' to the previous declaration'
                        f'\n[line: {token_position.lineno} |'
                        f' column: {token_position.colno}]')
        super().__init__(self.message)
