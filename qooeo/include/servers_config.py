# -*- coding: utf-8 -*-
import os
import sys

TRAIN_SERVERS = os.environ.get("TRAIN_SERVERS")
if TRAIN_SERVERS:
    pass
else:
    print ("can't get the run environment, please set PPS_TRAIN_SERVERS...")
    sys.exit(0)

