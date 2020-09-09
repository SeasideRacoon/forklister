
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from github.GithubException import GithubException, UnknownObjectException
from github.Repository import Repository

from core import ForkInfo, RateLimitError, Client
from core.functions import create_logger, get_github_client, get_report_writer, parse_repo_name, sort_forks


def parse_html_page(html: str, forks: List[ForkInfo], repo: Repository):
    """
    Extracts fork information from page contents and adds to forks list
    """
    soup = BeautifulSoup(html, 'html.parser')
    comparing = soup.findAll('div', class_='d-flex flex-auto')
    try:
        if 'ahead' in comparing[0].contents[0]:
            fi = ForkInfo(repo.html_url, (abs(datetime.now() - repo.updated_at)).days, repo.stargazers_count)
            for element in comparing[0].contents[0].split('ahead')[0].split():
                if element.isdigit():
                    fi.ahead_by = int(element)
            if 'behind' in comparing[0].contents[0]:
                for element in comparing[0].contents[0].split('ahead')[1].split():
                    if element.isdigit():
                        fi.behind_by = int(element)
            else:
                fi.behind_by = 0
            forks.append(fi)
        log.info('error was handled for %s', repo.html_url)
    except IndexError:
        log.info('html page has no required content : %s', repo.html_url)


def handle_github_exception(forks: List[ForkInfo], repo: Repository):
    """
    If API comparison request wasn't success, we can try to get info from fork page
    """
    try:
        log.info('requesting uri: %s', repo.html_url)
        response = requests.get(repo.html_url)
        response.raise_for_status()
        parse_html_page(response.text, forks, repo)
    except requests.RequestException:
        log.exception('request failed: %s', repo.html_url)


def pagination_correction(forks_count, forks_per_page: int) -> int:
    return forks_count // forks_per_page + 1


def get_forks_info(origin: Repository, client: Client) -> List[ForkInfo]:
    """
    Requests forks and wraps them in 'ForkInfo' objects
    """
    result = []
    forks = origin.get_forks()
    log.info('got list of forks, total %d', forks.totalCount)
    client.count_rate_limit(1)
    try:
        rate_limits_check(client, forks.totalCount + pagination_correction(forks.totalCount, 30))
    except RateLimitError:
        return
    for fork in forks:
        try:
            log.info('comparing fork: %s', fork.full_name)
            comparison = origin.compare(origin.owner.login + ":master", fork.owner.login + ":master")
            fi = ForkInfo(fork.html_url, (abs(datetime.now() - fork.updated_at)).days, fork.stargazers_count, comparison.ahead_by, comparison.behind_by)
            result.append(fi)
        except UnknownObjectException as e:
            log.exception('possibly removed fork or user: %s, %d, message: %s', fork.html_url, e.status,
                          e.data.get('message', ''))
        except GithubException as e:
            message = e.data.get('message', '')
            if e.status == 404 and 'No common ancestor between ' in message:  # that can be handled
                log.error('404 %s', message)
                handle_github_exception(result, fork)
            else:
                log.exception('github error')
    client.count_rate_limit(forks.totalCount + pagination_correction(forks.totalCount, 30))
    return result


def arguments_valid(args: Namespace):
    if not args.repo:
        log.error('repository address can\'t be empty')
        return False
    return True


def rate_limits_check(client, requests_count):
    if client.current_rate_limiting[0] < requests_count:
        log.error('Number of available requests is not enough for the operation: '
                  'client rate limits: %s/%s. Required requests: %s. Try again later.',
                  client.current_rate_limiting[0], client.current_rate_limiting[1], requests_count)
        raise RateLimitError


def main(args: Namespace):
    brief = parse_repo_name(arguments.repo)
    client = get_github_client(arguments)
    log.info('client rate limits: %s/%s', client.rate_limiting[0], client.rate_limiting[1])
    client.rate_limiting_initialization()
    try:
        rate_limits_check(client, 1)
    except RateLimitError:
        return
    try:
        origin = client.get_repo(brief.fullname)
    except GithubException as e:
        log.exception('Repository not found: %s, %d, message: %s', brief.fullname, e.status,
                      e.data.get('message', ''))
        return
    client.count_rate_limit(1)
    log.info('got repository info')
    with get_report_writer(args, brief) as writer:
        try:
            rate_limits_check(client, 1)
        except RateLimitError:
            return
        comparable_forks = get_forks_info(origin, client)
        if comparable_forks is not None:
            sorted_forks = sort_forks(comparable_forks, args)
            writer.create_from_list(sorted_forks, origin)


if __name__ == '__main__':
    log = create_logger()
    argparser = ArgumentParser()
    argparser.add_argument('repo', help='any form: full uri, github.com/{owner}/{repo}, {owner}/{repo}')
    argparser.add_argument('-f', '--format', default='csv', help='csv, json, ndjson, html',
                           choices=['csv', 'json', 'ndjson', 'html'],
                           type=str.lower)
    argparser.add_argument('-sb', '--sort-by', default='default', type=str.lower,
                           help='Sort forks by commits ahead, commits behind, stargazers, deviation or default.'
                                'Deviation is a sum of ahead and behind,'
                                'default sort is when ahead-only forks listed first',
                           choices=['default', 'ahead', 'behind', 'stars', 'deviation'])
    argparser.add_argument('-so', '--sort-order', default='desc',  help='asc or desc', choices=['asc', 'desc'],
                           type=str.lower)
    argparser.add_argument('-o', '--output', required=False, type=str, help='specify output file, otherwise generated')
    argparser.add_argument('-t', '--token', type=str, help='specify Github API token')
    argparser.add_argument('-tv', '--token-var', default='GITHUB_TOKEN',
                           help='specify Github API token environment variable')
    arguments = argparser.parse_args()

    if arguments_valid(arguments):
        try:
            main(arguments)
            log.info('done')
        except NotImplementedError as e:
            log.error('feature not implemented: %s', str(e))
            exit(1)
        except Exception as e:
            log.exception('execution failed', exc_info=e)
            exit(1)
    else:
        exit(1)
