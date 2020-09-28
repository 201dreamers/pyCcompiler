class CodeError(Exception):

    def __init__(self, token):
        self.token = token
        self.message = (f"ERROR: <'{token.gettokentype()}': {token.value}> "
                        f"on line {token.getsourcepos().lineno}, "
                        f"column {token.getsourcepos().colno}")
        super().__init__(self.message)
