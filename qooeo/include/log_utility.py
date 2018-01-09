# -*- coding: utf-8 -*-

import os
import gc
import sys
import math
import time
import random
import pickle
import logging
import zipfile
import argparse
import functools
import datetime
import simplejson as json

from dateutil import rrule, parser
from qooeo.include.patterns import Singleton

#===============================================================================
# LogUtility : 日志工具类
#===============================================================================
class LogUtility(Singleton):
    def __init__(self):
        pass
    
    #===========================================================================
    # log : 写日志
    #===========================================================================
    def log(self, msg, Type, path="", level=logging.INFO):
        now = time.ctime()
        log_msg = "\t".join((
                            now, msg
                            ))

        if Type == "File":
            if level == logging.INFO:
                logging.basicConfig(filename=path, level=logging.INFO)
                logging.info(log_msg)

            elif level == logging.WARNING:
                logging.basicConfig(filename=path, level=logging.WARNING)
                logging.warning(log_msg)

            elif level == logging.DEBUG:
                logging.basicConfig(filename=path, level=logging.DEBUG)
                logging.debug(log_msg)

        if Type == "Database":
            ### add log messdage into Oracle Database 
            pass