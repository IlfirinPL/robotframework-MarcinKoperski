#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski


class CollectionsKeywords(object):
    @staticmethod
    def create_dictionary_from_list(table):
        """

        :rtype : dict
        """
        return dict((x, 0) for x in table)

    @staticmethod
    def create_dictionary_from_two_lists(keys, values):
        """

        :rtype : dict
        """
        return dict(zip(keys, values))

    @staticmethod
    def sort_list_by_number(list_):
        """Sorts the given list in place.

        """
        list_.sort(key=float)
