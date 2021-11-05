from os import environ as env
from pathlib import Path
from subprocess import run, Popen

wiki_data_dir = Path('/root/wiki-data')
wiki_remote_url = env['GITHUB_WIKI_REMOTE_URL']
wiki_remote_branch = env['GITHUB_WIKI_REMOTE_BRANCH']

if __name__ == '__main__':
    # If the wiki folder has not been cloned yet, then clone it
    if not wiki_data_dir.exists():
        run(['git', 'clone', '--branch', wiki_remote_branch, wiki_remote_url, str(wiki_data_dir)])

    Popen(['python3', '/root/docker-run/scheduled_jobs.py'], close_fds=True)

    # Start gollum
    run(['/usr/local/bin/gollum', str(wiki_data_dir),
         '--config', '/root/gollum-data/config.rb',
         '--port', f'{env.get("PORT", "80")}',
         '--ref', wiki_remote_branch])
