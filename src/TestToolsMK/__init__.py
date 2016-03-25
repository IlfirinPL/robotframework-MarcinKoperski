#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.logger_extension_keywords import LoggerKeywords
from TestToolsMK.collections_keywords import CollectionsKeywords
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.selenium_extentions_keywords import Selenium2LibraryKeywords
from TestToolsMK.google_sheets_keywords import GoogleSheetsKeywords
from TestToolsMK.sqlite_keywords import SQLITE_Keywords
from TestToolsMK.timers_keywords import TimerKeywords
import os

__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class TestToolsMK(GoogleSheetsKeywords, Selenium2LibraryKeywords, TimerKeywords, CollectionsKeywords, ImageMagickKeywords, LoggerKeywords, CsvKeywords,
    SQLITE_Keywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, **kwargs):
        print "TestToolsMK loaded"
        # super(TestToolsMK, self).__init__(**kwargs)
