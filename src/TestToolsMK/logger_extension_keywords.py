#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import csv
import os

from robot.api import logger
from robot.libraries import DateTime

from TestToolsMK.robot_instances import validate_create_artifacts_dir
from robot_instances import *


class LoggerKeywords(object):

    @staticmethod
    def log_variable_to_file(name, comment="", output_file="Artifacts/variables.csv"):
        log_file = validate_create_artifacts_dir(output_file)
        logger.debug("Log to file " + log_file)
        fieldnames = ['Time', 'Test Case Name', 'Variable Name', 'Variable Value', 'Comment']
        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        test_case_name = str(bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(bi().get_variable_value("${SUITE_NAME}"))
        variable_value = name

        # TODO
        # get variable name is not working
        # variable_name = _Variables._get_var_name(bi(),str(name))
        # bi().get_variable_value("${" + variable_name + "}", "Missing!!!")

        with open(log_file, 'ab') as csv_file:
            writer_csv = csv.writer(csv_file, dialect='excel')
            if os.stat(log_file).st_size < 10:
                writer_csv.writerow(fieldnames)
            writer_csv.writerow([current_time, suite_name + "." + test_case_name, name, variable_value, comment])

    # noinspection PyProtectedMember
    @staticmethod
    def set_log_level_none():
        temp = bi()._context.output.set_log_level("None")
        bi().set_global_variable("${previous log level}", temp)

    # noinspection PyProtectedMember
    @staticmethod
    def set_log_level_restore():
        temp = bi().get_variable_value("${previous log level}")
        if temp is None:
            temp = "INFO"
        bi()._context.output.set_log_level(temp)
