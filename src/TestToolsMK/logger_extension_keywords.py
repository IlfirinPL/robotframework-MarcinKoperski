#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

import csv
import os

from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries import DateTime

from TestToolsMK.robot_instances import bi, validate_create_artifacts_dir


@library
class LoggerKeywords:
    @keyword
    def log_variable_to_file(
        self, name, comment="", output_file="Artifacts/variables.csv"
    ):
        log_file = validate_create_artifacts_dir(output_file)
        logger.debug("Log to file " + log_file)
        fieldnames = [
            "Time",
            "Test Case Name",
            "Variable Name",
            "Variable Value",
            "Comment",
        ]
        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        test_case_name = str(bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(bi().get_variable_value("${SUITE_NAME}"))
        variable_value = name

        with open(log_file, "a", encoding="UTF-8") as csv_file:
            writer_csv = csv.writer(csv_file, dialect="excel")
            if os.stat(log_file).st_size < 10:
                writer_csv.writerow(fieldnames)
            writer_csv.writerow(
                [
                    current_time,
                    suite_name + "." + test_case_name,
                    name,
                    variable_value,
                    comment,
                ]
            )

    # noinspection PyProtectedMember
    @keyword
    def set_log_level_none(self):
        log_level_history = bi().get_variable_value("${LOG_LEVEL_HISTORY}")
        if log_level_history is None:
            log_level_history = []
        old = bi().set_log_level("None")
        log_level_history.append(old)
        bi().set_global_variable("${LOG_LEVEL_HISTORY}", log_level_history)

    # noinspection PyProtectedMember
    @keyword
    def set_log_level_restore(self):
        log_level_history = bi().get_variable_value("${LOG_LEVEL_HISTORY}")
        if not log_level_history:
            bi().set_log_level("INFO")
        else:
            last = log_level_history.pop()
            bi().set_log_level(last)
