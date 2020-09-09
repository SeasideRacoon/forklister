from collections import namedtuple
from functools import wraps


def check_for_fork(method):
    @wraps(method)
    def wrapper(instance, argument):
        if not isinstance(argument, ForkInfo):
            raise TypeError('can compare ForkInfo only with another ForkInfo instance')
        return method(instance, argument)

    return wrapper


RepoBrief = namedtuple('Repo', ['owner', 'name', 'fullname'])


class ForkInfo:
    def __init__(self, url: str, days_ago: int, stargazers_count: int, ahead_by: int = 0, behind_by: int = 0):
        self.url = url
        self.days_ago = days_ago
        self.stargazers_count = stargazers_count
        self.ahead_by = ahead_by
        self.behind_by = behind_by

    @property
    def commits_diff(self) -> int:
        return self.ahead_by - self.behind_by

    @property
    def deviation_rate(self) -> int:
        return self.ahead_by + self.behind_by

    @check_for_fork
    def __lt__(self, other: 'ForkInfo') -> bool:
        return self.commits_diff < other.commits_diff

    @check_for_fork
    def __gt__(self, other: 'ForkInfo'):
        return self.commits_diff > other.commits_diff

    @check_for_fork
    def __ge__(self, other: 'ForkInfo'):
        return self.commits_diff >= other.commits_diff

    @check_for_fork
    def __le__(self, other: 'ForkInfo'):
        return self.commits_diff <= other.commits_diff

    def __str__(self):
        return f'ahead: {self.ahead_by}, behind: {self.behind_by}, stars: {self.stargazers_count}, url: {self.url}'

    def __repr__(self):
        return str(self)
