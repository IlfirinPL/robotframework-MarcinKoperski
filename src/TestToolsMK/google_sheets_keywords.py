#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import json
import re
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


class GoogleSheetsKeywords(object):
    SPREADSHEET = None
    WORKSHEET = None
    JSON_KEY = None

    def __init__(self, key_json_file=None, google_document_id=None, worksheet_name=None, **kwargs):
        super(GoogleSheetsKeywords, self).__init__(**kwargs)
        if key_json_file is not None:
            if google_document_id is not None:
                self.get_spreadsheet_by_id(key_json_file, google_document_id, worksheet_name)

    def get_spreadsheet_by_id(self, file_name, google_document_id, worksheet_name=None):
        self.JSON_KEY = json.load(open(file_name))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(self.JSON_KEY['client_email'], self.JSON_KEY['private_key'], scope)
        gc = gspread.authorize(credentials)
        self.SPREADSHEET = gc.open_by_key(google_document_id)
        self.WORKSHEET = self.SPREADSHEET.sheet1
        if worksheet_name is not None:
            self.WORKSHEET = self.SPREADSHEET.worksheet(worksheet_name)
        else:
            self.WORKSHEET = self.SPREADSHEET.sheet1

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
        print pattern
        amount_re = re.compile(pattern)
        return self.WORKSHEET.find(amount_re)

    def find_all_cell_using_regex(self, regex):
        """Return password for provided login, rise error when login is missing"""
        pattern = r'%s' % regex
        amount_re = re.compile(pattern)
        return self.WORKSHEET.findall(amount_re)
