#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
from Selenium2Library import Selenium2Library
from robot.libraries import DateTime
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot_instances import *
import os
import os.path


class Selenium2LibraryExtensions(object):
    WIDTH_DEFAULT = "1366"
    HEIGHT_DEFAULT = "768"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    SELENIUM_TIMEOUT = "5 s"
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

    def set_browser_size_and_position(self, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x=0, y=0):
        s2l().set_window_size(width, height)
        s2l().set_window_position(x, y)

    def go_to_smart(self, url):
        """Redirect only in on different url"""
        current_url = s2l().get_location()
        if url != current_url:
            s2l().go_to(url)

    def click_element_extended(self, locator, timeout=None, error_msg=None):
        """Click element proceed with following steps
        1.wait_until_page_contains_element
        2.wait_until_element_is_visible_wait_until_element_is_visible
        3.mouse_over"""
        s2l().wait_until_page_contains_element(locator, timeout, error_msg)
        s2l().wait_until_element_is_visible(locator, timeout, error_msg)
        s2l().mouse_over(locator)
        s2l().click_element(locator)

    def double_click_element_extended(self, locator, timeout=None, error=None):
        s2l().wait_until_page_contains_element(locator, timeout, error)
        s2l().wait_until_element_is_visible(locator, timeout, error)
        s2l().mouse_over(locator)
        s2l().double_click_element(locator)

    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error_msg=None, reason=None):
        self.click_element_extended(locator, timeout, error_msg)
        bi().sleep(sleep, reason)

    def open_browser_extension(self, url, browser="ff", width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x="0", y="0", alias=None, remote_url=False,
            desired_capabilities=None, ff_profile_dir=None, selenium_timeout=SELENIUM_TIMEOUT, keyword_to_run_on_failure="Capture Page Screenshot Extension"):
        s2l().open_browser(url, browser, alias, remote_url, desired_capabilities, ff_profile_dir)
        s2l().set_window_position(x, y)
        s2l().set_window_size(width, height)
        s2l().set_selenium_timeout(selenium_timeout)
        s2l().register_keyword_to_run_on_failure(keyword_to_run_on_failure)

    def import_xpath2(self):
        s2l().execute_javascript(self.XPATH2_JS)

    # noinspection PyPep8Naming,PyPep8Naming
    def import_jQuery(self):
        s2l().execute_javascript(self.JQUERY_JS)

    def capture_page_screenshot_extension(self, prefix="", postfix="", add_time_stamp=True, add_test_case_name=True,
            add_file_path_to_list="${list of screenshots}", output_dir="Screenshots"):
        output_dir_normalized = get_artifacts_dir(output_dir)

        if add_time_stamp:
            current_time = " " + DateTime.get_current_date(result_format="%Y.%m.%d_%H.%M.%S")
        else:
            current_time = ""
        if add_test_case_name:
            test_case_name = bi().get_variable_value("${TEST_NAME}")
        else:
            test_case_name = ""

        output_file = output_dir_normalized + "/" + prefix + test_case_name + postfix + current_time + ".png"
        output_file_normalized = os.path.normpath(output_file)

        s2l().capture_page_screenshot(output_file_normalized)

        results = bi().run_keyword_and_return_status("Variable Should Exist", add_file_path_to_list)

        if not results:
            list_with_files = bi().create_list(output_file_normalized)
            bi().set_test_variable(add_file_path_to_list, list_with_files)
        else:
            list_with_files = bi().create_list(output_file_normalized)
            list_with_files = bi().run_keyword("Combine Lists", add_file_path_to_list, list_with_files)
            bi().set_test_variable(add_file_path_to_list, list_with_files)

        return output_file_normalized
