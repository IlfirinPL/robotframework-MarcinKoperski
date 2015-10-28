#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import os
import re
import robot
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import subprocess
import os.path


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
        convertPath = os.path.normpath(os.environ['MAGICK_HOME'] + "\\" + "convert.exe")
        comparePath = os.path.normpath(os.environ['MAGICK_HOME'] + "\\" + "compare.exe")

        if os.path.isfile(convertPath):
            logger.info("Convert file exits")
        else:
            message = "Missing file convert.exe"
            raise AssertionError(message)

        if os.path.isfile(comparePath):
            logger.info("Compare file exits")
        else:
            message = "Missing file compare.exe"
            raise AssertionError(message)

        argument_list = [comparePath]
        try:
            procces = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , shell=True
            procces.wait()
            logger.info("returnCode \t:" + str(procces.returncode))
            logger.info("stdout \t:" + str(procces.communicate()[0]))
            logger.info("stderr \t:" + str(procces.communicate()[1]))

        except OSError, e:
            logger.error(e)
        except:
            logger.error("Last exception handler")

    def compare_image_files(self, file_1_path, file_2_path, delta_file_path=None, metric="RMSE"):
        file_1_path_normalized = os.path.normpath(file_1_path)
        file_2_path_normalized = os.path.normpath(file_2_path)
        if delta_file_path is not None:
            delta_file_path_normalized = os.path.normpath(delta_file_path)
        else:
            delta_file_path = os.path.dirname(file_1_path_normalized) + "\\delta_" + os.path.basename(file_1_path_normalized) + os.path.basename(
                file_2_path_normalized)
            delta_file_path_normalized = os.path.normpath(delta_file_path)
        if (os.path.isfile(file_1_path_normalized) and os.path.isfile(file_2_path_normalized)):
            argument_list = [self.COMPARE_PATH, "-metric", metric, file_1_path_normalized, file_2_path_normalized, delta_file_path_normalized]
            procces = subprocess.Popen(argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procces.wait()
            delta_percent = procces.communicate()[1].split("(")[1].replace(")", "")
            return float(delta_percent)

    def image_should_be_difference_less_then(self, file_1_path, file_2_path, difference_percent=1, delta_file_path=None):
        """difference_percent test to 0 mean both images are identical """
        results = self.compare_image_files(file_1_path, file_2_path, delta_file_path)

        difference_percent = float(difference_percent) / float(100)

        if results > difference_percent:
            message = "Difference between files is greater then expected actual %s > %s expected" % (results, difference_percent)
            raise AssertionError(message)
        else:
            logger.info("Image check successful ")
        return results
