# -*- coding：utf-8 -*-

import os
import platform

#数据库配置模板
DB_CONFIG_TEMPLATE = {'NAME': 'orcl', 'USER': 'USER', 'PASSWORD': 'PASSWORD', 'HOST': 'HOST', 'PORT': 'PORT', "SID": True}
DB_CENTER_MANAGE = DB_CONFIG_TEMPLATE
DB_CONFIG_STORAGE = DB_CONFIG_TEMPLATE
JOB_OUTPUT_DIR = ""


#===============================================================================
# graphite配置
#===============================================================================
DEFAULT_CITY_CONFIG="suzhou"
DEFAULT_PROJECT_CONFIG="pps"
DEFAULT_GRAPHITE_HOST=""
DEFAULT_GRAPHITE_PORT="8085"
DEFAULT_GRAPHITE_QUERY_PORT="8087"

#===============================================================================
# luigi配置
#===============================================================================
DEFAULT_LUIGI_HOST=""
DEFAULT_LUIGI_PORT="8082"


