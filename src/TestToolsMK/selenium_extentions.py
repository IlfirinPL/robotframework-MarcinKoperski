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
    WIDTH_DEFAULT = "1920"
    HEIGHT_DEFAULT = "1200"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    XPATH2_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    def __int__(self):
        temp = self.s2l(self)

    # def __init__(self, timeout=5.0, implicit_wait=0.0, run_on_failure='Capture Page Screenshot'):
    #     for base in Selenium2LibraryExtensions.__bases__:
    #         if hasattr(base,'__init__'):
    #             base.__init__(self)

    @property
    def s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def open_browser_custom_size(self, url, width=WIDTH_DEFAULT, heigh=HEIGHT_DEFAULT, alias=None,
                                 browser=SELENIUM_TEST_BROWSER, remote_url=False, desired_capabilities=None):
        self.s2l.open_browser(self.s2l, browser, alias, remote_url,
                                            desired_capabilities)
        self.s2l.set_window_size(self.s2l, width, heigh)
        self.s2l.set_selenium_speed(self.s2l, self.s2l.SELENIUM_SPEED)
        # add handling rally screenshots

    def click_element_extended(self, locator, timeout=None, error=None):
        self.s2l.wait_until_page_contains_element(self, locator, timeout, error)
        self.s2l.wait_until_element_is_visible(self, locator, timeout, error)
        self.s2l.mouse_over(self, locator)
        self.s2l.click_element(self.locator)

    def double_click_element_extended(self, locator, timeout=None, error=None):
        self.s2l.wait_until_page_contains_element(self, locator, timeout, error)
        self.s2l.wait_until_element_is_visible(self, locator, timeout, error)
        self.s2l.mouse_over(self, locator)
        self.s2l.double_click_element(self.locator)

    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error=None, reason=None):
        self.click_element_extended(self, locator, timeout, error)
        BuiltIn.sleep(self, sleep, reason)

    def import_xpath2(self):
        self.s2l.execute_javascript(self, self.XPATH2_JS)
