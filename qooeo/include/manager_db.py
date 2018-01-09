# -*- coding: utf-8 -*-
'''

'''

import sys
import os
import json
import datetime

from qooeo.include.oracle import MyOracleUtil
from qooeo.include.config import DB_CENTER_MANAGE
from bson import json_util

#===============================================================================
# ManagerCenter : 
#===============================================================================
class ManagerCenter(object):
    '''
    classdocs
    '''
    def __init__(self, db):
        '''
        Constructor
        '''
        self.db = db
        self.oracle = MyOracleUtil(db)
    
    #===========================================================================
    # get_connect_info : 同步数据库连接, db_type 1:oracle; 2:sqlserver; 3:mysql; 4:other 
    #===========================================================================
    def get_connect_info(self):
        table_name = "VST_CONNECT_INFO"
        rows = self.oracle.get_data_rows(table_name, where="deleted = 0")
        result = {}
        for row in rows:
            key = row["id"]
            if int(row["db_type"]) == 1:
                db_type_name = "oracle"
            elif int(row["db_type"]) == 2:
                db_type_name = "sqlserver"
            elif int(row["db_type"]) == 3:
                db_type_name = "mysql"
            else:
                db_type_name = "other"
            
            row["HOST"] = row["db_host"]
            row["PORT"] = row["db_port"]
            row["USER"] = row["db_user"]
            row["NAME"] = row["db_name"]
            row["PASSWORD"] = row["db_password"]
            row["MODEL"] = row["db_model"]
            row["db_type_name"] = db_type_name
            result[key] = row
        return result
    
    #===========================================================================
    # get_job_task : 获得作业配置
    # deleted : 删除标志
    # id
    # task_id : 作业id
    # execute_strategy : 执行策略,crontab
    # execute_condition
    # ext_conn_id: 源库连接ID
    # ext_pk 
    # load_conn_id: 目标库连接ID
    # in_time
    # load_pk
    # task_name
    # ext_tb_name
    # task_state
    # acc_name
    # load_tb_name: 目的表
    # table_id : 作业表id
    # acc
    # task_type
    #===========================================================================
    def get_job_tasks(self):
        sql_str = """ """
        rows = self.oracle.query(sql_str)
        results = []
        connect_resource = self.get_connect_info()
        for row in rows:
            row["ext_conn"] = connect_resource[row["ext_conn_id"]]
            row["load_conn"] = connect_resource[row["load_conn_id"]]
            row["ext_columns"], row["load_columns"] = self.get_table_columns(row["table_id"])
            row["job_name"] = "_".join([row["ext_conn"]["USER"], row["task_name"], row["table_id"]])
            row["job_type"] = self.get_task_type(row["task_type"])
            results.append(row)
        return results
    
    #=======================================================================
    # get_task_type : 获得作业类型
    #=======================================================================
    def get_task_type(self, type_code):
        if(type_code in ['1', '3']):
            job_type = 'immediate'
        elif(type_code in ['2', '4']):
            job_type = 'timer'
        else:
            job_type = False
        return job_type
    
    #===========================================================================
    # get_table_columns
    #===========================================================================
    def get_table_columns(self, table_id):
        sql_str = ""
        ext_columns = []
        load_columns = []
        tmp_rows = self.oracle.query(sql_str)
        for tmp_row in tmp_rows:
            ext_columns.append(tmp_row["ext_column_name"])
            load_columns.append(tmp_row["load_column_name"])
        return ext_columns, load_columns
    
    #===========================================================================
    # save_log_result
    #===========================================================================
    def save_log_result(self, log_result):
        tmp = {}
        tmp["TABLE_ID"] = log_result["table_id"]
        tmp["INSERT_NUM"] = int(log_result["read_count"]) - int(log_result["read_failure"])
        tmp["UPDATE_NUM"] = tmp["INSERT_NUM"]
        tmp["COST_TIME"] = log_result["cost_time"].replace("s", "")
        tmp["STATE"] = 1
        tmp["EXC_VALUE"] = "" #log_result["text"][-1000:]
        tmp["TRACE_BACK"] = log_result["text"][-1000:].replace("'", "")
        tmp["DELETED"] = 0
        tmp["START_TIME"] = datetime.datetime.strptime(log_result["start_time"], "%Y-%m-%d %H:%M:%S")
        tmp["END_TIME"] = datetime.datetime.strptime(log_result["end_time"], "%Y-%m-%d %H:%M:%S")
        tmp["AVG_SPEED"] = log_result["avg_speed"]
        tmp["WRITE_SPEED"] = log_result["write_speed"]
        tmp["READ_FAILURE"] = log_result["read_failure"]
        insert_sql = self.oracle.get_insert_str("VST_TASK_RESULT", tmp, tmp.keys())
        try:
            self.oracle.update(insert_sql)
            print ("save log result success")
        except:
            print (insert_sql)
            print ("sql_error, save log result failure")
            sys.exit()
        
if __name__ == '__main__':
    test = ManagerCenter(DB_CENTER_MANAGE)
    data = test.get_connect_info()
    print (json.dumps(data, ensure_ascii=False, default=json_util.default, indent=True))
    
    
        