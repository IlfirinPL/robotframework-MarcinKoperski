#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski

from datetime import datetime

from robot.api import logger
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.utils import (is_falsy)


def get_current_time_for_timers():
    return datetime.now()


class TimerKeywords(Time, Date):
    TIMERS_DICTIONARY = {}

    def timer_start(self, timer_name="Global"):
        current_time = get_current_time_for_timers()
        logger.info(current_time)
        if timer_name in self.TIMERS_DICTIONARY:
            error = "Timer with name \"%s\" already stated at %s" % (timer_name, self.TIMERS_DICTIONARY[timer_name].__str__())
            logger.warn(error)
        self.TIMERS_DICTIONARY[timer_name] = current_time
        msg = "Timer with name \"%s\" stated at %s" % (timer_name, self.TIMERS_DICTIONARY[timer_name].__str__())
        logger.info(msg)

    def timer_stop(self, timer_name="Global", result_format="number", exclude_millis="True"):
        current_time = get_current_time_for_timers()
        if timer_name not in self.TIMERS_DICTIONARY:
            message = "Time '%s' is not started." % timer_name
            raise AssertionError(message)
        else:
            delta = Time(current_time - self.TIMERS_DICTIONARY[timer_name]).convert(result_format, millis=is_falsy(exclude_millis))
            del self.TIMERS_DICTIONARY[timer_name]
            return delta

    def timer_restart(self, timer_name="Global", result_format="number", exclude_millis="True"):
        time_results = self.timer_stop(timer_name, result_format, exclude_millis)
        self.timer_start(timer_name)
        return time_results

    def timer_log(self, timer_name="Global", log_level="INFO", result_format="number", exclude_millis="True"):
        current_time = get_current_time_for_timers()
        if timer_name not in self.TIMERS_DICTIONARY:
            message = "Time '%s' is not started." % timer_name
            raise AssertionError(message)
        else:
            delta = Time(current_time - self.TIMERS_DICTIONARY[timer_name]).convert(result_format, millis=is_falsy(exclude_millis))
            msg = "Timer \"%s\" current results is %s" % (
                timer_name, Time(current_time - self.TIMERS_DICTIONARY[timer_name]).convert("verbose", millis=is_falsy(exclude_millis)))
            logger.write(msg, log_level)
            return delta

    def timer_should_be_lesser_then(self, expected_time, timer_name="Global"):
        if timer_name not in self.TIMERS_DICTIONARY:
            message = "Time '%s' is not started." % timer_name
            raise AssertionError(message)
        else:
            delta = get_current_time_for_timers() - self.TIMERS_DICTIONARY[timer_name]
            delta = Time._convert_time_to_seconds(self, delta)
            expected_time = Time._convert_time_to_seconds(self, expected_time)
            if delta > expected_time:
                message = "Timer '%s' is above expected time. Actual time %s > %s expected time " % (timer_name, delta, expected_time)
                raise AssertionError(message)
            return delta
