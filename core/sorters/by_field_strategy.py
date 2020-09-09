from typing import List

from core import ForkInfo
from core.sorters.sorting_strategy import SortingStrategy


class SortByField(SortingStrategy):
    def __init__(self, field: str, *, reverse=False, include_without_ahead=False):
        super().__init__(reverse=reverse, include_without_ahead=include_without_ahead)
        self.field = field

    def sort(self, forks: List[ForkInfo]) -> List[ForkInfo]:
        return sorted(self.filtered(forks), key=lambda fi: getattr(fi, self.field), reverse=self.reverse)
