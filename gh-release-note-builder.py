#!/usr/bin/python
# coding: utf-8 -*-
#
#
# Copyright 2020 TiTom73
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http: //www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import logging
import pprint
import requests
import sys

# CONSTANTS

# API URI to use to get Milestone information.
GH_API_MILESTONE = "https://api.github.com/search/issues?q=milestone:{}+type:pr+repo:{}"
# Pull Request entry line format
PR_ENTRY = "{} (#{})"
# Release Note format for single entry
RN_ENTRY = "- {}"
# Release Note format for authors.
RN_AUTHOR = "@{}"


def parse_cli():
    """
    Generate CLI options manager

    Returns
    -------
    dict
        dictionary with all options configured by user.
    """
    # Argaparser to load information using CLI
    parser = argparse.ArgumentParser(
        description="Cloudvision Authentication stress script")
    parser.add_argument('-r', '--repository',
                        help='GH Repository like org/repo', type=str,
                        default='aristanetworks/ansible-avd')
    parser.add_argument('-m', '--milestone',
                        help='Milestone', type=str)
    parser.add_argument('-v', '--verbosity',
                        help='Verbose level (debug / info / warning / error / critical)',
                        type=str, default='info')
    options = parser.parse_args()

    return options


def gh_get_milestone_content(repository, milestone):
    """
    Get milestone JSON information from a given repository and milestone.

    Parameters
    ----------
    repository : string
        Repository name using user/repository
    milestone : string
        Milestone existing on the given repository

    Returns
    -------
    dict
        JSON provided by GH API
    """
    url = GH_API_MILESTONE.format(milestone, repository)
    logging.debug("Github API url is: %s", str(url))
    gh_result = requests.get(url)
    if gh_result.status_code == 200:
        return gh_result.json()
    return None


def is_labelled(pr, searched_label):
    """
    Test if given PR has searched_label configured.

    Parameters
    ----------
    pr : dict
        PR from GH JSON dataset
    searched_label : string
        label to look for on the given PR

    Returns
    -------
    boolean
        True if label is configured, False if not
    """
    for label in pr['labels']:
        if label['name'] == searched_label:
            return True
    return False


def parse_pr(milestone_prs, label):
    """
    Read milestone JSON and get PR information.

    Parameters
    ----------
    milestone_prs : dict
        JSON data from GH API
    label : string
        Label PR must have to be extracted.

    Returns
    -------
    list
        List of PRs with correct label.
    """
    list_pr = list()
    for pr in milestone_prs:
        if is_labelled(pr, searched_label=label):
            logging.debug('* Found one PR: %s', pr['title'])
            pr_summary = PR_ENTRY.format(pr['title'], str(pr['number']))
            list_pr.append(pr_summary)
    return list_pr


def get_contributors(milestone_prs):
    """
    Extract list of PR contributors for milestone.

    Parameters
    ----------
    milestone_prs : list
        List or PRs attached to a milestone like pr[items]

    Returns
    -------
    list
        List of PR contributors.
    """
    author = list()
    for pr in milestone_prs:
        author.append(pr['user']['login'])
    return list(dict.fromkeys(author))


if __name__ == '__main__':
    """
    Main section.
    """

    pp = pprint.PrettyPrinter(indent=4)
    cli = parse_cli()

    # Logging configuration
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    LOGLEVEL = LEVELS.get(cli.verbosity, logging.NOTSET)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)-8s - func: %(funcName)-12s - %(message)s',
        level=LOGLEVEL,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.debug("Collecting information for milestone %s in repo %s", str(cli.milestone), str(cli.repository))

    milestone_content = gh_get_milestone_content(repository=cli.repository, milestone=cli.milestone)
    # logging.debug("%s", str(pp.pprint(milestone_content)))
    print("\n# Release Notes for {}".format(cli.milestone))
    print("\n## Fixed issues\n")
    for issue in parse_pr(milestone_prs=milestone_content['items'], label='type: bug'):
        print(RN_ENTRY.format(issue))
    print("\n## Enhancements\n")
    for issue in parse_pr(milestone_prs=milestone_content['items'], label='type: enhancement'):
        print(RN_ENTRY.format(issue))
    for issue in parse_pr(milestone_prs=milestone_content['items'], label='type: simple enhancement'):
        print(RN_ENTRY.format(issue))
    print("\n## Documentation updates\n")
    for issue in parse_pr(milestone_prs=milestone_content['items'], label='type: documentation'):
        print(RN_ENTRY.format(issue))
    print("\n## Contributors\n")
    for author in get_contributors(milestone_prs=milestone_content['items']):
        print(RN_AUTHOR.format(author))
    sys.exit(0)
