"""Module contains classes for all errors that could be raised in my project"""

from rply.errors import LexingError


class CodeError(Exception):

    def __init__(self, err):
        self.err = err
        err_pos = err.getsourcepos()

        if isinstance(self.err, LexingError):
            self.message = ("ERROR: no such reserved lexem"
                            f" on line {err_pos.lineno},"
                            f" column {err_pos.colno}")
        else:
            self.message = (f"ERROR: ran into <{err.value}> where it wasn't expected"
                            f" on line {err_pos.lineno},"
                            f" column {err_pos.colno}")
        super().__init__(self.message)


class WrongReturnType(Exception):

    def __init__(self, type_, func_name):
        self.message = (f"ERROR: wrong return value. "
                        f"<{type_}> expected in function {func_name}")
        super().__init__(self.message)
