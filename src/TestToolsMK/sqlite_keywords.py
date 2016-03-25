#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import csv
import os

from robot.libraries import DateTime

from robot_instances import *
import sqlite3


class SQLITE_Keywords(object):
    def open_database_sqlite_file(self, path, timeout=None, isolation_level=None, detect_types=None, factory=None):
        self.conn = sqlite3.connect(path, timeout, isolation_level, detect_types, factory)
        self.conn.enable_load_extension(True)
        self.cursor = self.conn.cursor()

    def open_database_sqlite_using_csv_file(self, path):
        """
        Open csv file as database in ram it will not persiste
        """
        self.conn = sqlite3.connect(':memory:')
        self.conn.enable_load_extension(True)
        self.cursor = self.conn.cursor()

    def execute_sql_string_sqlite(self, sqlString):
        self.cursor.execute(sqlString)
        temp = self.cursor.fetchall();
        self.conn.commit()
        print temp

    def execute_sql_string_script_sqlite(self, sqlScriptString):
        self.cursor.executescript(sqlScriptString)
        temp = self.cursor.fetchall();
        self.conn.commit()
        print temp

    def disconnect_database_sqlite(self):
        self.conn.close()
