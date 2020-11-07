"""Module contains classes for all errors that could be raised in my project"""

from rply.errors import LexingError

from config import logger


class CodeError(Exception):

    def __init__(self, err):
        self.err = err
        err_pos = err.getsourcepos()

        if isinstance(self.err, LexingError):
            self.message = ("ERROR: no such reserved lexeme"
                            f" [line: {err_pos.lineno} |"
                            f" column: {err_pos.colno}]")
        else:
            self.message = (f"ERROR: ran into <{err.value}> where it was not"
                            f" expected [line: {err_pos.lineno} |"
                            f" column: {err_pos.colno}]")
        super().__init__(self.message)


class VariableDoesNotExistsError(Exception):

    def __init__(self, token):
        _token_position = token.getsourcepos()
        self.message = (f"ERROR: Variable <{token.value}> does not exists"
                        f" [line: {_token_position.lineno} |"
                        f" column: {_token_position.colno}]")
        super().__init__(self.message)


class VariableIsNotInitializedError(Exception):

    def __init__(self, token):
        _token_position = token.getsourcepos()
        self.message = (f"ERROR: You should initialize variable <{token.value}>"
                        f" before usage [line: {_token_position.lineno} |"
                        f" column: {_token_position.colno}]")
        super().__init__(self.message)


class DivisionByZeroError(Exception):

    def __init__(self, token):
        _token_position = token.getsourcepos()
        self.message = (f"ERROR: You can't divide by zero"
                        f" [line: {_token_position.lineno}]")
        super().__init__(self.message)



class WrongReturnType(Exception):

    def __init__(self, type_, func_name):
        self.message = (f"ERROR: wrong return value. "
                        f"<{type_}> expected in function {func_name}")
        super().__init__(self.message)
