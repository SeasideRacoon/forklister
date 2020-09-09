from typing import List

import pytest

from core import ForkInfo


def diff_equal(first: ForkInfo, second: ForkInfo) -> bool:
    return first.ahead_by == second.ahead_by and first.behind_by == second.behind_by


def all_equal(first: ForkInfo, second: ForkInfo) -> bool:
    return all([
        first.ahead_by == second.ahead_by,
        first.behind_by == second.behind_by,
        first.stargazers_count == second.stargazers_count
    ])


@pytest.fixture
def forks_list() -> List[ForkInfo]:
    simple = [
        ForkInfo('', days_ago=0, stargazers_count=i, ahead_by=i, behind_by=i)
        for i in range(11)
    ]

    special = [
        ForkInfo('', days_ago=0, stargazers_count=0, ahead_by=11, behind_by=0),
        ForkInfo('', days_ago=0, stargazers_count=0, ahead_by=0, behind_by=11),
        ForkInfo('', days_ago=0, stargazers_count=11, ahead_by=0, behind_by=0),
    ]

    return simple + special
