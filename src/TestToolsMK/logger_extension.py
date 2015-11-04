#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import robot
from robot.libraries.BuiltIn import BuiltIn
import robot.libraries.DateTime
from robot.libraries.DateTime import Time
from robot.libraries.DateTime import Date
from robot.api import logger
from datetime import datetime, timedelta
import time
import re
import datetime
from robot.version import get_version
from robot.utils import (elapsed_time_to_string, is_falsy, is_number, is_string, secs_to_timestr, timestr_to_secs, type_name, IRONPYTHON)
from robot_instances import *


class LoggerKeywordsExtension(object):
    OUTPUT_FILE = None

    def __init__(self):
        self.OUTPUT_FILE = bi().get_variable_value("${EXECDIR}")

    @staticmethod
    def log_variable_to_file_test(variable_name, level="INFO", html=False):
        logger.write(bi().get_variable_value(variable_name), level, html)
