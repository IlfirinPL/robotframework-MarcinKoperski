#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import json
import os
import os.path
import platform
import shlex
import subprocess
import urllib

import requests

from TestToolsMK.robot_instances import osl
import time

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


def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param port:
        @param server:
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    # noinspection PyGlobalUndefined,PyGlobalUndefined
    global end, now
    import socket
    import errno

    s = socket.socket()
    if timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout as err:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error as err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if type(err.args) != tuple or err[0] != errno.ETIMEDOUT:
                raise

        except:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if timeout:
                return False
        else:
            s.close()
            return True


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

            if path_abstract not in initial:
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
            if version_latest not in version_current:
                logger.info("Current version %s , latest is %s" % (version_current, version_latest))
                if not os.path.exists(path_abstract):
                    os.makedirs(path_abstract)
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

            if path_abstract not in initial:
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
            if version_latest not in version_current:
                logger.info("Current version %s , latest is %s" % (version_current, version_latest))

                logger.info("start download firefox geckodriver driver :" + url_firefox)
                if not os.path.exists(path_abstract):
                    os.makedirs(path_abstract)
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

    @staticmethod
    def get_selenium_server(url='https://goo.gl/lbAQcq', path='./bin/selenium-server.jar',
                            skip_if_already_exists="True"):
        """
        Currently hard coded as arg future change to download from https://selenium-release.storage.googleapis.com
        """
        dir_selenium = os.path.dirname(path)
        path = os.path.abspath(path)
        logger.debug("Folder to download " + dir_selenium)

        if not os.path.exists(dir_selenium):
            os.makedirs(dir_selenium)

        if skip_if_already_exists == "True":
            if os.path.exists(path):
                logger.info(
                    "Skip Selenium Server download already exists in path \"%s\" because skip_if_already_exists is set to \"%s\"" % (
                    path, skip_if_already_exists))
                return

        try:
            r = requests.head(url, allow_redirects=True)
            logger.info("Resolved url: \t" + r.url)
            testfile = urllib.URLopener()
            testfile.retrieve(r.url, path)
            logger.info("Selenium Server download completed to " + path)

        except KeyError as e:
            logger.error(e)
        except OSError as e:
            logger.error(e)

    def start_selenium_server(self, path='./bin/selenium-server.jar', timeout=60, port="4444", logs_path='./bin'):
        """
        :return:
        """
        path = os.path.abspath(path)

        with open(os.path.abspath(logs_path + "/selenium_server_stdout.txt"), "wb") as out, open(os.path.abspath(logs_path + "/selenium_server_stderr.txt"),
                "wb") as err:
            command = "java -jar \"" + path + "\" -port " + port
            logger.info("Command to start server :" + command)
            # noinspection PyAttributeOutsideInit
            self.selenium_server = subprocess.Popen(shlex.split(command), stdout=out, stderr=err)
        time.sleep(7)

    def shutdown_selenium_server(self):
        if self.selenium_server is not None :
            self.selenium_server.terminate()
            logger.info("Selenium Server shutdown")
        else:
            logger.error("Server not started")

