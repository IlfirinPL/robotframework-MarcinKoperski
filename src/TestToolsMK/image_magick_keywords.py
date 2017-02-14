#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

import os
import os.path
import platform
import subprocess

try:
    # noinspection PyCompatibility
    from urlparse import urljoin
except ImportError:  # python3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from urllib.parse import urljoin

import urllib
from robot.api import logger


class ImageMagickKeywords(object):
    def __init__(self):
        if os.path.isfile(self.get_convert_path):
            logger.debug("Convert file exits path, path used :" + self.get_convert_path)
        else:
            message = "Missing file convert.exe"
            logger.debug(message)

        if os.path.isfile(self.get_compare_path):
            logger.debug("Compare file exits , path used :" + self.get_compare_path)
        else:
            message = "Missing file compare.exe"
            logger.debug(message)

        if os.path.isfile(self.get_identify_path):
            logger.debug("Identify file exits, path used :" + self.get_identify_path)
        else:
            message = "Missing file identify.exe"
            logger.debug(message)

    @property
    def get_magick_home(self):
        try:
            if platform.system() == "Windows":
                return os.environ['MAGICK_HOME']
            if platform.system() == "Linux":
                return "/usr/bin/"

        except os.error as e:
            message = "Missing system variable 'MAGICK_HOME'" + e
            logger.warn(message)
            return message

    @property
    def get_compare_path(self):
        try:
            if platform.system() == "Windows":
                return os.path.normpath(self.get_magick_home + "\\" + "compare.exe")
            if platform.system() == "Linux":
                return os.path.normpath("/usr/bin/compare")
        except os.error as e:
            logger.warn("Missing file compare" + e)
            return "missing"

    @property
    def get_identify_path(self):
        try:
            if platform.system() == "Windows":
                return os.path.normpath(self.get_magick_home + "\\" + "identify.exe")
            if platform.system() == "Linux":
                return os.path.normpath("/usr/bin/identify")

        except os.error as e:
            logger.warn("Missing file identify" + e)
            return "missing"

    @property
    def get_convert_path(self):
        try:
            if platform.system() == "Windows":
                return os.path.normpath(self.get_magick_home + "\\" + "convert.exe")
            if platform.system() == "Linux":
                return os.path.normpath("/usr/bin/convert")

        except os.error as e:
            logger.warn("Missing file convert.exe" + e)
            return "missing"

    def image_self_check(self):
        if os.path.isfile(self.get_convert_path):
            logger.info("Convert file exits path, path used :" + self.get_convert_path)
        else:
            message = "Missing file convert.exe"
            raise AssertionError(message)

        if os.path.isfile(self.get_compare_path):
            logger.info("Compare file exits , path used :" + self.get_compare_path)
        else:
            message = "Missing file compare.exe"
            raise AssertionError(message)

        if os.path.isfile(self.get_identify_path):
            logger.info("Identify file exits, path used :" + self.get_identify_path)
        else:
            message = "Missing file identify.exe"
            raise AssertionError(message)

        argument_list = [self.get_convert_path, "--version"]
        try:
            procces = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , shell=True
            procces.wait()
            output = procces.communicate()
            logger.info("returnCode \t:" + str(procces.returncode))
            if procces.returncode != 0:
                message = "processing failed msg= %s" % str(output)
                raise AssertionError(message)
            logger.info("stdout \t:" + str(output[0]))
            logger.info("stderr \t:" + str(output[1]))

        except OSError as e:
            logger.error(e)

    def _compare_image_files(self, file_1_path, file_2_path, gif_file_path=None, delta_file_path=None, metric="RMSE", embedded_gif=True, embedded_delta=False,
            force_resize=True):
        file_1_path_normalized = os.path.normpath(file_1_path)
        file_2_path_normalized = os.path.normpath(file_2_path)

        if force_resize:
            file_1_width, file_1_height = self._get_info_for_image(file_1_path_normalized)
            self._resize_file(file_2_path_normalized, file_1_width, file_1_height)
        if delta_file_path is not None:
            delta_file_path_normalized = os.path.normpath(delta_file_path)
        else:
            delta_file_path = os.path.dirname(file_1_path_normalized) + "\\" + os.path.splitext(os.path.basename(file_1_path_normalized))[0] + "_" + \
                              os.path.splitext(os.path.basename(file_2_path_normalized))[0] + "_delta.png"
            delta_file_path_normalized = os.path.normpath(delta_file_path)

        if gif_file_path is not None:
            gif_file_path_normalized = os.path.normpath(gif_file_path)
        else:
            gif_file_path = os.path.dirname(file_1_path_normalized) + "\\" + os.path.splitext(os.path.basename(file_1_path_normalized))[0] + "_" + \
                            os.path.splitext(os.path.basename(file_2_path_normalized))[0] + ".gif"
            gif_file_path_normalized = os.path.normpath(gif_file_path)
        if os.path.isfile(file_1_path_normalized) and os.path.isfile(file_2_path_normalized):
            argument_list = [self.get_compare_path, "-metric", metric, file_1_path_normalized, file_2_path_normalized, delta_file_path_normalized]
            process = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            output = process.communicate()
            if "error" in str(output):
                message = "processing failed msg= %s" % str(output)
                raise AssertionError(message)

            delta_percent = output[1].split("(")[1].replace(")", "")

            if gif_file_path is not None:
                self.create_gif_from_three_files(gif_file_path_normalized, file_1_path_normalized, file_2_path_normalized, delta_file_path_normalized,
                    embedded=embedded_gif)
            if delta_file_path is None:
                todo = True
                # TODO maybe remove files
            else:
                if embedded_delta:
                    self._embed_screenshot(delta_file_path_normalized)

            return float(delta_percent) * float(100), delta_file_path_normalized, gif_file_path_normalized

    def compare_image_files(self, file_1_path, file_2_path, gif_file_path=None, delta_file_path=None, metric="RMSE", embedded_gif=True, embedded_delta=False,
            force_resize=True):
        results = self._compare_image_files(file_1_path, file_2_path, gif_file_path, delta_file_path, metric, embedded_gif, embedded_delta, force_resize)

        return results[0]

    def image_should_be_difference_less_then(self, file_1_path, file_2_path, difference_percent=1, gif_file_path=None, delta_file_path=None, embedded_gif=True,
            embedded_delta=False, force_resize=True):
        """difference_percent test to 0 mean both images are identical """
        results = self._compare_image_files(file_1_path, file_2_path, gif_file_path, delta_file_path, embedded_gif=embedded_gif, embedded_delta=embedded_delta,
            force_resize=force_resize)
        if float(results[0]) > float(difference_percent):
            message = "Difference between files is greater then expected actual %.2f > %.2f expected percent" % (float(results[0]), float(difference_percent))
            raise AssertionError(message)
        else:
            logger.info("Image check successful ")
        return results[0]

    def create_gif_from_three_files(self, gif_file_path, file_1_path, file_2_path, file_3_path, delay_ms=100, loop=0, embedded=True):
        files_list = [file_1_path, file_2_path, file_3_path]
        self.create_gif_from_list_of_files(gif_file_path, files_list, delay_ms, loop, embedded)

    def create_gif_from_list_of_files(self, gif_file_path, files_list_path, delay_ms=100, loop=0, embedded=True):
        files_list_path_normalized = []
        for singleFile in files_list_path:
            files_list_path_normalized.append(os.path.normpath(singleFile))
        gif_file_path_normalized = os.path.normpath(gif_file_path)
        if all(os.path.isfile(singleFile) == True for singleFile in files_list_path_normalized):
            argument_list = [self.get_convert_path, "-delay", str(delay_ms), "-loop", str(loop)]
            argument_list.extend(files_list_path_normalized)
            argument_list.append(gif_file_path_normalized)
            process = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            if embedded:
                self._embed_screenshot(gif_file_path_normalized)

        else:
            message = "Gif Creation failed."
            for singleFile in files_list_path_normalized:
                if os.path.isfile(singleFile):
                    message += "File missing %s." % singleFile
            raise AssertionError(message)

    @staticmethod
    def _embed_screenshot(path, level="INFO", width="1200px"):
        link = urljoin('file:', urllib.pathname2url(os.path.normpath(path)))
        logger.write('</td></tr><tr><td colspan="3"><a href="%s"><img src="%s" width="%s"></a>' % (link, link, width), level, html=True)

    def _get_info_for_image(self, file_name):
        argument_list = [self.get_identify_path, "-quiet", "-format", "%[fx:w]\\n%[fx:h]", file_name]
        try:
            procces = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , shell=True
            procces.wait()
            output = procces.communicate()
            if procces.returncode != 0:
                message = "processing failed msg= %s" % str(output)
                raise AssertionError(message)

            # logger.info("file Name \t:" + file_name+str(output))
            table_results = output[0].split()
            return table_results[0], table_results[1]
        except OSError as e:
            logger.error(e)

    def _resize_file(self, file_path_normalized, width, height):
        if os.path.isfile(file_path_normalized):
            argument_list = [self.get_convert_path, "-resize", width + "x" + height + "!", file_path_normalized, file_path_normalized]
            process = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            output = process.communicate()
            if process.returncode != 0:
                message = "processing failed msg= %s" % str(output)
                raise AssertionError(message)
