from collections import namedtuple

import pytest

from core.functions import get_sorting_strategy
from core.sorters import DefaultSortingStrategy, SortByField

arg = namedtuple('arg', ['sort_by', 'sort_order'])


@pytest.mark.parametrize(
    ['args', 'expected_type', 'expected_reverse'],
    [
        (arg('default', 'asc'), DefaultSortingStrategy, False),
        (arg('default', 'desc'), DefaultSortingStrategy, True)
    ]
)
def test_get_sorting_strategy_default(args, expected_type, expected_reverse):
    actual = get_sorting_strategy(args)
    assert type(actual) == expected_type
    assert actual.reverse == expected_reverse


@pytest.mark.parametrize(
    ['args', 'field_name', 'expected_type', 'expected_reverse'],
    [
        (arg('ahead', 'asc'), 'ahead_by', SortByField, False),
        (arg('behind', 'desc'), 'behind_by', SortByField, True),
        (arg('stars', 'desc'), 'stargazers_count', SortByField, True),
        (arg('deviation', 'desc'), 'deviation_rate', SortByField, True)
    ]
)
def test_get_sorting_strategy_by_field(args, field_name, expected_type, expected_reverse):
    actual = get_sorting_strategy(args)
    assert type(actual) == expected_type
    assert actual.reverse == expected_reverse
    assert actual.field == field_name
