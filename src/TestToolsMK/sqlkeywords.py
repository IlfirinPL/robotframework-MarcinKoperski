#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os
# from xmlrpclib import DateTime
import string
import random
from datetime import datetime
import codecs

from robot.api import logger
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.utils import (is_falsy)

from TestToolsMK.robot_instances import dbl, ttmkl, validate_create_artifacts_dir
import sys


def get_current_time_for_timers():
    return datetime.now()


# noinspection PyProtectedMember
class SQLKeywords(object):
    OUTPUT_FILE_LOG_SQL = "Artifacts/log_of_sql_execution.sql"
    ADD_LOGS_FLAG = True

    def set_sql_log_output_file(self, path="Artifacts/log_of_sql_execution.sql"):
        self.OUTPUT_FILE_LOG_SQL = validate_create_artifacts_dir(path)

    def set_add_logs_flag(self, flag=False):
        self.ADD_LOGS_FLAG = flag

    def query_many_rows(self, select_statement, append_to_logs=ADD_LOGS_FLAG):
        """
        To switch output file with logs use
        | Set Sql Log Output File | ./myFile.sql |
        :param select_statement:
        :param append_to_logs:
        :return:
        """
        if append_to_logs:
            self._add_query_to_log_file(select_statement)
        results = dbl().query(select_statement)
        if append_to_logs:
            self._add_results_to_log_file(results)
        return results

    def query_row(self, select_statement, append_to_logs=ADD_LOGS_FLAG):
        """
        To switch output file with logs use
        | Set Sql Log Output File | ./myFile.sql |
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
        To switch output file with logs use
        | Set Sql Log Output File | ./myFile.sql |
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
        final_string = "\n/* Start execution, statement below : " + current_time.strftime(
            "%Y.%m.%d %H:%M:%S") + " */\n" + statement + "\n"
        self._append_to_file(final_string)

    def _add_results_to_log_file(self, results):
        current_time = get_current_time_for_timers()
        total_time_verbose = Time(current_time - self.start_time).convert("verbose")

        if results:
            data = "[\n"
            for i in range(len(results)):
                data += "("
                for j in range(len(results[i])):
                    data += repr(results[i][j])
                    if j != (len(results[i]) - 1):
                        data += "\t,"
                data += ")\n"
            data += "]"
        else:
            data = ""
        final_string = "/* Response of statement in :" + total_time_verbose + " , data below " + data + " */\n"
        self._append_to_file(final_string)

    def _append_to_file(self, text):
        full_log_file_path = validate_create_artifacts_dir(self.OUTPUT_FILE_LOG_SQL)
        modeFile = 'a' if os.path.exists(full_log_file_path) else 'w'
        with codecs.open(full_log_file_path, modeFile, "utf-8") as output:
            output.write(text)

    def execute_sql_string_with_logs(self, sql_string, append_to_logs=ADD_LOGS_FLAG):
        """
        To switch output file with logs use
        | Set Sql Log Output File | ./myFile.sql |
        :param sql_string:
        :param append_to_logs:
        :return:
        """
        if append_to_logs:
            self._add_query_to_log_file(sql_string)
        dbl().execute_sql_string(sql_string)
        if append_to_logs:
            self._add_results_to_log_file(None)

    def insert_data_to_table(self, table_name, data):
        """
        return table name, table will have columns with names 'c0', 'c1' for all columns
        table will be also reindex after insert
        """
        cur = dbl()._dbconnection.cursor()

        size = len(data)
        if size < 1:
            raise AssertionError("missing data 0 rows")

        row_size = len(data[0])
        if row_size < 1:
            raise AssertionError("missing data 0 columns")

        columns_desc = ""
        for index in range(len(data[0])):
            columns_desc += """"c""" + str(index) + """" VARCHAR"""
            if index < (row_size - 1):
                columns_desc += ","

        create_sql = "CREATE TABLE \"%s\" (%s)" % (table_name, columns_desc)

        logger.info(create_sql)
        cur.execute(create_sql)

        columns_names = ""
        values = ""
        for index in range(len(data[0])):
            columns_names += "c" + str(index)
            values += """?"""
            if index < (row_size - 1):
                columns_names += ", "
                values += ", "

        insert_data_sql = "INSERT INTO \"main\".\"%s\" (%s) VALUES (%s) " % (table_name, columns_names, values)

        logger.info(insert_data_sql)
        cur.executemany(insert_data_sql, data)

        reindex_sql = "REINDEX \"main\".\"%s\"" % table_name
        cur.execute(reindex_sql)

        dbl()._dbconnection.commit()

        return

    def insert_data_to_generated_table(self, data):
        table_name = table_name_generator()
        self.insert_data_to_table(table_name, data)
        return table_name

    def csv_read_file_to_database(self, table_name, csv_file, encoding='UTF-8', encoding_errors='strict'):
        """ Use only for temporary use
        connect to database in memory if not connected, create table with name and import data from csv file"""

        if dbl()._dbconnection is None:
            dbl().connect_to_database_using_custom_params("sqlite3", "':memory:'")
        array_table = ttmkl().csv_read_file(csv_file, encoding, encoding_errors)
        self.insert_data_to_table(table_name, array_table)
        return table_name

    def connect_to_database_using_jdbc_driver(self, jdbc_connection_string, user, password, jdbc_driver, jdbc_jar_path,
                                              library="jaydebeapi"):
        """
        Example parameters for CIS databases Cisto Integration Services, using java drivers is done using library
        jdbc_connection_string: jdbc:compositesw:dbapi@localhost:9401?domain=composite&dataSource=Example
        jdbc_driver: cs.jdbc.driver.CompositeDriver
        jdbc_jar_path: Binaries/csjdbc.jar
        jaydebeapi library has to be installed 

        """
        dbl().connect_to_database_using_custom_params(library, "\"%s\",\"%s\",[ \"%s\", \"%s\"],\"%s\"," % (
            jdbc_driver, jdbc_connection_string, user, password,
            jdbc_jar_path))


def table_name_generator(size=12, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
