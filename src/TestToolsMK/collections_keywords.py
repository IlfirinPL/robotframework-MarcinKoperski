#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski


from robot.api.deco import keyword, library


@library
class CollectionsKeywords(object):
    @keyword
    def create_dictionary_from_list(self, table):
        return dict((x, 0) for x in table)

    @keyword
    def create_dictionary_from_two_lists(self, keys, values):
        return dict(zip(keys, values))

    @keyword
    def sort_list_by_number(self, list):
        """Sorts the given list in place."""
        list.sort(key=float)
