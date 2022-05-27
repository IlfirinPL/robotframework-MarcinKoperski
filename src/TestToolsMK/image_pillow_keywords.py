#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

import os
import os.path


from robot.api import logger

from PIL import Image, ImageChops, ImageStat, ImageOps

from robot.api.deco import keyword, library

from urllib.parse import urljoin
from urllib.request import pathname2url


@library
class ImagePillowKeywords(object):
    @staticmethod
    def _count_non_black_pil(img):
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
        embedded_gif=True,
        embedded_delta=False,
    ):
        file_1 = os.path.normpath(file_1_path)
        file_2 = os.path.normpath(file_2_path)

        if delta_file_path is not None:
            delta_file = os.path.normpath(delta_file_path)
        else:
            delta_file_path = (
                "./"
                + os.path.splitext(os.path.basename(file_1))[0]
                + "_"
                + os.path.splitext(os.path.basename(file_2))[0]
                + "_delta.png"
            )
            delta_file = os.path.normpath(delta_file_path)

        if gif_file_path is not None:
            gif_file = os.path.normpath(gif_file_path)
        else:
            gif_file_path = (
                "./"
                + os.path.splitext(os.path.basename(file_1))[0]
                + "_"
                + os.path.splitext(os.path.basename(file_2))[0]
                + ".gif"
            )
            gif_file = os.path.normpath(gif_file_path)
        if os.path.isfile(file_1) and os.path.isfile(file_2):

            img1 = Image.open(file_1)
            img2 = Image.open(file_2)

            # finding difference
            diff = ImageChops.difference(img1, img2)

            diff.save(delta_file)

            inverted_image = ImageOps.invert(diff)

            inverted_image.save(delta_file_path)

            nonblack = self._count_non_black_pil(diff)
            total = ImageStat.Stat(diff).count[0]

            delta_percent = nonblack * 100 / total

            if gif_file_path is not None:
                self.create_gif_from_three_files(
                    gif_file,
                    file_1,
                    file_2,
                    delta_file,
                    embedded=embedded_gif,
                )
            if delta_file_path is None:
                os.remove(delta_file)
            else:
                if embedded_delta:
                    self._embed_screenshot(delta_file)

            return (
                delta_percent,
                delta_file,
                gif_file,
            )

    @keyword
    def compare_image_files(
        self,
        file_1_path,
        file_2_path,
        gif_file_path=None,
        delta_file_path=None,
        embedded_gif=True,
        embedded_delta=False,
    ):
        results = self._compare_image_files(
            file_1_path,
            file_2_path,
            gif_file_path,
            delta_file_path,
            embedded_gif,
            embedded_delta,
        )

        return results[0]

    @keyword
    def image_should_be_difference_less_then(
        self,
        file_1_path,
        file_2_path,
        difference_percent=1,
        gif_file_path=None,
        delta_file_path=None,
        embedded_gif=True,
        embedded_delta=False,
    ):
        """difference_percent test to 0 mean both images are identical"""
        results = self._compare_image_files(
            file_1_path,
            file_2_path,
            gif_file_path,
            delta_file_path,
            embedded_gif=embedded_gif,
            embedded_delta=embedded_delta,
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

    @keyword
    def create_gif_from_three_files(
        self,
        gif_file_path,
        file_1_path,
        file_2_path,
        file_3_path,
        delay_ms=500,
        loop=0,
        embedded=True,
    ):
        files_list = [file_1_path, file_2_path, file_3_path]
        self.create_gif_from_list_of_files(
            gif_file_path, files_list, delay_ms, loop, embedded
        )

    @keyword
    def create_gif_from_list_of_files(
        self, gif_file_path, list_of_files, delay_ms=500, loop=0, embedded=True
    ):
        images = []
        for file in list_of_files:
            temp = Image.open(file)
            images.append(temp)

        images[0].save(
            gif_file_path,
            save_all=True,
            append_images=images,
            duration=delay_ms,
            loop=loop,
        )
        if embedded:
            self._embed_screenshot(gif_file_path)

    @staticmethod
    def _embed_screenshot(path, level="INFO", width="1200px"):
        link = urljoin("file:", pathname2url(os.path.normpath(path)))
        logger.write(
            '</td></tr><tr><td colspan="3"><a href="%s"><img src="%s" width="%s"></a>'
            % (link, link, width),
            level,
            html=True,
        )
