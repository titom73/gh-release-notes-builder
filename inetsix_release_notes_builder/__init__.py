#!/usr/bin/python
# coding: utf-8 -*-

import sys
import os
import logging
import requests
import jinja2

# CONSTANTS

# API URI to use to get Milestone information.
GH_API_MILESTONE = "https://api.github.com/search/issues?per_page=100&q=milestone:{}+type:pr+repo:{}"

__author__ = "titom73"
__version__ = 0.1


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


def templater(milestone, milestone_json, contributors=list(), template_file="default.j2"):
    """
    Generate Release Notes document based on J2 template

    Parameters
    ----------
    milestone : string
        Milestone name
    milestone_json : dict
        JSON data from GH API
    contributors : list, optional
        List of contributors for given milestone, by default list()
    template_file : str, optional
        Name of template to use for RN rendering, by default TEMPLATE_FILE

    Returns
    -------
    string
        Release Notes content
    """
    # templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
    template_path = '%s/templates/'% os.path.dirname(__file__)
    templateLoader = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                        autoescape=jinja2.select_autoescape(),
                                        trim_blocks=True,
                                        lstrip_blocks=True)
    try:
        template = templateLoader.get_template(template_file)
    except jinja2.TemplateNotFound as error:
        logging.error("Template not found in %s", str(template_path))
    else:
        output_from_parsed_template = template.render(milestone_name=milestone,
                                                      milestone_json=milestone_json,
                                                      contributors=contributors)
        return output_from_parsed_template
    return None
