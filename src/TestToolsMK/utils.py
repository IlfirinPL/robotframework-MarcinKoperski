#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
import json
import os
import os.path
import platform
import subprocess
import urllib

from TestToolsMK.robot_instances import osl

try:
    # noinspection PyCompatibility
    from urlparse import urljoin
except ImportError:  # python3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from urllib.parse import urljoin

from robot.api import logger


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class UtilsKeywords(object):
    @property
    def get_latest_chrome_driver_version(self):
        return urllib.urlopen('http://chromedriver.storage.googleapis.com/LATEST_RELEASE').read().strip()

    @property
    def get_latest_firefox_driver_version(self):
        json_raw = urllib.urlopen('https://api.github.com/repos/mozilla/geckodriver/releases/latest').read().strip()
        json_data = json.loads(json_raw)
        return json_data["tag_name"].strip()

    @property
    def get_url_for_latest_chrome_driver(self):
        last_build = self.get_latest_chrome_driver_version
        try:
            base_url_for_driver = "http://chromedriver.storage.googleapis.com/" + last_build + "/"
            if platform.system() == "Windows":
                return base_url_for_driver + "chromedriver_win32.zip"
            if platform.system() == "Linux":
                return base_url_for_driver + "chromedriver_linux64.zip"

        except os.error as e:
            logger.warn("Unexpected error" + e)
            return "missing"

    @property
    def get_url_for_latest_firefox_driver(self):
        last_build = self.get_latest_firefox_driver_version
        try:
            base_url_for_driver = "https://github.com/mozilla/geckodriver/releases/download/" + last_build + "/"
            if platform.system() == "Windows":
                return base_url_for_driver + "geckodriver-" + last_build + "-win64.zip"
            if platform.system() == "Linux":
                return base_url_for_driver + "geckodriver-" + last_build + "-linux64.tar.gz"

        except os.error as e:
            logger.warn("Unexpected error" + e)
            return "missing"


    def get_chrome_driver_latest(self, path='./bin'):
        """
        Download Latest Chrome Driver and add it to system path (only for this session).
        If system already contains proper version do nothing.
        Based on information from http://chromedriver.storage.googleapis.com/LATEST_RELEASE
        """
        try:
            initial = osl().get_environment_variable("PATH")
            path_abstract = os.path.abspath(path)
            if (path_abstract not in initial):
                osl().set_environment_variable("PATH", path_abstract + os.pathsep + initial)

            try:
                version = subprocess.check_output(["chromedriver", "--version"], shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                version = "Chrome driver is MISSING "

            version_current = version.strip()
            version_latest = self.get_latest_chrome_driver_version
            url_chrome = self.get_url_for_latest_chrome_driver
            logger.debug("Current version \t" + version_current)
            logger.debug("Latest version :\t" + version_latest)
            if (version_latest not in version_current):
                logger.info("Current version %s , latest is %s" % (version_current, version_latest))

                logger.info("start download chrome driver :" + url_chrome)

                driver = urllib.urlopen(url_chrome).read()
                logger.debug("Chrome driver compressed size: " + sizeof_fmt(len(driver)))

                from zipfile import ZipFile
                from io import BytesIO
                with ZipFile(BytesIO(driver)) as zfile:
                    zfile.extractall(path_abstract)
                logger.info("Chrome driver extracted to : " + path_abstract)

            else:
                logger.info("Latest Version of ChromeDriver Present %s , latest %s" % (version_current, version_latest))

        except KeyError as e:
            logger.error(e)
        except OSError as e:
            logger.error(e)

    def get_firefox_driver_latest(self, path='./bin'):
        """
        Download Latest Firefox geckodriver Driver and add it to system path (only for this session).
        If system already contains proper version do nothing.
        Based on information from https://api.github.com/repos/mozilla/geckodriver/releases/latest
        """
        try:
            initial = osl().get_environment_variable("PATH")
            path_abstract = os.path.abspath(path)
            if (path_abstract not in initial):
                osl().set_environment_variable("PATH", path_abstract + os.pathsep + initial)

            try:
                version = subprocess.check_output(["geckodriver", "--version"], shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                version = "Firefox geckodriver driver is MISSING "

            version_current = version.strip()
            version_latest = self.get_latest_firefox_driver_version.replace("v", "").strip()
            url_firefox = self.get_url_for_latest_firefox_driver
            logger.debug("Current version \t" + version_current)
            logger.debug("Latest version :\t" + version_latest)
            if (version_latest not in version_current):
                logger.info("Current version %s , latest is %s" % (version_current, version_latest))

                logger.info("start download firefox geckodriver driver :" + url_firefox)

                driver = urllib.urlopen(url_firefox).read()
                logger.debug("Firefox geckodriver driver compressed size: " + sizeof_fmt(len(driver)))

                from zipfile import ZipFile
                from io import BytesIO
                with ZipFile(BytesIO(driver)) as zfile:
                    zfile.extractall(path_abstract)
                logger.info("Chrome driver extracted to : " + path_abstract)

            else:
                logger.info("Latest Version of Firefox geckodriver Present %s , latest %s" % (version_current, version_latest))

        except KeyError as e:
            logger.error(e)
        except OSError as e:
            logger.error(e)
