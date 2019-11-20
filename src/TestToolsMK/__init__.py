#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
from __future__ import print_function

import os

from TestToolsMK.collections_keywords import CollectionsKeywords
from TestToolsMK.csv_keywords import CsvKeywords
from TestToolsMK.excel_keywords import ExcelKeywords
from TestToolsMK.google_sheets_keywords import GoogleSheetsKeywords
from TestToolsMK.image_magick_keywords import ImageMagickKeywords
from TestToolsMK.logger_extension_keywords import LoggerKeywords
from TestToolsMK.pdf_keywords import PDFKeywords
from TestToolsMK.selenium_extentions_keywords import SeleniumLibraryKeywords
from TestToolsMK.send_android_notification_keywords import SendNotificationKeywords
from TestToolsMK.sqlkeywords import SQLKeywords
from TestToolsMK.timers_keywords import TimerKeywords
from TestToolsMK.utils import UtilsKeywords

__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class TestToolsMK(GoogleSheetsKeywords, SeleniumLibraryKeywords, TimerKeywords, CollectionsKeywords, ImageMagickKeywords, LoggerKeywords, CsvKeywords,
                  SQLKeywords, UtilsKeywords, SendNotificationKeywords, ExcelKeywords,PDFKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

