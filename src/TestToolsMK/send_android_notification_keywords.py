#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import requests
from robot.api import logger


class SendNotificationKeywords(object):
    @staticmethod
    def send_notification_to_phone(msg, identifier):
        """
        To use its based on https://github.com/mashlol/notify
        link to android app (get identifier from this app)
        https://play.google.com/store/apps/details?id=com.kevinbedi.notify

        """
        params_to_send = {'to': identifier, 'text': msg}
        r = requests.get('https://us-central1-notify-b7652.cloudfunctions.net/sendNotification', params=params_to_send)

        logger.debug("Send Url:\t" + r.url)
        logger.debug("Response Url:\t" + r.text)
        if "\"success\":true" not in r.text:
            message = "Failed to send message err=%s" % r.text
            raise AssertionError(message)

        logger.info("Send Message \'" + msg + "\' to user with id " + identifier)
