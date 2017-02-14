#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

from __future__ import print_function

import json
import re

import gspread
from robot.api import logger
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GoogleSheetsKeywords(object):
    SPREADSHEET = None  # type: gspread.Spreadsheet
    WORKSHEET = None  # type: gspread.Worksheet
    JSON_KEY = None  # type: file

    def __init__(self, key_json_file=None, google_document_id=None, worksheet_name=None):
        if key_json_file is not None:
            if google_document_id is not None:
                self.get_spreadsheet_by_id(key_json_file, google_document_id, worksheet_name)

    def get_spreadsheet_by_id(self, file_name, google_document_id, worksheet_name=None):
        self.JSON_KEY = json.load(open(file_name))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
        gc = gspread.authorize(credentials)
        self.SPREADSHEET = gc.open_by_key(google_document_id)
        self.WORKSHEET = self.SPREADSHEET.sheet1
        if worksheet_name is not None:
            self.WORKSHEET = self.SPREADSHEET.worksheet(worksheet_name)
        else:
            self.WORKSHEET = self.SPREADSHEET.sheet1

        logger.info("Spreadsheet id opened '" + google_document_id + "'")
        logger.info("worksheet opened '" + self.WORKSHEET.title + "'")

    def select_worksheet_by_name(self, worksheet_name):
        self.WORKSHEET = self.SPREADSHEET.worksheet(worksheet_name)

    def get_dictionary_logins_and_passwords(self):
        return dict(zip(self.WORKSHEET.col_values(1), self.WORKSHEET.col_values(2)))

    def get_password_for_login(self, login):
        """Return password for provided login, rise error when login is missing"""
        dictionary = self.get_dictionary_logins_and_passwords()
        return dictionary[login]

    def find_cell_using_regex(self, regex):
        """Return password for provided login, rise error when login is missing"""
        pattern = r'%s' % regex
        print(pattern)
        amount_re = re.compile(pattern)
        return self.WORKSHEET.find(amount_re)

    def find_all_cell_using_regex(self, regex):
        """Return password for provided login, rise error when login is missing"""
        pattern = r'%s' % regex
        amount_re = re.compile(pattern)
        return self.WORKSHEET.findall(amount_re)

    def insert_row(self, values, index=1):
        """
        first argument is list, second optional index
        """
        self.WORKSHEET.insert_row(values, int(index))
        logger.info("Row inserted to index " + str(index) + " to Spreadsheet " + self.SPREADSHEET.title)
