#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

import logging
from constants import LOG_FILE_PATH

g_log_init = False

def __log_init():
    global g_log_init
    if not g_log_init:
        logging.basicConfig(level=logging.DEBUG,  
                    filename=LOG_FILE_PATH,
                    filemode='a',  
                    format='%(asctime)s - %(levelname)s: %(message)s')
        g_log_init = True

def log_info(logstr):
    __log_init()
    logging.info(logstr)

def log_debug(logstr):
    __log_init()
    logging.debug(logstr)

def log_error(logstr):
    __log_init()
    logging.error(logstr)