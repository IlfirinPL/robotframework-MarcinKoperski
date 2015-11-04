#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import robot
from robot.libraries import DateTime
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
from robotide.lib.robot.errors import DataError
from robot_instances import *
import csv


class LoggerKeywordsExtension(object):
    OUTPUT_FILE = None

    def __init__(self):
        self.OUTPUT_FILE = bi().get_variable_value("${EXECDIR}")

    @staticmethod
    def log_variable_to_file(variable_name, comment="", output_dir="variables.csv", level="INFO", html=False):
        log_file = get_artifacts_dir(output_dir)

        fieldnames = ['Time', 'Test Case Name', 'Variable Name', 'Variable Value', 'Comment']
        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        test_case_name = str(bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(bi().get_variable_value("${SUITE_NAME}"))
        variable_value = bi().get_variable_value("${" + variable_name + "}", "Missing!!!")

        with open(log_file, 'ab') as  csvfile:
            writer_csv = csv.writer(csvfile, dialect='excel')
            if os.stat(log_file).st_size < 10:
                writer_csv.writerow(fieldnames)
            writer_csv.writerow([current_time, suite_name + "." + test_case_name, variable_name, variable_value, comment])

        logger.write(bi().get_variable_value("${" + variable_name + "}", "Missing!!!"), level, html)
