#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import subprocess
import os.path
import urlparse
import urllib

from robot.api import logger


class ImageMagickKeywords(object):
    CONVERT_PATH = os.path.normpath(os.environ['MAGICK_HOME'] + "\\" + "convert.exe")
    COMPARE_PATH = os.path.normpath(os.environ['MAGICK_HOME'] + "\\" + "compare.exe")

    def image_self_check(self):
        try:
            os.environ['MAGICK_HOME']
        except:
            message = "Missing system variable 'MAGICK_HOME'"
            logger.error(message)
            raise AssertionError(message)

        if os.path.isfile(self.CONVERT_PATH):
            logger.info("Convert file exits")
        else:
            message = "Missing file convert.exe"
            raise AssertionError(message)

        if os.path.isfile(self.COMPARE_PATH):
            logger.info("Compare file exits")
        else:
            message = "Missing file compare.exe"
            raise AssertionError(message)

        argument_list = [self.CONVERT_PATH]
        try:
            procces = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , shell=True
            procces.wait()
            logger.info("returnCode \t:" + str(procces.returncode))
            logger.info("stdout \t:" + str(procces.communicate()[0]))
            logger.info("stderr \t:" + str(procces.communicate()[1]))

        except OSError, e:
            logger.error(e)

    def _compare_image_files(self, file_1_path, file_2_path, gif_file_path=None, delta_file_path=None, metric="RMSE", embedded_gif=True, embedded_delta=False):
        file_1_path_normalized = os.path.normpath(file_1_path)
        file_2_path_normalized = os.path.normpath(file_2_path)
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
            argument_list = [self.COMPARE_PATH, "-metric", metric, file_1_path_normalized, file_2_path_normalized, delta_file_path_normalized]
            process = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            delta_percent = process.communicate()[1].split("(")[1].replace(")", "")

            if gif_file_path is not None:
                self.create_gif_from_three_files(gif_file_path_normalized, file_1_path_normalized, file_2_path_normalized, delta_file_path_normalized,
                                                 embedded=embedded_gif)
            if delta_file_path is None:
                os.remove(delta_file_path_normalized)
            else:
                if embedded_delta:
                    self._embed_screenshot(delta_file_path_normalized)

            return float(delta_percent) * float(100), delta_file_path_normalized, gif_file_path_normalized

    def compare_image_files(self, file_1_path, file_2_path, gif_file_path=None, delta_file_path=None, metric="RMSE", embedded_gif=True, embedded_delta=False):
        return self._compare_image_files(file_1_path, file_2_path, gif_file_path, delta_file_path, metric, embedded_gif, embedded_delta)[0]

    def image_should_be_difference_less_then(self, file_1_path, file_2_path, difference_percent=1, gif_file_path=None, delta_file_path=None, embedded_gif=True,
                                             embedded_delta=False):
        """difference_percent test to 0 mean both images are identical """
        results = self._compare_image_files(file_1_path, file_2_path, gif_file_path, delta_file_path, embedded_gif=embedded_gif, embedded_delta=embedded_delta)
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
            argument_list = [self.CONVERT_PATH, "-delay", str(delay_ms), "-loop", str(loop)]
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
    def _embed_screenshot(path, level="INFO", width="800px"):
        link = urlparse.urljoin('file:', urllib.pathname2url(os.path.normpath(path)))
        logger.write('<a href="%s"><img src="%s" width="%s"></a>' % (link, link, width), level, html=True)
