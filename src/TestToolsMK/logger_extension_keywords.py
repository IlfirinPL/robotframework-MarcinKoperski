#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import csv
import os

from robot.libraries import DateTime

from robot_instances import *


class LoggerKeywords(object):
    OUTPUT_FILE = None

    def __init__(self, **kwargs):
        super(LoggerKeywords, self).__init__(**kwargs)
        self.OUTPUT_FILE = bi().get_variable_value("${EXECDIR}")

    @staticmethod
    def log_variable_to_file(name, comment="", output_file="variables.csv", level="INFO", html=False):
        log_file = get_artifacts_dir(output_file)

        fieldnames = ['Time', 'Test Case Name', 'Variable Name', 'Variable Value', 'Comment']
        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        test_case_name = str(bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(bi().get_variable_value("${SUITE_NAME}"))
        variable_value = name

        # TODO
        # get variable name is not working
        # variable_name = _Variables._get_var_name(bi(),str(name))
        # bi().get_variable_value("${" + variable_name + "}", "Missing!!!")

        with open(log_file, 'ab') as  csvfile:
            writer_csv = csv.writer(csvfile, dialect='excel')
            if os.stat(log_file).st_size < 10:
                writer_csv.writerow(fieldnames)
            writer_csv.writerow([current_time, suite_name + "." + test_case_name, name, variable_value, comment])

    def set_log_level_none(self):
        temp = bi()._context.output.set_log_level("None")
        bi().set_global_variable("${previous log level}", temp)

    def set_log_level_restore(self):
        temp = bi().get_variable_value("${previous log level}")
        if temp is None:
            temp = "INFO"
        bi()._context.output.set_log_level(temp)
