import logging
import re
from os import environ as env


def module_logger(mod_name: str):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


# Required environment variables and their assertion error messages
assertions = [
    ('GITHUB_CLIENT_ID', 'The GitHub Client ID of the OAuth application must be specified.'),
    ('GITHUB_CLIENT_SECRET', 'The GitHub Client Secret of the OAuth application must be specified.'),
    ('GITHUB_WIKI_REMOTE_URL',
     'The URL for the remote repository for syncing must be specified along with a personal access token.'),
    ('GITHUB_WIKI_REMOTE_BRANCH', 'The used branch of the remote repository for syncing must be specified.'),
]

# Fail hard with a meaningful message in the case of missing env vars
for env_var, message in assertions:
    assert len(env.get(env_var, '')), f'{env_var} is missing from the environment variables. {message}'

# Fail hard if the remote URL is not a valid GitHub URL and it has no valid personal access token
assert len(re.findall(r'https:\/\/(.*)@', env['GITHUB_WIKI_REMOTE_URL'])), \
    'GITHUB_WIKI_REMOTE_URL must contain a personal access token to access the repo. ' \
    'It should match the pattern "https://<GitHub Personal Access Token>@github.com/<owner>/<repo>/.git".'
