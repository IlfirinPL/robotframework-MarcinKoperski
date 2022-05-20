#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os

from TestToolsMK.collections_keywords import CollectionsKeywords
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.logger_extension_keywords import LoggerKeywords
from TestToolsMK.selenium_extentions_keywords import SeleniumLibraryKeywords
from TestToolsMK.sqlkeywords import SQLKeywords
from TestToolsMK.timers_keywords import TimerKeywords
from TestToolsMK.utils import UtilsKeywords

__version_file_path__ = os.path.join(os.path.dirname(__file__), "VERSION")
__version__ = open(__version_file_path__, "r").read().strip()


class TestToolsMK(
    CollectionsKeywords,
    CsvKeywords,
    ImageMagickKeywords,
    LoggerKeywords,
    SeleniumLibraryKeywords,
    SQLKeywords,
    TimerKeywords,
    UtilsKeywords,
):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = __version__
