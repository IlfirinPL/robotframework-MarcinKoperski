#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import io
import os
import time
from robot.api import logger
import unicodecsv as csv
from openpyxl import load_workbook
from robot.libraries import DateTime
from robot.utils import asserts

from TestToolsMK.robot_instances import validate_create_artifacts_dir
from robot_instances import *
import openpyxl


class ExcelKeywords(object):
    def __init__(self):
        self.wb = None  # type: openpyxl.workbook
        self.tb = None
        self.sheetNum = None
        self.sheetNames = None
        self.currentSheet = None  # type: openpyxl.worksheet
        self.fileName = None
        if os.name is "nt":
            self.tmpDir = "Temp"
        else:
            self.tmpDir = "tmp"

    def open_excel(self, filename, read_only=True, **kwark):
        """
        Open spread excel and return spreadsheet names
        :param self: 
        :param filename: 
        :param kwark: 
        :return: 
        """
        self.fileName = filename
        self.wb = load_workbook(self.fileName, read_only, **kwark)
        self.sheetNames = self.wb.get_sheet_names()
        return self.sheetNames

    def select_SpreadSheet(self, name=""):

        if (name == ""):
            name = self.sheetNames[0]
            self.currentSheet = self.wb[name]
        else:
            self.currentSheet = self.wb[name]

    def get_all_values(self):

        table = []
        for row in self.currentSheet.rows:

            single_row = []
            for cell in row:
                single_row.append(cell.value)

            table.append(single_row)
        return table

    def get_cell_data_by_coordinates(self, column, row):

        cellValue = self.currentSheet[column + row].value
        return cellValue
