from typing import Any

from core.sorters.by_field_strategy import SortByField
from .fixtures import *


def assert_field_equal(field: str, value: Any, fi: ForkInfo):
    assert getattr(fi, field) == value


@pytest.mark.parametrize(  # range of all possible values: 0-11
    ['field', 'reverse', 'include_noahead', 'first_field_val', 'last_field_val'],
    [
        ('ahead_by', False, False, 1, 11),
        ('ahead_by', True, False, 11, 1),
        ('stargazers_count', False, True, 0, 11)
    ]
)
def test_sort_by_field(forks_list, field, reverse, include_noahead, first_field_val, last_field_val):
    strategy = SortByField(field, reverse=reverse, include_without_ahead=include_noahead)
    result = strategy.sort(forks_list)

    assert_field_equal(field, first_field_val, result[0])
    assert_field_equal(field, last_field_val, result[-1])
