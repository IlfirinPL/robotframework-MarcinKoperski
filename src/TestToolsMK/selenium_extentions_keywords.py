#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os
import os.path
import time

from robot.api import logger
from robot.libraries import DateTime
from selenium.webdriver import FirefoxProfile, ChromeOptions
from selenium.webdriver.common.keys import Keys

from TestToolsMK.robot_instances import validate_create_artifacts_dir, sl, bi

try:
    # noinspection PyCompatibility
    from urlparse import urljoin
except ImportError:  # python3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from urllib.parse import urljoin


# noinspection PyProtectedMember
class SeleniumLibraryKeywords(object):
    WIDTH_DEFAULT = "1366"
    HEIGHT_DEFAULT = "768"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    SELENIUM_TIMEOUT = "5 s"
    # noinspection PyPep8
    XPATH2_JS = 'if(!window.jQuery){var headID = document.getElementsByTagName("head")[0]; var newScript = document.createElement(\'script\'); newScript.type=\'text/javascript\'; newScript.src=\'http://llamalab.com/js/xpath/minified/XPath.js\'; headID.appendChild(newScript);}'
    # noinspection PyPep8
    JQUERY_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    @staticmethod
    def open_new_tab(url):
        """Hack it use Control +t to open new tab"""
        driver = sl().driver
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')
        time.sleep(2)
        sl().go_to(url)

    @staticmethod
    def switch_tab_by_id(id_tab):
        """Hack it use Control + 1,2,3 etc to switch tab"""
        driver = sl().driver
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + id_tab)
        time.sleep(4)
        # actions = ActionChains(driver)
        # actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()

    @staticmethod
    def press_key_python(command, locator="//body", strategy="XPATH"):
        """Hack !!!  example argument | Keys.CONTROL + 't' |Keys.TAB + Keys.SHIFT"""
        driver = sl().driver
        element = driver.find_element(eval("By." + strategy), locator)
        element.send_keys(eval(command))

    @staticmethod
    def close_tab():
        """Hack it use Control +w to close tab"""
        driver = sl().driver
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 'w')

    @staticmethod
    def set_browser_size_and_position(width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x=0, y=0):
        sl().set_window_size(width, height)
        sl().set_window_position(x, y)

    @staticmethod
    def go_to_smart(url):
        """Redirect only in on different url"""
        current_url = sl().get_location()
        if url != current_url:
            sl().go_to(url)

    @staticmethod
    def click_element_extended(locator, modifier=False, action_chain=False, timeout=None, error_msg=None):
        """
        Click element proceed with following steps
        * wait_until_page_contains_element
        * wait_until_element_is_visible_wait_until_element_is_visible
        * scroll_element_into_view
        * mouse_over
        * click_element

        """
        sl().wait_until_page_contains_element(locator, timeout, error_msg)
        sl().wait_until_element_is_visible(locator, timeout, error_msg)
        sl().scroll_element_into_view(locator)
        sl().mouse_over(locator)
        sl().click_element(locator, modifier=modifier, action_chain=action_chain)

    @staticmethod
    def double_click_element_extended(locator, modifier=False, action_chain=False, timeout=None, error=None):
        """
        Double Click element proceed with following steps
        * wait_until_page_contains_element
        * wait_until_element_is_visible_wait_until_element_is_visible
        * scroll_element_into_view
        * mouse_over
        * double_click_element
        """
        sl().wait_until_page_contains_element(locator, timeout, error)
        sl().wait_until_element_is_visible(locator, timeout, error)
        sl().scroll_element_into_view(locator)
        sl().mouse_over(locator)
        sl().double_click_element(locator, modifier=modifier, action_chain=action_chain)

    def click_element_extended_and_wait(self, locator, sleep, modifier=False, action_chain=False, timeout=None, error_msg=None, reason=None):
        self.click_element_extended(locator, timeout, error_msg)
        bi().sleep(sleep, reason)

    @staticmethod
    def open_browser_extension(url, browser="ff", width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x="0", y="0", alias=None, remote_url=False,
                               desired_capabilities=None, ff_profile_dir=None, selenium_timeout=SELENIUM_TIMEOUT, keyword_to_run_on_failure="Capture Page Screenshot Extension"):
        sl().open_browser("about:blank", browser, alias,
                          remote_url, desired_capabilities, ff_profile_dir)
        sl().set_window_position(x, y)
        sl().set_window_size(width, height)
        sl().set_selenium_timeout(selenium_timeout)
        sl().register_keyword_to_run_on_failure(keyword_to_run_on_failure)
        sl().go_to(url)

    def import_xpath2(self):
        sl().execute_javascript(self.XPATH2_JS)

    # noinspection PyPep8Naming,PyPep8Naming
    def import_jQuery(self):
        sl().execute_javascript(self.JQUERY_JS)

    # noinspection PyProtectedMember
    @staticmethod
    def capture_page_screenshot_extension(prefix="", postfix="", add_time_stamp=True, add_test_case_name=True, add_file_path_to_list="${list of screenshots}",
                                          output_dir="Artifacts/Screenshots"):
        output_dir_normalized = validate_create_artifacts_dir(output_dir)

        if add_time_stamp:
            current_time = " " + \
                DateTime.get_current_date(result_format="%Y.%m.%d_%H.%M.%S")
        else:
            current_time = ""
        if add_test_case_name:
            test_case_name = bi().get_variable_value("${TEST_NAME}")
        else:
            test_case_name = ""

        output_file = output_dir_normalized + "/" + prefix + \
            test_case_name + postfix + current_time + ".png"
        output_file_normalized = os.path.normpath(output_file)

        # sl()driver.get_screenshot_as_file(output_file_normalized)
        sl().capture_page_screenshot(output_file_normalized)

        results = bi().run_keyword_and_return_status(
            "Variable Should Exist", add_file_path_to_list)

        if not results:
            bi()._get_var_name(add_file_path_to_list)
            list_with_files = bi().create_list(output_file_normalized)
            bi().set_test_variable(add_file_path_to_list, list_with_files)
        else:
            list_with_files = bi().create_list(output_file_normalized)
            list_with_files = bi().run_keyword(
                "Combine Lists", add_file_path_to_list, list_with_files)
            bi().set_test_variable(add_file_path_to_list, list_with_files)

        return output_file_normalized

    @staticmethod
    def element_attribute_should_be(locator, attribute, attribute_value_expected, msg=None, values=True):
        actual_value = sl().get_element_attribute(locator + "@" + attribute)
        # noinspection PyProtectedMember
        actual_value, attribute_value_expected = [bi()._convert_to_string( i) for i in (actual_value, attribute_value_expected)]
        bi()._should_be_equal(actual_value, attribute_value_expected, msg, values)

    # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
    @staticmethod
    def create_download_dir_profile_for_firefox(path_to_download, mime_types_file=None, *extensions_files):
        """
        Example use
        | ${profile} | Create Download Dir Profile For Firefox | Artifacts | Resources/mimeTypes.rdf | Resources/webdriver_element_locator-2.0-fx.xpi | Resources/selenium_ide-2.9.1-fx.xpi |
        | Open Browser Extension | https://support.spatialkey.com/spatialkey-sample-csv-data/ | ff_profile_dir=${profile} |
        | Click Element | //a[contains(@href,'sample.csv.zip')]  |
        """
        path_to_download_check = validate_create_artifacts_dir(
            path_to_download)

        fp = FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
        fp.set_preference("browser.download.dir", path_to_download_check)
        fp.set_preference("xpinstall.signatures.required", False)
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "application/msword;application/csv;text/csv;image/png;image/jpeg;application/pdf;text/html;text/plain;application/octet-stream")
        fp.set_preference("pdfjs.disabled", True)
        fp.update_preferences()
        for single_extension in extensions_files:
            fp.add_extension(single_extension)
        if mime_types_file is not None:
            mime_types_file = os.path.abspath(mime_types_file)
            from shutil import copy2
            copy2(os.path.normpath(mime_types_file), fp.profile_dir)
        logger.info("Firefox Profile Created in dir '" + fp.profile_dir + "'")
        return fp.profile_dir

    # noinspection SpellCheckingInspection,SpellCheckingInspection
    @staticmethod
    def create_download_dir_capabilities_for_chrome(path_to_download, **extensions_files):
        """
        Example use
        | ${capabilities} |	create_download_dir_capabilities_for_chrome	| Artifacts |
        | Open Browser Extension | https://support.spatialkey.com/spatialkey-sample-csv-data/ |	gc | desired_capabilities=${capabilities} |
        | Click Element	 | //a[contains(@href,'sample.csv.zip')] |
        """

        path_to_download_check = validate_create_artifacts_dir(
            path_to_download)

        chrome_options = ChromeOptions()
        prefs = {"download.default_directory": path_to_download_check,
                 "directory_upgrade": "true"}

        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-web-security")
        for single_extension in extensions_files:
            chrome_options.add_extension(single_extension)

        logger.info("Chrome Capabilities set download dir '" +
                    path_to_download_check + "'")
        return chrome_options.to_capabilities()
