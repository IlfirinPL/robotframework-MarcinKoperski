#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import robot
from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import Selenium2Library

class Selenium2LibraryExtensions(object):
    TIMEOUT_LONG = "60 sec"
    TIMEOUT = "2 sec"
    WIDTH_DEFAULT = "1366"
    HEIGHT_DEFAULT = "768"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    XPATH2_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"
    JQUERY_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    def __init__(self, timeout=5.0, implicit_wait=0.0, run_on_failure='Capture Page Screenshot'):
        for base in Selenium2LibraryExtensions.__bases__:
            if hasattr(base, '__init__'):
                base.__init__(self)
        print "Selenium2LibraryExtensions loaded"

    @property
    def s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    @property
    def bi(self):
        return BuiltIn().get_library_instance('BuiltIn')

    def set_browser_size_and_position(self, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x=0, y=0):
        Selenium2Library.set_window_size(self.s2l, width, height)
        Selenium2Library.set_window_position(self.s2l, x, y)

    def go_to_smart(self, url):
        """Redirect only in on different url"""
        currentUrl = Selenium2Library.get_location(self.s2l)
        if url != currentUrl:
            Selenium2Library.get_location(self.s2l, url)

    def click_element_extended(self, locator, timeout=None, error=None):
        """Click element proceed with following steps
        1.wait_until_page_contains_element
        2.wait_until_element_is_visiblewait_until_element_is_visible
        3.mouse_over"""
        Selenium2Library.wait_until_page_contains_element(self.s2l, locator, timeout, error)
        Selenium2Library.wait_until_element_is_visible(self.s2l, locator, timeout, error)
        Selenium2Library.mouse_over(self.s2l, locator)
        Selenium2Library.click_element(self.s2l, locator)


    def double_click_element_extended(self, locator, timeout=None, error=None):
        Selenium2Library.wait_until_page_contains_element(self.s2l, locator, timeout, error)
        Selenium2Library.wait_until_element_is_visible(self.s2l, locator, timeout, error)
        Selenium2Library.mouse_over(self.s2l, locator)
        Selenium2Library.double_click_element(self.s2l, locator)


    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error=None, reason=None):
        Selenium2Library.click_element_extended(self.s2l, locator, timeout, error)
        BuiltIn.sleep(self.bi, sleep, reason)

    def import_xpath2(self):
        Selenium2Library.execute_javascript(self.s2l, self.XPATH2_JS)

    def import_jQuery(self):
        Selenium2Library.execute_javascript(self.s2l, self.JQUERY_JS)
