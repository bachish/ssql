class SsqlTypeError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class SsqlDBError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        # idx + 1, fullname
