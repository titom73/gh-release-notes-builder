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
import jinja2


# CONSTANTS

# API URI to use to get Milestone information.
GH_API_MILESTONE = "https://api.github.com/search/issues?q=milestone:{}+type:pr+repo:{}"
# Default template file
TEMPLATE_FILE = "avd.j2"


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
    parser.add_argument('-t', '--template',
                        help='Path to template', type=str,
                        default=TEMPLATE_FILE)
    parser.add_argument('-o', '--output',
                        help='File to save release-notes', type=str)
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


def templater(milestone, milestone_json, contributors=list(), template_file=TEMPLATE_FILE):
    """
    Generate Release Notes document based on J2 template

    Parameters
    ----------
    milestone : string
        Milestone name
    milestone_json : dict
        JSON data from GH API
    contributors : list, optional
        List of contirubutors for given milestone, by default list()
    template_file : str, optional
        Name of template to use for RN rendering, by default TEMPLATE_FILE

    Returns
    -------
    string
        Release Notes content
    """
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
    templateEnv = jinja2.Environment(loader=templateLoader,
                                     autoescape=True,
                                     trim_blocks=True,
                                     lstrip_blocks=True)
    template = templateEnv.get_template(template_file)
    output_from_parsed_template = template.render(milestone_name=milestone,
                                                  milestone_json=milestone_json,
                                                  contributors=contributors)
    return output_from_parsed_template


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

    release_notes = templater(milestone=cli.milestone,
                              milestone_json=milestone_content,
                              contributors=get_contributors(milestone_prs=milestone_content['items']),
                              template_file=cli.template)

    if cli.output is None:
        print(release_notes)
    else:
        file = open(cli.output, "w")
        file.write(release_notes)
        file.close()
        print("Release notes saved under {}".format(cli.output))

    sys.exit(0)
