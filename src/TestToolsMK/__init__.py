#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.logger_extension import LoggerKeywordsExtension
from robot.version import VERSION
from TestToolsMK.collections_keywords import CollectionsKeywordsExtension
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.selenium_extentions import Selenium2LibraryExtensions
from TestToolsMK.google_sheets import GoogleSheets
from TestToolsMK.timers import TimerKeywords
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class TestToolsMK(GoogleSheets, Selenium2LibraryExtensions, TimerKeywords, CollectionsKeywordsExtension, ImageMagickKeywords, LoggerKeywordsExtension,
    CsvKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        print "TestToolsMK loaded"
        # super(TestToolsMK, self).__init__(**kwargs)
