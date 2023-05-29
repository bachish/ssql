class Connection:
    def __init__(self):
        self.mapper = None

    def check(self, query, types) -> str | None:
        # todo throw some "not implement" or do this class abstract?
        return None

    def check_without_types(self, query) -> str | None:
        return None
