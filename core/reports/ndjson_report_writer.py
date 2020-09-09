import json
import os

from core import ForkInfo
from core.reports.abstract_report_writer import ReportWriter


class NdjsonReportWriter(ReportWriter):
    def __init__(self, filepath: str, encoding='utf-8', numbered=False):
        assert filepath
        self.encoding = encoding
        self.filepath = filepath
        self.numbered = numbered
        self._empty = True
        self._file = None
        self._writer = None

    def __enter__(self):
        self._file = open(self.filepath, mode='w', encoding=self.encoding, newline='')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def add(self, fork_info: ForkInfo, number: int = None):
        if not self._empty:
            self._file.write(os.linesep)
        row = self.make_row(fork_info, number)
        self._file.write(row)
        self._empty = False

    def make_row(self, fork_info: ForkInfo, number: int = None):
        if number is not None and self.numbered:
            return json.dumps({'number': number, 'ahead_by': fork_info.ahead_by, 'behind_by': fork_info.behind_by,
                               'stargazers': fork_info.stargazers_count, 'days ago':  fork_info.days_ago,
                               'url': fork_info.url})
        return json.dumps({'ahead_by': fork_info.ahead_by, 'behind_by': fork_info.behind_by,
                           'stargazers': fork_info.stargazers_count, 'days ago':  fork_info.days_ago,
                           'url': fork_info.url})
