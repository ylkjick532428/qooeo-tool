# -*- coding: utf-8 -*-
import os
import sys
import logging
import math
import argparse
import datetime
import time
import json

from qooeo.include.oracle import MyOracleUtil

def get_table_names(oracle):
    sql_str = "SELECT * from user_tables"
    tables = []
    rows = oracle.query(sql_str)
    for row in rows:
        name = row["table_name"]
        tables.append(name)
    return tables

def get_table_desc(oracle, table):
    sql_str = "select DBMS_METADATA.GET_DDL('TABLE', '%s') as ddl FROM DUAL" % table
    rows = oracle.query(sql_str)
    table_space = oracle.db["USER"].upper()
    for row in rows:
        ddl = str(row["ddl"])
        ddl = ddl.replace('TABLESPACE "PPS"', 'TABLESPACE "%s"' % table_space)
        ddl = ddl.replace(table_space, "DB_USER")
    return ddl
        
if __name__ == '__main__':
    db_config_local = {}
    source_oracle = MyOracleUtil(db_config_local["77"])
    table_names = get_table_names(source_oracle)
    dist_path = "table"
    all_tables_ddl = []
    all_table_names = []
    tables_fileds = {}
    for table_name in table_names:
        all_table_names.append(table_name.upper())
        print(table_name)
        table_fileds = source_oracle.table_fileds(table_name)
        tables_fileds[table_name] = table_fileds
        print (table_name, table_fileds)
        output_file_path = "%s/%s.sql" % (dist_path, table_name.upper())
        output_file = open(output_file_path, "w")
        table_ddl = get_table_desc(source_oracle, table_name)
        print (table_ddl)
        all_tables_ddl.append(table_ddl)
        output_file.write(table_ddl)
        output_file.close()
    
    #所有表的sql
    output_file_path = "%s/all_table_ddl.sql" % (dist_path)
    output_file = open(output_file_path, "w")
    output_file.write("\n\n\n".join(all_tables_ddl))
    output_file.close()
    
    #表名单
    output_file_path = "%s/table_list.sql" % (dist_path)
    output_file = open(output_file_path, "w")
    output_file.write(",".join(all_table_names))
    output_file.close()
    
    
    #表字段
    output_file_path = "%s/tables_fileds.sql" % (dist_path)
    output_file = open(output_file_path, "w")
    output_file.write(json.dumps(tables_fileds))
    output_file.close()
    
    
    
