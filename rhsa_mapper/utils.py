import re
from typing import Generator

import requests
from bs4 import BeautifulSoup

REPOSITORY_TO_CPE_URL = 'https://www.redhat.com/security/data/metrics/repository-to-cpe.json'


def fetch_repository_to_cpe_mapping() -> dict:
    """Fetch the Red Hat repository to CPE mapping"""
    res = requests.get(REPOSITORY_TO_CPE_URL)
    res.raise_for_status()
    return res.json().get('data', {})


def group_by_repository() -> dict:
    """Return dictionary of repositories to their linked CPEs"""
    return {repository: cpes.get('cpes', []) for repository, cpes in fetch_repository_to_cpe_mapping().items()}


def group_by_cpe() -> dict:
    """Return dictionary of CPEs mapped to the repositories they appear in"""
    cpe_dict = {}
    for repository, cpes in fetch_repository_to_cpe_mapping().items():
        for cpe in cpes.get('cpes', []):
            cpe_dict.setdefault(cpe, set()).add(repository)
    return {cpe: sorted(repositories) for cpe, repositories in cpe_dict.items()}


def query_repositories_by_cpes(cpes: list) -> list:
    """Return list of repositories that contain the CPEs in cpes"""
    return sorted({repositories for cpe in cpes for repositories in group_by_cpe().get(cpe, [])})


def query_cpes_by_repositories(repositories: list) -> list:
    """Return CPEs for the given repositories"""
    return sorted({cpes for repo in repositories for cpes in group_by_repository().get(repo, [])})


def generate_advisory_dict(advisory_details: tuple) -> Generator:
    """
    Generates a dictionary mapping advisories to their CPEs and repositories.

    :param advisory_details: Generator of tuples containing the advisory ID and CPEs for that advisory
    :return: Generator of dictionaries containing advisory -> CPE/Repo mappings
    """
    for advisory_id, cpes in advisory_details:
        repos = query_repositories_by_cpes(cpes)
        yield {advisory_id: {'num_of_cpes': len(cpes), 'list_of_cpes': cpes, 'num_of_repos': len(repos),
                             'list_of_repos': repos}}


def generate_output(advisory_id: str, details: dict) -> str:
    """
    Generates the output for the given advisory_id and list of CPEs

    :param advisory_id: Advisory ID from the OVAL XML file
    :param details: Dictionary containing a list of CPEs and repositories for the advisory_id
    :return: Output to display on the CLI for the advisory
    """
    cpe_count = details.get('num_of_cpes', 0)
    repo_count = details.get('num_of_repos', 0)
    cpe_string = '\n'.join([f"    - {cpe}" for cpe in details.get('list_of_cpes', [])])
    repo_string = '\n'.join([f"    - {cpe}" for cpe in details.get('list_of_repos', [])])
    output = f'Advisory {advisory_id}:\n'
    output += f'  Contains {cpe_count} {"CPEs" if cpe_count > 1 else "CPE"}...\n{cpe_string}\n'
    output += (f'  Applies to {repo_count} '
               f'{"repositories" if repo_count > 1 else "repository"}...\n{repo_string}\n')
    return output


def parse_xml(oval_file: str, advisory_id: str = None) -> Generator:
    """
    Attempt to open and parse the OVAL file for the given advisory_id.  Returns list of CPEs found in the advisory.

    :param oval_file: Path to the OVAL XML file.
    :param advisory_id: Advisory ID to search for in the advisory (optional)
    :return: generator of tuples containing the advisory ID and CPEs for that advisory.
    """
    with open(oval_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        if advisory_id:
            advisory_title = soup.find('title', text=re.compile(advisory_id))
            if advisory_title:
                yield advisory_id, sorted({cpe.get_text() for cpe in advisory_title.parent.find_all('cpe')})
        else:
            for definition in soup.find_all('definition'):
                advisory_id_search = re.search(r'(RH\w+-\d+:\d+)', definition.metadata.title.get_text(strip=True))
                if advisory_id_search:
                    yield advisory_id_search.group(1), sorted({cpe.get_text() for cpe in definition.find_all('cpe')})
