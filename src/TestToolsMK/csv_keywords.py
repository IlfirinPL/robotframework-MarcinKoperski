#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import csv
import os

from robot.libraries import DateTime

from robot_instances import *


class Csv_Keywords(object):
    OUTPUT_FILE = None

    def __init__(self, **kwargs):
        super(Csv_Keywords, self).__init__(**kwargs)
        self.OUTPUT_FILE = "output.csv"

    def csv_writer(self, *values):
        log_file = get_artifacts_dir(self.OUTPUT_FILE)
        with open(log_file, 'ab') as  csvfile:
            writer_csv = csv.writer(csvfile, dialect='excel')
            if os.stat(log_file).st_size < 10:
            # writer_csv.writerow(fieldnames)
            writer_csv.writerow(values)

    def csv_writer_with_extra(self, *values):
        list = []

        current_time = DateTime.get_current_date(result_format="%Y.%m.%d %H:%M:%S")
        test_case_name = str(bi().get_variable_value("${TEST_NAME}"))
        suite_name = str(bi().get_variable_value("${SUITE_NAME}"))

        list.insert(0, current_time)
        list.insert(0, suite_name + test_case_name)
        list = list + values
        self.csv_writer(**list)
