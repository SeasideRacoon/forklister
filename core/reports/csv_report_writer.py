from csv import writer
from typing import Optional

from github.Repository import Repository

from core import ForkInfo
from core.reports.abstract_report_writer import ReportWriter


class CsvReportWriter(ReportWriter):
    def __init__(self, filepath: str, encoding='utf-8', numbered=False):
        assert filepath
        self.encoding = encoding
        self.filepath = filepath
        self.numbered = numbered
        self._file = None
        self._writer = None

    def __enter__(self):
        self._file = open(self.filepath, mode='w', encoding=self.encoding, newline='')
        self._writer = writer(self._file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def begin(self, origin: Optional[Repository] = None):
        if self.numbered:
            self._writer.writerow(['number', 'ahead by', 'behind by', 'stargazers', 'days ago', 'url'])
        else:
            self._writer.writerow(['ahead by', 'behind by', 'stargazers',  'days ago', 'url'])

    def add(self, fork_info: ForkInfo, number: int = None):
        if number is not None and self.numbered:
            self._writer.writerow([number, fork_info.ahead_by, fork_info.behind_by, fork_info.stargazers_count,
                                   fork_info.days_ago, fork_info.url])
        else:
            self._writer.writerow([fork_info.ahead_by, fork_info.behind_by, fork_info.stargazers_count,
                                   fork_info.days_ago, fork_info.url])
