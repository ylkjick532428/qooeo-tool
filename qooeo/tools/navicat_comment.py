    # -*- coding: utf-8 -*-
import codecs
import re
import os
import sys
import json

from qooeo.include.config import DB_CONFIG_TEMPLATE
from qooeo.include.oracle import MyOracleUtil
local_oracle = MyOracleUtil(DB_CONFIG_TEMPLATE)

#===============================================================================
# get_file
#===============================================================================
def get_file(tmp_file_path):
    input_file = codecs.open(tmp_file_path, "r", "utf8")
    result = []
    filed_name = []
    
    for line in input_file:
        if not filed_name:
            filed_name = line.strip().split("\t")
            continue
        line = line.strip().split("\t")
        if not line:
            continue
        
        if len(line) != len(filed_name):
            continue
        
        tmp = {}
        for i in range(0, len(filed_name)):
            tmp[filed_name[i]] = line[i] 
        result.append(tmp)
    return result
    

#===============================================================================
# get_tables_comment
#===============================================================================
def get_tables_comment():
    return get_file("csv/tables.txt")

#===============================================================================
# get_fileds_comment
#===============================================================================
def get_fileds_comment():
    return get_file("csv/fileds.txt")

#===============================================================================
# comment_table
#===============================================================================
def comment_table(user_scheme, tables_comment):
    for row in tables_comment:
#         print (row)
        comment_sql = """ COMMENT ON TABLE "%s"."%s" IS '%s'; """ % (user_scheme, row["表名"], row["注释"])
        try:
            local_oracle.update(comment_sql)
        except:
            
            print (comment_sql)

#===============================================================================
# comment_table_filed
#===============================================================================
def comment_table_filed(user_scheme, fileds_comment):
    for row in fileds_comment:
#         print (row)
        comment_sql = """ COMMENT ON COLUMN "%s"."%s"."%s" IS '%s'; """ % (user_scheme, row["表名"], row["字段"], row["注释"])
        try:
            local_oracle.update(comment_sql)
        except:
            
            print (comment_sql)
        
if __name__ == '__main__':
    USER_SCHEME = "PPS"
    tables_comment = get_tables_comment()
#     comment_table(USER_SCHEME, tables_comment)
    
    fileds_comment = get_fileds_comment()
    comment_table_filed(USER_SCHEME, fileds_comment)
    
    
    