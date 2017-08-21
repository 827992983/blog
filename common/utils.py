#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Abel Lee
# date: 2017
#Copyright: free

import uuid
import datetime
import time

def uuid1():
    return str(uuid.uuid1())

# '2015-08-28 16:43:37.283' --> 1440751417.283
# '2015-08-28 16:43:37' --> 1440751417.0
def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        print timeStamp
        return timeStamp
    except ValueError as e:
        print e
        d = datetime.datetime.strptime(str2, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        print timeStamp
        return timeStamp

# 1440751417.283 --> '2015-08-28 16:43:37.283'
def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print e
        return ''

