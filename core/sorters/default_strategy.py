from typing import List

from core import ForkInfo
from core.sorters.sorting_strategy import SortingStrategy


class DefaultSortingStrategy(SortingStrategy):
    """
    Sorts by default ForkInfo comparison rules. Ahead-only forks go first no matter if strategy is reversed
    """
    def sort(self, forks: List[ForkInfo]) -> List[ForkInfo]:
        to_sort = self.filtered(forks)

        ahead_only = []
        ahead_and_behind = []
        behind_or_equal = []

        for fork in to_sort:
            if fork.ahead_by == 0:
                behind_or_equal.append(fork)
            elif fork.behind_by == 0:
                ahead_only.append(fork)
            else:
                ahead_and_behind.append(fork)

        for part in [ahead_only, ahead_and_behind, behind_or_equal]:
            part.sort(reverse=self.reverse)

        return ahead_only + ahead_and_behind + behind_or_equal
