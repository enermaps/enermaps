import re
from os import environ as env

from github import Github, Repository

wiki_remote_url = env['GITHUB_WIKI_REMOTE_URL']


def __extract_repo_full_name_from_repo_url(repo_url: str) -> str:
    """
    :param repo_url: a string of the format: ``https://<personal_access_token>@github.com/<owner>/<repo name>.git``
    :return: the value of ``<owner>/<repo name>``
    """
    return re.findall(r'github.com\/(.*)\.git', repo_url)[0]


def __extract_personal_access_token_from_repo_url(repo_url: str) -> str:
    """
    :param repo_url: a string of the format: ``https://<personal_access_token>@github.com/<owner>/<repo name>.git``
    :return: the value of ``<personal_access_token>``
    """
    return re.findall(r'https:\/\/(.*)@', repo_url)[0]


def __git_hub_instance() -> Github:
    """
    :return: The ``Github`` instance by reading the ``$GITHUB_WIKI_REMOTE_URL`` environment variable
    """
    token = __extract_personal_access_token_from_repo_url(repo_url=wiki_remote_url)
    return Github(login_or_token=token)


def __get_wiki_repo(gh: Github) -> Repository:
    """
    :param gh: the used ``Github`` instance
    :return: a ``Repository`` object encapsulating the data about the repo under ``$GITHUB_WIKI_REMOTE_URL``
    """
    wiki_full_name = __extract_repo_full_name_from_repo_url(repo_url=wiki_remote_url)
    return gh.get_repo(full_name_or_id=wiki_full_name)


def __get_wiki_users(wiki_repo: Repository) -> list:
    collaborators = wiki_repo.get_collaborators(affiliation='all')
    contributors = wiki_repo.get_contributors()
    return [*collaborators, *contributors]


def get_authenticated_user_string() -> str:
    """
    :return: a string in which the GitHub usernames of the users who should have editor rights are listed
    """
    gh: Github = __git_hub_instance()
    wiki_repo = __get_wiki_repo(gh)
    wiki_users: list = __get_wiki_users(wiki_repo)
    usernames = sorted(set(user.login for user in wiki_users), key=lambda username: username.lower())
    return ','.join(usernames)
