#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import io
import os
import time
import re
import collections
import calendar


from datetime import datetime, timedelta
import random, string
from random import randint

from TestToolsMK import robot_instances
from robot.api import logger
from robot.libraries import DateTime
from robot.utils import asserts

class PeselKeywords(object):
    def Pesel(self,date='20/12/1999',sex=''):
        """ Generate PSL for given birthdate DD/MM/YYYY and gender M - male, F - female, <empty> - random. """
        sex = sex.upper() 
        if sex != '' and sex != 'M' and sex != 'F':
            raise ValueError("Accepted values for gender: M or F or <empty>")
        dt = datetime.strptime(date,'%d/%m/%Y')
        y = str(dt.year)
        m = int(dt.month)
        d = int(dt.day)
        if int(dt.year) >= 2000:
            m = m + 20
        if int(dt.year) < 1900:
            m = m + 80
        psl01 = int(y[2])
        psl02 = int(y[3])
        if m <10:
            psl03 = 0
            psl04 = m
        else:
           temp = str(m)
           psl03 = int(temp[0])
           psl04 = int(temp[1])
        if d < 10:
           psl05 = 0
           psl06 = d
        else:
           tempo = str(d)
           psl05 = int(tempo[0])
           psl06 = int(tempo[1])
        psl07 = random.randrange(10)
        psl08 = random.randrange(10)
        psl09 = random.randrange(10)
        rand = random.randrange(10)
        if sex=='M':
            if rand%2==0:
                psl10 = rand+1
            else:
                psl10 = rand
        elif sex=='F':
            if rand%2==0:
                psl10 = rand
            else:
                psl10 = rand-1
        else:
            psl10 = rand
            if psl10 % 2 == 0:
                sex = 'F'  
            else:
                sex = 'M'
        rest = (psl01*1 + psl02*3 + psl03*7 + psl04*9 + psl05*1 + psl06*3 + psl07*7 + psl08*9 + psl09*1 + psl10*3) % 10
        if rest == 0:
            psl11 = 0
        else:
            psl11 = 10 - rest
        finalPSL =  str(psl01) + str(psl02) + str(psl03) + str(psl04) + str(psl05) + str(psl06) + str(psl07) + str(psl08) + str(psl09) + str(psl10) + str(psl11)
        return finalPSL
