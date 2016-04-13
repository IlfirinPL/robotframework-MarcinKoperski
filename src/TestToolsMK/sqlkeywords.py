#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
import os
from xmlrpclib import DateTime

from TestToolsMK.robot_instances import *
from datetime import datetime

from robot.api import logger
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.utils import (is_falsy)

from TestToolsMK.robot_instances import dbl


def get_current_time_for_timers():
    return datetime.now()


class SQLKeywords(object):
    OUTPUT_FILE_LOG_SQL = "log_of_sql_execution.sql"
    ADD_LOGS_FLAG = True

    def set_sql_log_output_file(self, name):
        self.OUTPUT_FILE_LOG_SQL = name

    def query_many_rows(self, select_statement, append_to_logs=ADD_LOGS_FLAG):
        if append_to_logs:
            self._add_query_to_log_file(select_statement)
        results = dbl().query(select_statement)
        if append_to_logs:
            self._add_results_to_log_file(results)
        return results

    def query_row(self, select_statement, append_to_logs=ADD_LOGS_FLAG):
        """
        :raise error when results contains more then one row results
        :return: table
        """
        results = self.query_many_rows(select_statement, append_to_logs)

        if len(results) > 1:
            message = "Error. Results contains more then one row. Actual size is %s " % (len(results))
            self._append_to_file("/* \n" + message + "\n */")
            raise AssertionError(message)

        return results[0]

    def query_cell(self, select_statement, append_to_logs=ADD_LOGS_FLAG):
        """
        :raise error when results contains more then one cell
        :return: single value
        """
        results = self.query_row(select_statement, append_to_logs)
        if len(results) > 1:
            message = "Error. Results contains more then one cell. Actual size is %s " % (len(results))
            self._append_to_file("/* \n" + message + "\n */")
            raise AssertionError(message)
        return results[0]

    def _add_query_to_log_file(self, statement):
        current_time = get_current_time_for_timers()
        self.start_time = current_time
        final_string = "\n/* Start execution, statement below : " + current_time.strftime("%Y.%m.%d %H:%M:%S") + " */\n" + statement + "\n"
        self._append_to_file(final_string)

    def _add_results_to_log_file(self, results):
        current_time = get_current_time_for_timers()
        total_time_verbose = Time(current_time - self.start_time).convert("verbose")

        if results:
            data = "[\n"
            for i in range(len(results)):
                data += "("
                for j in range(len(results[i])):
                    data += str(results[i][j])
                    if j != (len(results[i]) - 1):
                        data += "\t,"
                data += ")\n"
            data += "]"
        else:
            data = ""
        final_string = "/* Response of statement in :" + total_time_verbose + " , data below " + data + " */\n"
        self._append_to_file(final_string)

    def _append_to_file(self, text):
        full_log_file_path = os.path.normpath(get_artifacts_dir() + "/" + self.OUTPUT_FILE_LOG_SQL)
        mode = 'a' if os.path.exists(full_log_file_path) else 'w'
        with open(full_log_file_path, mode) as output:
            output.write(text)

    def execute_sql_string_with_logs(self, sql_string, append_to_logs=ADD_LOGS_FLAG):
        if append_to_logs:
            self._add_query_to_log_file(sql_string)
        dbl().execute_sql_string(sql_string)
        if append_to_logs:
            self._add_results_to_log_file(None)
