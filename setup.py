#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Cutting Edge QA


"""Setup script for Robot's Marcin Koperski bundle distributions"""

from setuptools import setup

version = u'0.0.3'

setup(
    name=u'robotframework-MarcinKoperski',
    version=version,
    description=u'RobotFramework Marcin Koperski bundle',
    author=u'Marcin Koperski',
    author_email=u'marcin.koperski+github[at].gmail.com',
    url=u'https://github.com/IlfirinPL/robotframework-MarcinKoperski',
    download_url=u'https://github.com/IlfirinPL/robotframework-MarcinKoperski/tarball/v{version}'.format(version=version),
    keywords=['robotframework', 'pyral'],
    package_dir={u'': 'src'},
    packages=['TestTools'],
    install_requires=[
        u'robotframework>=2.9.2',
        u'robotframework-archivelibrary',
        u'robotframework-databaselibrary',
        u'robotframework-imaplibrary',
        u'robotframework-pabot',
        u'robotframework-ride>=1.5a2',
        u'robotframework-selenium2library>=1.7.4',
        u'robotframework-testmanagement',
        u'robotframework-sshlibrary>=2.1.1',
        u'robotframework-sudslibrary'
    ]
)
