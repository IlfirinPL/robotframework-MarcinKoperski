#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.logger_extension import LoggerKeywordsExtension
from TestToolsMK.collections_keywords import CollectionsKeywordsExtension
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.selenium_extentions import Selenium2LibraryExtensions
from TestToolsMK.google_sheets import GoogleSheets
from TestToolsMK.timers import TimerKeywords
import os

__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class TestToolsMK(GoogleSheets, Selenium2LibraryExtensions, TimerKeywords, CollectionsKeywordsExtension, ImageMagickKeywords, LoggerKeywordsExtension,
    CsvKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, **kwargs):
        print "TestToolsMK loaded"
        # super(TestToolsMK, self).__init__(**kwargs)
