from rply.errors import LexingError


class CodeError(Exception):

    def __init__(self, token):
        self.token = token
        token_pos = token.getsourcepos()

        if isinstance(self.token, LexingError):
            self.message = ("ERROR: no such reserved lexem on"
                            f" on line {token_pos.lineno},"
                            f" column {token_pos.colno}")
        else:
            self.message = (f"ERROR: <'{token.gettokentype()}': {token.value}>"
                            f" on line {token_pos.lineno},"
                            f" column {token_pos.colno}")
        super().__init__(self.message)
