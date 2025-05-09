# -*- coding: utf-8 -*-
"""Installer for the eea.testegg package."""

from os.path import join
from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open(join("docs", "HISTORY.txt")).read(),
    ]
)

NAME = "eea.testegg"
PATH = NAME.split(".") + ["version.txt"]
VERSION = open(join(*PATH)).read().strip()

setup(
    name=NAME,
    version=VERSION,
    description="plone test egg to test python pipelines",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Valentina Balan",
    author_email="valentina@eaudeweb.ro",
    url="https://github.com/eea/eea.testegg",
    project_urls={
        "Source": "https://github.com/eea/eea.testegg",
        "Tracker": "https://github.com/eea/eea.testegg/issues",
    },
    license="GPL version 2",
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['eea'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
