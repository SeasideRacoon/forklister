import abc
from typing import Collection, Optional

from github.Repository import Repository

from core import ForkInfo


class ReportWriter(metaclass=abc.ABCMeta):
    def begin(self, origin: Optional[Repository] = None):
        """
        Add header to report
        """
        pass

    def finalize(self):
        """
        Add footer to report. Writer must know it's footer
        """
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    def add(self, fork_info: ForkInfo, number: int = None):
        """
        Add one fork information to report

        :param fork_info:
        :param number: in case you need to add fork number
        :return:
        """
        pass

    def create_from_list(self, forks: Collection[ForkInfo], origin: Repository = None):
        self.begin(origin)
        for n, fork in enumerate(forks):
            self.add(fork_info=fork, number=n)
        self.finalize()
