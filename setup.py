#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Cutting Edge QA


"""Setup script for Robot's Marcin Koperski bundle distributions"""

from setuptools import setup

import sys, os

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

__version_file_path__ = os.path.join(src_path, 'TestToolsMK', 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


setup(
    name=u'robotframework-MarcinKoperski', version=__version__,
    description=u'RobotFramework Marcin Koperski bundle',
    author=u'Marcin Koperski',
    author_email=u'marcin.koperski+github[at].gmail.com', license='AGPL',
    url=u'https://github.com/IlfirinPL/robotframework-MarcinKoperski',
    download_url=u'https://github.com/IlfirinPL/robotframework-MarcinKoperski/archive/master.zip'.format(version=__version__), keywords=['robotframework'],
    package_dir={u'': 'src'}, packages=['TestToolsMK'], exclude_package_data={'': ['.git', '.git/*', '.idea', '.gitignore', 'doc/*', 'atest/*']},
    package_data={'TestToolsMK': ['VERSION']},
    install_requires=[
        u'robotframework>=3.0',
        u'robotframework-archivelibrary',
        u'robotframework-databaselibrary', u'robotframework-imaplibrary', u'robotframework-pabot', u'robotframework-ride==1.5.2.1',
        u'robotframework-selenium2library>=1.7.4',
        u'robotframework-testmanagement>=0.1.10',  # u'robotframework-sshlibrary>=2.1.1',
        u'robotframework-sudslibrary',
        u'robotframework-appiumlibrary',
        u'gspread', u'unicodecsv',
        u'oauth2client==1.5.2',
        u'selenium',
        u'robotframework-httplibrary'

    ]
)
