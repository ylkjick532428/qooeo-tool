# -*- coding: utf-8 -*-
'''

'''

import sys
import os
import re
import json
import argparse
import platform
import time

from qooeo.include.config import DATAX_CONFIG_DIR, DATAX_CONFIG_LOG_DIR, DATAX_CONFIG_SCRIPT

#===============================================================================
# get_args : 获得命令行参数
#===============================================================================
def get_args():
    if len(sys.argv) == 1:
        print ("place use:\npython3 %s -h" % sys.argv[0])
        #sys.exit(0)
        
    parser = argparse.ArgumentParser(description=u'')
    parser.add_argument('--init', help=u"init default=False", default="False", choices=["True", "False"], required=True)
    args = parser.parse_args()
    args.init = True if args.init == "True" else False
    return args

#===============================================================================
# execute_job_main
#===============================================================================
def execute_job_main(job_json_path, table_id):
    cmd = "python %s %s -t %s" % (DATAX_CONFIG_SCRIPT, job_json_path, table_id)
    print (cmd)
    os.system(cmd)
    time.sleep(1)
    
#===============================================================================
# execute_job_crontab
#===============================================================================
def execute_job_crontab(job_json_path, table_id):
    cmd = "python %s %s -t %s" % (DATAX_CONFIG_SCRIPT, job_json_path, table_id)
    return cmd
    
if __name__ == "__main__":
    pass
    