#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

import os
import os.path
import platform
import subprocess


from urllib.parse import urljoin

import urllib
from robot.api import logger


class ImageMagickKeywords(object):

    def _count_nonblack_pil(img):
    """Return the number of pixels in img that are not black.
    img must be a PIL.Image object in mode RGB.

    """
    bbox = img.getbbox()
    if not bbox:
        return 0
    return sum(
        img.crop(bbox)
        .point(lambda x: 255 if x else 0)
        .convert("L")
        .point(bool)
        .getdata()
    )



    def _compare_image_files(
        self,
        file_1_path,
        file_2_path,
        gif_file_path=None,
        delta_file_path=None,
        metric="RMSE",
        embedded_gif=True,
        embedded_delta=False,
        force_resize=True,
    ):
        file_1_path_normalized = os.path.normpath(file_1_path)
        file_2_path_normalized = os.path.normpath(file_2_path)

        if force_resize:
            file_1_width, file_1_height = self._get_info_for_image(
                file_1_path_normalized
            )
            self._resize_file(file_2_path_normalized, file_1_width, file_1_height)
        if delta_file_path is not None:
            delta_file_path_normalized = os.path.normpath(delta_file_path)
        else:
            delta_file_path = (
                os.path.dirname(file_1_path_normalized)
                + "\\"
                + os.path.splitext(os.path.basename(file_1_path_normalized))[0]
                + "_"
                + os.path.splitext(os.path.basename(file_2_path_normalized))[0]
                + "_delta.png"
            )
            delta_file_path_normalized = os.path.normpath(delta_file_path)

        if gif_file_path is not None:
            gif_file_path_normalized = os.path.normpath(gif_file_path)
        else:
            gif_file_path = (
                os.path.dirname(file_1_path_normalized)
                + "\\"
                + os.path.splitext(os.path.basename(file_1_path_normalized))[0]
                + "_"
                + os.path.splitext(os.path.basename(file_2_path_normalized))[0]
                + ".gif"
            )
            gif_file_path_normalized = os.path.normpath(gif_file_path)
        if os.path.isfile(file_1_path_normalized) and os.path.isfile(
            file_2_path_normalized
        ):

            img1 = Image.open("1.png")
            img2 = Image.open("2.png")

            # finding difference
            diff = ImageChops.difference(img1, img2)

            diff.save("delta.png")

            inverted_image = ImageOps.invert(diff)

            inverted_image.save(delta_file_path)

            nonblack = count_nonblack_pil(diff)
            total = ImageStat.Stat(diff).count[0]

            delta_percent = nonblack * 100 / total

            if gif_file_path is not None:
                self.create_gif_from_three_files(
                    gif_file_path_normalized,
                    file_1_path_normalized,
                    file_2_path_normalized,
                    delta_file_path_normalized,
                    embedded=embedded_gif,
                )
            if delta_file_path is None:
                todo = True
                # TODO maybe remove files
            else:
                if embedded_delta:
                    self._embed_screenshot(delta_file_path_normalized)

            return (
                float(delta_percent) * float(100),
                delta_file_path_normalized,
                gif_file_path_normalized,
            )

    def compare_image_files(
        self,
        file_1_path,
        file_2_path,
        gif_file_path=None,
        delta_file_path=None,
        metric="RMSE",
        embedded_gif=True,
        embedded_delta=False,
        force_resize=True,
    ):
        results = self._compare_image_files(
            file_1_path,
            file_2_path,
            gif_file_path,
            delta_file_path,
            metric,
            embedded_gif,
            embedded_delta,
            force_resize,
        )

        return results[0]

    def image_should_be_difference_less_then(
        self,
        file_1_path,
        file_2_path,
        difference_percent=1,
        gif_file_path=None,
        delta_file_path=None,
        embedded_gif=True,
        embedded_delta=False,
        force_resize=True,
    ):
        """difference_percent test to 0 mean both images are identical"""
        results = self._compare_image_files(
            file_1_path,
            file_2_path,
            gif_file_path,
            delta_file_path,
            embedded_gif=embedded_gif,
            embedded_delta=embedded_delta,
            force_resize=force_resize,
        )
        if float(results[0]) > float(difference_percent):
            message = (
                "Difference between files is greater then expected actual %.2f > %.2f expected percent"
                % (float(results[0]), float(difference_percent))
            )
            raise AssertionError(message)
        else:
            logger.info("Image check successful ")
        return results[0]

    def create_gif_from_three_files(
        self,
        gif_file_path,
        file_1_path,
        file_2_path,
        file_3_path,
        delay_ms=100,
        loop=0,
        embedded=True,
    ):
        files_list = [file_1_path, file_2_path, file_3_path]
        self.create_gif_from_list_of_files(
            gif_file_path, files_list, delay_ms, loop, embedded
        )

    def create_gif_from_list_of_files(
        self, gif_file_path, files_list_path, delay_ms=500, loop=0, embedded=True
    ):
        files_list_path_normalized = []
        for singleFile in files_list_path:
            files_list_path_normalized.append(os.path.normpath(singleFile))
        gif_file_path_normalized = os.path.normpath(gif_file_path)
        img1.save(
        gif_file_path,
        save_all=True,
        append_images=files_list_path,
        duration=delay_ms,
        loop=loop,
        )


    @staticmethod
    def _embed_screenshot(path, level="INFO", width="1200px"):
        link = urljoin("file:", urllib.pathname2url(os.path.normpath(path)))
        logger.write(
            '</td></tr><tr><td colspan="3"><a href="%s"><img src="%s" width="%s"></a>'
            % (link, link, width),
            level,
            html=True,
        )

    def _get_info_for_image(self, file_name):
        argument_list = [
            self.get_identify_path,
            "-quiet",
            "-format",
            "%[fx:w]\\n%[fx:h]",
            file_name,
        ]
        try:
            procces = subprocess.Popen(
                argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )  # , shell=True
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
            argument_list = [
                self.get_convert_path,
                "-resize",
                width + "x" + height + "!",
                file_path_normalized,
                file_path_normalized,
            ]
            process = subprocess.Popen(
                argument_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            process.wait()
            output = process.communicate()
            if process.returncode != 0:
                message = "processing failed msg= %s" % str(output)
                raise AssertionError(message)
