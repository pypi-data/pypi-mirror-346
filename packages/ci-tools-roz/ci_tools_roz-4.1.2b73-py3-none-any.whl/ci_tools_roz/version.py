#!/usr/bin/env python3
import os
import sys

import logging
from git import Repo

log = logging.getLogger(os.path.basename(__file__))
log.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.INFO)

log.addHandler(ch)


def git_details(path=None):
    '''
    :param path: Optional relative directory path for analysis
    :return: Tuple(commit_count, short_hash)
    '''
    _, _, count, short_hash = git_details_v2(path)
    return count, short_hash


def git_details_v2(path=None):
    '''
    :param path: Optional relative directory path for analysis
    :return: Tuple(is_dirty, githash, commit_count, short_hash)
    '''
    # An exception here should end the process
    repo = Repo(search_parent_directories=True)
    all_commits = list(repo.iter_commits(paths=path))
    if not all_commits:
        return True, '0', 0, '0'  # Maybe first time build before git commited

    count = len(all_commits)

    githash = all_commits[0].hexsha
    short_hash = githash[0:8]

    return repo.is_dirty(), githash,  f'{count:06}', short_hash


def get_jenkins_pipeline():
    '''
    JOB_NAME is a Jenkins environment variable of the form:
    <project>/<jenkins_pipeline>/<branch_name>
    '''

    job_name = os.environ.get('JOB_NAME', 'local')

    try:
        pipe = job_name.split('/')[1]
        return pipe if pipe in ('develop', 'release') else 'feature'
    except IndexError:
        log.warning("JOB_NAME is not defined as a 'develop' or 'release' pipeline. Treating as a feature pipeline")
        return 'feature'


def get_package_version(semver, path=None):
    '''
    :param semver: A semantic version for the package
    :param path: Optional relative directory path for analysis
    :return: The package semantic version, depending on the Jenkins pipeline it was called from
    '''

    pipe = get_jenkins_pipeline()

    # release: <semver>
    # develop: <semver>b<change_count>+<git_hash>
    # feature: <semver>a<change_count>+<git_hash>

    if pipe == 'release':
        return semver

    ab = {'d': 'b', 'f': 'a'}[pipe[0]]

    count, githash = git_details(path=path)
    return f'{semver}{ab}{count}+{githash}'


def print_jenkins_pipeline():
    '''
    Prints the current Jenkins pipeline to stdout
    Used by CI scripts to determine the current pipeline
    '''

    print(get_jenkins_pipeline())


# This is to allow ci_tools to call this without having to already be installed
if __name__ == '__main__':
    print_jenkins_pipeline()
