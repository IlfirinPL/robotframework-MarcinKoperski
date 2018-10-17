#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
from PyPDF2.generic import NameObject

from TestToolsMK import robot_instances
import PyPDF2
from robot.api import logger


class PDFKeywords(object):
    pdfReader = None  # type: PyPDF2.PdfFileReader

    def __open_pdf(self, path):
        """
        read_pdf file read
        and return number of pages
        """
        pdfFileObj = open(path, 'rb')

        # creating a pdf reader object
        self.pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)

        # closing the pdf file object

        # printing number of pages in pdf file
        # logger.info("Open PDF in " + path + " loaded with " + self.pdfReader.numPages + " pages")
        return self.pdfReader.numPages


    def get_file_pdf(self, path, split_by_page="False"):
        """
        Return text from file
        with splitByPage=True return list with splitted by page
        @return:
        """
        self.__open_pdf(path)

        pages = list()
        for pageNumber in range(0, self.pdfReader.numPages):
            # creating a page object
            pageObj = self.pdfReader.getPage(pageNumber)
            name = pageObj.extractText().strip().strip('\n')
            pages.append(name)
            # extracting text from page
            logger.debug("Page\t" + str(pageNumber) + " \tBody\t" + name)
        # self.pdfFileObj.close()

        if split_by_page != "False":
            return pages
        else:
            return "\n".join(pages)
