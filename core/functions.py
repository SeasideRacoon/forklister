import os
import sys
from argparse import Namespace
from logging import Formatter, Logger, StreamHandler
from logging.handlers import RotatingFileHandler
from typing import List, Collection

from github import Github

from core import CsvReportWriter, JsonReportWriter, NdjsonReportWriter, ReportWriter, AddressParsingError, Client
from core.fork_info import RepoBrief, ForkInfo
from core.reports.html_report_writer import HtmlReportWriter
from core.sorters import SortingStrategy, DefaultSortingStrategy, SortByField


def sort_forks(forklist: List[ForkInfo], args: Namespace) -> Collection[ForkInfo]:
    strategy = get_sorting_strategy(args)
    return strategy.sort(forklist)


def get_sorting_strategy(args: Namespace) -> SortingStrategy:
    """
    Args:
        args (Namespace): command line arguments of application
    """
    fields_mapping = {
        'ahead': 'ahead_by',
        'behind': 'behind_by',
        'stars': 'stargazers_count',
        'deviation': 'deviation_rate'
    }

    reverse = args.sort_order == 'desc'
    if args.sort_by == 'default':
        return DefaultSortingStrategy(reverse=reverse)
    fork_info_field = fields_mapping.get(args.sort_by)
    if fork_info_field:
        return SortByField(fork_info_field, reverse=reverse)


def create_logger() -> Logger:
    logger = Logger('')
    light_fmt = Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    full_fmt = Formatter('%(asctime)s - [%(levelname)s] - [%(filename)s:%(lineno)s] - %(message)s')

    rf = RotatingFileHandler('app.log', maxBytes=10 * (1024 ** 2), encoding='utf-8')
    # rf.setLevel(logging.WARNING)
    rf.setFormatter(full_fmt)

    stdout = StreamHandler(sys.stdout)
    stdout.setFormatter(light_fmt)

    for handler in [rf, stdout]:
        logger.addHandler(handler)

    return logger


def get_github_client(args: Namespace) -> Client:
    api_key = args.token or os.getenv(args.token_var, default=None)
    return Client(api_key)


def get_report_writer(args: Namespace, brief: RepoBrief) -> ReportWriter:
    type_mapping = {
        'csv': CsvReportWriter,
        'json': JsonReportWriter,
        'ndjson': NdjsonReportWriter,
        'html': HtmlReportWriter
    }

    filename = args.output or generate_report_name(brief, args.format)
    if args.format not in type_mapping:
        raise NotImplementedError(f'format not supported: {args.format}')
    return type_mapping[args.format](filename)


def generate_report_name(brief: RepoBrief, fmt: str) -> str:
    return f'{brief.owner}_{brief.name}.{fmt}'


def parse_repo_name(value: str) -> RepoBrief:
    for s in ['https://', 'http://']:  # full addr
        if value.startswith(s):
            value = value.replace(s, '')
    if value.startswith('github.com'):  # github.com/owner/name
        value = value.replace('github.com/', '')
    if value.count('/') == 1:  # owner/name
        spl = value.split('/')
        return RepoBrief(owner=spl[0], name=spl[1], fullname=value)
    raise AddressParsingError()
