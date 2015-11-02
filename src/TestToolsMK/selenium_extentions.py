#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import robot
from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import Selenium2Library


def s2l():
    """

        :rtype : Selenium2Library
        """
    s2l_instance = BuiltIn().get_library_instance('Selenium2Library')
    assert isinstance(s2l_instance, Selenium2Library)
    return Selenium2Library(s2l_instance)


def bi():
    """

        :rtype : BuiltIn
        """
    bi_instance = BuiltIn().get_library_instance('BuiltIn')
    assert isinstance(bi_instance, BuiltIn)
    return Selenium2Library(bi_instance)


class Selenium2LibraryExtensions(object):
    WIDTH_DEFAULT = "1366"
    HEIGHT_DEFAULT = "768"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    # noinspection PyPep8
    XPATH2_JS = 'if(!window.jQuery){var headID = document.getElementsByTagName("head")[0]; var newScript = document.createElement(\'script\'); newScript.type=\'text/javascript\'; newScript.src=\'http://code.jquery.com/jquery-2.1.4.min.js\'; headID.appendChild(newScript);}'
    # noinspection PyPep8
    JQUERY_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    # noinspection PyArgumentList
    def __init__(self):
        for base in Selenium2LibraryExtensions.__bases__:
            if hasattr(base, '__init__'):
                base.__init__(self)
        print "Selenium2LibraryExtensions loaded"

    @staticmethod
    def set_browser_size_and_position(width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x=0, y=0):
        s2l().set_window_size(width, height)
        s2l().set_window_position(x, y)

    @staticmethod
    def go_to_smart(url):
        """Redirect only in on different url"""
        current_url = s2l().get_location()
        if url != current_url:
            s2l().go_to(url)

    @staticmethod
    def click_element_extended(locator, timeout=None, error_msg=None):
        """Click element proceed with following steps
        1.wait_until_page_contains_element
        2.wait_until_element_is_visiblewait_until_element_is_visible
        3.mouse_over"""
        s2l().wait_until_page_contains_element(locator, timeout, error_msg)
        s2l().wait_until_element_is_visible(locator, timeout, error_msg)
        s2l().mouse_over(locator)
        s2l().click_element(locator)

    @staticmethod
    def double_click_element_extended(locator, timeout=None, error=None):
        s2l().wait_until_page_contains_element(locator, timeout, error)
        s2l().wait_until_element_is_visible(locator, timeout, error)
        s2l().mouse_over(locator)
        s2l().double_click_element(locator)

    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error_msg=None, reason=None):
        self.click_element_extended(locator, timeout, error_msg)
        BuiltIn.sleep(bi(), sleep, reason)

    def import_xpath2(self):
        s2l().execute_javascript(self.XPATH2_JS)

    def import_jQuery(self):
        s2l().execute_javascript(self.JQUERY_JS)
