#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os

from TestToolsMK.collections_keywords import CollectionsKeywords
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.image_pillow_keywords import ImagePillowKeywords
from TestToolsMK.logger_extension_keywords import LoggerKeywords
from TestToolsMK.selenium_extensions_keywords import ExtendedSeleniumLibrary
from TestToolsMK.sql_keywords import SQLKeywords
from TestToolsMK.timers_keywords import TimerKeywords
from TestToolsMK.utils import UtilsKeywords

__version_file_path__ = os.path.join(os.path.dirname(__file__), "VERSION")
__version__ = open(__version_file_path__, "r").read().strip()


class TestToolsMK(
    CollectionsKeywords,
    CsvKeywords,
    ImagePillowKeywords,
    LoggerKeywords,
    ExtendedSeleniumLibrary,
    SQLKeywords,
    TimerKeywords,
    UtilsKeywords,
):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        pass
