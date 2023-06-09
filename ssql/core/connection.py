from typing import List, Optional

from mypy.types import ProperType


class Connection:
    def __init__(self):
        self.mapper = None

    def check(
        self, query: str, types: List[Optional[ProperType]]
    ) -> Optional[str]:
        return None

    def check_without_types(self, query: str) -> Optional[str]:
        return None
