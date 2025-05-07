#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
import os

__author__ = "hujianli94"
__email__ = "your_email@example.com"
__license__ = "MIT"
__description__ = "A simple project template for Ansible"
__url__ = "https://github.com/hujianli94/asb-pl-template"


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), "asb_pl_template", "__init__.py")

version_line = list(filter(lambda l: l.startswith("VERSION"), open(init)))[0]

VERSION = get_version(eval(version_line.split('=')[-1]))

README = os.path.join(os.path.dirname(__file__), "README.md")


def read_md(file_path):
    with open(file_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description


def strip_comments(l):
    # strip comments and empty lines
    return l.split("#", 1)[0].strip()


def reqs(*f):
    # read requirements from file
    return list(
        filter(None, [strip_comments(l) for l in open(os.path.join(os.path.dirname(__file__), *f)).readlines()]))


setuptools.setup(
    name="asb_pl_template",
    version=VERSION,
    author=__author__,
    author_email=__email__,
    license=__license__,
    description=__description__,
    long_description=read_md(README),
    long_description_content_type="text/markdown",
    url=__url__,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.6',
    install_requires=reqs("requirements.txt"),
    entry_points={
        'console_scripts': [
            'asb_pl_template = asb_pl_template.cli:main',
        ],
    },
)
