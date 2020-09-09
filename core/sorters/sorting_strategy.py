import abc
from typing import List, Generator, Iterable, Collection

from core import ForkInfo


class SortingStrategy(metaclass=abc.ABCMeta):
    def __init__(self, *, reverse: bool = False, include_without_ahead=False):
        self.reverse = reverse
        self.include_without_ahead = include_without_ahead

    """
    Base class for all sorting strategies
    """

    @abc.abstractmethod
    def sort(self, forks: List[ForkInfo]) -> Collection[ForkInfo]:
        """
        Applies strategy algorithm with or without filtration

        Args:
            forks: list of ForkInfo
        """
        raise NotImplementedError('abstract method')

    @staticmethod
    def no_behinds(forks: List[ForkInfo]) -> Generator[ForkInfo, None, None]:
        """
        Return forks only with ahead commits

        Args:
            forks: collection to filter
        """
        return (fi for fi in forks if fi.ahead_by > 0)

    def filtered(self, forks: List[ForkInfo]) -> Iterable[ForkInfo]:
        """
        Filter collection based by sort arguments

        Args:
            forks: collection to filter
        """
        if self.include_without_ahead:
            return forks
        return self.no_behinds(forks)
