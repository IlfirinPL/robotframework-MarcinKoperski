#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os
import time
import sys

import csv
# import unicodecsv as csv
from robot.libraries import DateTime
from robot.utils import asserts

from TestToolsMK import robot_instances
from TestToolsMK.robot_instances import validate_create_artifacts_dir


class CsvKeywords(object):
    OUTPUT_FILE_CSV = "Artifacts/output.csv"

    def csv_set_output_file(self, file_name="Artifacts/output.csv"):
        self.OUTPUT_FILE_CSV = validate_create_artifacts_dir(file_name)

    @staticmethod
    def append_to_csv(filename, values_list, encoding='UTF-8'):
        """
        Example usage:
        | ${list} | Create List	| a | ""1"" |	"é,őáá" | #example with chars utf-8 |
        | Append To Csv | example.csv   |
        """
        if sys.version_info[0] < 3:
            with open(filename, 'ab') as csv_file:
                writer_csv = csv.writer(csv_file, dialect='excel')
                writer_csv.writerow([item.encode(encoding) for item in values_list])
        else:
            with open(filename, 'a', newline='') as csv_file:
                writer_csv = csv.writer(csv_file, dialect='excel')
                writer_csv.writerow([item for item in values_list])

    def csv_writer(self, *values):
        """
        Store to default file records in csv
        ${EXECDIR}/Artifacts/output.csv
        change file name using csv change output file
        """
        log_file = self.OUTPUT_FILE_CSV
        self.append_to_csv(log_file, list(values))

    def csv_writer_with_extra(self, *values):
        """
        Add extra params at beginning
        1. time of execution
        2. suite + test cases name
        """
        test_case_name = str(robot_instances.bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(robot_instances.bi().get_variable_value("${SUITE_NAME}"))
        extra_list = list(values)
        extra_list.insert(0, suite_name + test_case_name)
        self.csv_writer_with_time(*extra_list)

    def csv_writer_with_time(self, *values):
        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        extra_list = list(values)
        extra_list.insert(0, current_time)
        self.csv_writer(*extra_list)

    @staticmethod
    def file_should_not_change(filename, time_in_sec="1", msg="File was modify during waiting time"):
        """
        Methods check modification date date if date doesnt change after set time return true
        Best use with method Wait Until Keyword Succeeds
        """
        before = os.stat(filename).st_mtime
        time.sleep(float(time_in_sec))
        after = os.stat(filename).st_mtime
        asserts.assert_equal(before, after, msg, values=False)

    @staticmethod
    def append_to_file_at_beginning(path, content, encoding="UTF-8"):
        path = os.path.abspath(path)
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(parent)
        if not os.path.isfile(path):
            open(path, 'w').close()
        with open(path, 'r') as original:
            data = original.read()
        final_content = content + "\n" + data
        with open(path, 'w') as modified:
            modified.write(final_content.encode(encoding))
        # noinspection PyProtectedMember
        robot_instances.osl()._link("Appended to file begin of file '%s'.", path)

    @staticmethod
    def get_file_lines_count(path):
        with open(path) as f:
            for i, l in enumerate(f):
                pass
            # noinspection PyUnboundLocalVariable
            return i + 1

    @staticmethod
    def csv_read_file(path, encoding='UTF-8', encoding_errors='strict',delimiter=',',quotechar='"'):
        """
        returns file CSV content as 2D table
        """
        output_table = []
        # encoding = osl()._map_encoding(encoding)
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, quotechar=quotechar,delimiter=delimiter)
            for row in csv_reader:
                output_table.append(row)
            return output_table

    @staticmethod
    def csv_read_file_return_dictionary(path, encoding='UTF-8', encoding_errors='strict',delimiter=',',quotechar='"'):
        """
        returns file CSV content as 1D table of dictionaries
        """
        output_table = []
        # encoding = osl()._map_encoding(encoding)
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file, quotechar=quotechar,delimiter=delimiter)
            for row in csv_reader:
                output_table.append(row)
            return output_table