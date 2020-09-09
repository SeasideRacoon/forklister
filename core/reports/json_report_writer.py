import json

from core import ForkInfo
from core.reports.abstract_report_writer import ReportWriter


class JsonReportWriter(ReportWriter):
    def __init__(self, filepath: str, encoding='utf-8', numbered=False):
        assert filepath
        self.encoding = encoding
        self.filepath = filepath
        self.numbered = numbered
        self._file = None
        self._json_array = []

    def __enter__(self):
        self._file = open(self.filepath, mode='w', encoding=self.encoding)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def add(self, fork_info: ForkInfo, number: int = None):
        if number is not None and self.numbered:
            fork_dict = {'number': number, 'ahead_by': fork_info.ahead_by, 'behind_by': fork_info.behind_by,
                         'stargazers': fork_info.stargazers_count, 'days ago':  fork_info.days_ago, 'url': fork_info.url}
            self._json_array.append(fork_dict)
        else:
            fork_dict = {'ahead_by': fork_info.ahead_by, 'behind_by': fork_info.behind_by,
                         'stargazers': fork_info.stargazers_count, 'days ago':  fork_info.days_ago, 'url': fork_info.url}
            self._json_array.append(fork_dict)

    def finalize(self):
        json_dict = {'forks': self._json_array}
        json.dump(json_dict, self._file)
