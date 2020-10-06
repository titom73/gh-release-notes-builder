import os
import sys
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="Github Release Notes builder",
    version="0.1",
    python_requires=">=3.6",
    scripts=["bin/release-notes-github"],
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    url="https://github.com/titom73/gh-release-notes-builder",
    license="GPLv3",
    author="Thomas Grimonet",
    author_email="tom@inetsix.net",
    description="Script to build Release Notes based on Github Milestone",
)