# -*- coding: utf-8 -*-
import codecs
import re
import os
import sys
import json

#===============================================================================
# get_sql_comments
#===============================================================================
def get_sql_comments(dir_name):
    files = os.listdir(dir_name)
    result = {}
    table_pattern = re.compile('CREATE TABLE "(.*)"."(.*)"')
    for file in files:
        input_file = codecs.open("%s/%s" % (dir_name, file), "r", "utf8")
        text = input_file.read()
        tables = text.split("DROP TABLE")
        
        for table in tables:
            tmp_txt = "%s%s" % ("DROP TABLE", table)
            match = table_pattern.search(tmp_txt)
            if match:
                print (match.group(1), match.group(2))
                output_file = codecs.open("%s_out/%s.sql" % (dir_name, match.group(2)), "w", "utf8")
                output_file.write(tmp_txt)
                output_file.close()
#                 print ("$$$$$$$$$$$$$$$$888888888888888888888888$$$$$$$$$$$$")

if __name__ == '__main__':
    try:
        dir_name = sys.argv[1]
        print (dir_name)
    except:
        dir_name = "data"
        print (dir_name)
    
    os.system("mkdir %s_out" % dir_name)
    get_sql_comments(dir_name)