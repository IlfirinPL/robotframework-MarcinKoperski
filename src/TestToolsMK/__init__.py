#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from __future__ import print_function

import os

from TestToolsMK.collections_keywords import CollectionsKeywords
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.google_sheets_keywords import GoogleSheetsKeywords
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.logger_extension_keywords import LoggerKeywords
from TestToolsMK.selenium_extentions_keywords import Selenium2LibraryKeywords
from TestToolsMK.sqlkeywords import SQLKeywords
from TestToolsMK.timers_keywords import TimerKeywords
__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class TestToolsMK(GoogleSheetsKeywords, Selenium2LibraryKeywords, TimerKeywords, CollectionsKeywords, ImageMagickKeywords, LoggerKeywords, CsvKeywords,
    SQLKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

