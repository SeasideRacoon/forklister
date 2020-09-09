import pytest

from core import ForkInfo
from core.sorters.default_strategy import DefaultSortingStrategy
from .fixtures import forks_list, diff_equal


@pytest.mark.parametrize(
    ['reverse', 'first', 'last'],
    [
        (False,
         ForkInfo('', days_ago=0, ahead_by=11, behind_by=0, stargazers_count=0),  # ahead-only goes first
         ForkInfo('', days_ago=0, ahead_by=10, behind_by=10, stargazers_count=0)),

        (True,
         ForkInfo('', days_ago=0, ahead_by=11, behind_by=0, stargazers_count=0),  # ahead-only goes first
         ForkInfo('', days_ago=0, ahead_by=10, behind_by=10, stargazers_count=0))
    ]
)
def test_default_strategy(forks_list, reverse, first, last):
    strategy = DefaultSortingStrategy(reverse=reverse)
    sorted_forks = strategy.sort(forks_list)

    assert diff_equal(first, sorted_forks[0])
    assert diff_equal(last, sorted_forks[-1])
