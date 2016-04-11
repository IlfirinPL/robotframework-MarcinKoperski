#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import sqlite3


class SQLiteKeywords(object):
    conn = None
    cursor = None

    def open_database_sqlite_file(self, path, **kwargs):
        """
        connect(database[, timeout, isolation_level, detect_types, factory])

        Opens a connection to the SQLite database file *database*. You can use
        ":memory:" to open a database connection to a database that resides in
        RAM instead of on disk.
        """

        self.conn = sqlite3.connect(path, **kwargs)
        self.conn.enable_load_extension(True)
        self.cursor = self.conn.cursor()

    def open_database_sqlite_using_csv_file(self, path, table):
        """
        Open csv file as database in ram it will not persist
        """
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.conn.execute(".mode csv")
        self.conn.execute(".import " + path + " " + table)

    def execute_sql_string_sqlite(self, sql_string):
        self.cursor.execute(sql_string)
        temp = self.cursor.fetchall()
        self.conn.commit()
        return temp

    def execute_sql_string_script_sqlite(self, sql_script_string):
        self.cursor.executescript(sql_script_string)
        temp = self.cursor.fetchall()
        self.conn.commit()
        return temp

    def disconnect_database_sqlite(self):
        self.conn.close()
