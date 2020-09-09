import json
import os
from datetime import datetime
from typing import Optional

from github.Repository import Repository
from jinja2 import Template, FileSystemLoader, Environment

from core import ReportWriter, ForkInfo


class HtmlReport:
    def __init__(self, date: datetime):
        self.date = date
        self.forks = []
        self.origin = None
        self.forks_json = {}


class HtmlReportWriter(ReportWriter):
    def __init__(self, filename: str):
        self.filename = filename
        self.template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        self.template_name = 'j2template.html'
        self._read_template()  # type: Template
        self.report = HtmlReport(datetime.now())
        self._json_array = []

    def __enter__(self):
        self.fh = open(self.filename, mode='w', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fh.close()

    def begin(self, origin: Optional[Repository] = None):
        self.report.origin = origin

    def add(self, fork_info: ForkInfo, number: int = None):
        self.report.forks.append(fork_info)
        fork_dict = {'ahead_by': fork_info.ahead_by, 'behind_by': fork_info.behind_by, 'days_ago': fork_info.days_ago,
                     'stargazers': fork_info.stargazers_count, 'url': fork_info.url}
        self._json_array.append(fork_dict)

    def finalize(self):
        self.report.forks_json = json.dumps({'forks': self._json_array})
        report = self._template.render(data=self.report)
        self.fh.write(report)

    def _read_template(self):
        template_loader = FileSystemLoader(searchpath=self.template_path)
        template_env = Environment(loader=template_loader, autoescape=True)
        self._template = template_env.get_template(self.template_name)
