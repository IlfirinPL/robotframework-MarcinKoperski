#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import robot
from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import Selenium2Library


class seleniumExtentions(object):
    TIMEOUT_LONG = "60 sec"
    TIMEOUT = "2 sec"
    WIDTH_DEFAULT = "1920"
    HEIGHT_DEFAULT = "1200"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    XPATH2_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    def __int__(self):
        SELENIUM_TEST_BROWSER = "ff"

    def open_browser_custom_size(self, url, width=WIDTH_DEFAULT, heigh=HEIGHT_DEFAULT, alias=None,
                                 browser=SELENIUM_TEST_BROWSER, remote_url=False, desired_capabilities=None):
        Selenium2Library.open_browser(self, url, browser, alias, remote_url, desired_capabilities)
        Selenium2Library.set_window_size(self, width, heigh)
        Selenium2Library.set_selenium_speed(self, self.SELENIUM_SPEED)
        # add handling rally screenshots

    def click_element_extended(self, locator, timeout=None, error=None):
        Selenium2Library.wait_until_page_contains_element(self, locator, timeout, error)
        Selenium2Library.wait_until_element_is_visible(self, locator, timeout, error)
        Selenium2Library.mouse_over(self, locator)
        Selenium2Library.click_element(self.locator)

    def double_click_element_extended(self, locator, timeout=None, error=None):
        Selenium2Library.wait_until_page_contains_element(self, locator, timeout, error)
        Selenium2Library.wait_until_element_is_visible(self, locator, timeout, error)
        Selenium2Library.mouse_over(self, locator)
        Selenium2Library.double_click_element(self.locator)

    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error=None, reason=None):
        self.click_element_extended(self, locator, timeout, error)
        BuiltIn.sleep(self, sleep, reason)

    def import_xpath2(self):
        Selenium2Library.execute_javascript(self, self.XPATH2_JS)
