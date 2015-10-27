#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from robot.version import VERSION

from selenium_extentions import Selenium2LibraryExtensions
from google_sheets import GoogleSheets
from timers import TimerKeywords
import os


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION


class TestToolsMK(GoogleSheets, Selenium2LibraryExtensions, TimerKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION
