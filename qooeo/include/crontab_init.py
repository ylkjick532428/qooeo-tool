# -*- codeing: UTF8 -*-
#output_json_file:处理函数
import os
import sys
import imp
import platform
import codecs
sys.path.append("../")

get_build_files = []
LABLE_NAME_DICT = {}
platform_str = platform.system()
if platform_str == "Windows":
    platform_window = True
else:
    platform_window = False

TIME_CONFIGS = {"1m":["current_jq"], 
                    "10m":[],
                    "1h":[],
                    "1d":[]}

def get_crontab_header(time_config):
    if time_config == "1m":
        crontab_header = "*/1 * * * *"
    elif time_config == "10m":
        crontab_header = "*/10 * * * *"
    elif time_config == "1h":
        crontab_header = "3 * * * *"
    elif time_config == "1d":
        crontab_header = "3 2 * * *"
    else:
        crontab_header = "3 * * * *"
    return crontab_header

def get_time_config(output_json_file):
    time_config = "1h"
    for key, tmp_list in TIME_CONFIGS.items():
        if output_json_file in tmp_list:
            time_config = key
    return time_config

#===============================================================================
# get_router_response
#===============================================================================
def gen_crontab_sh(parent_dir=""):
    files = get_build_files(parent_dir)
    if platform_window:
        python3_path = "python3.exe"
    else:
        python3_path = "/usr/local/python3/bin/python3"
        
    crontab_result = {key:[] for key in TIME_CONFIGS.keys()}
    for floder in files.keys():
        tmp_files = files[floder]
        for tmp_file in tmp_files:
            file_path = "%s/%s/%s.py" % (parent_dir, floder, tmp_file)

            file_path = file_path.replace("\\", "/")
#             print (file_path)
            try:
                py_mod = imp.load_source(tmp_file, file_path)
                web_api = getattr(py_mod, "web_api")
                output_json_file = getattr(py_mod, "output_json_file")
                output_json_file = output_json_file.split(".")[0]
                time_config = get_time_config(output_json_file)
                crontab_header = get_crontab_header(time_config)
                crontab_cmd = "%s %s" % (python3_path, file_path)
                tmp_row = {"header": crontab_header, "value":crontab_cmd, "name":output_json_file}
                crontab_result[time_config].append(tmp_row)
            except:
                pass
    return crontab_result

#===============================================================================
# write_file_header
#===============================================================================
def write_file_header(output_file, parent_dir):
    output_file.write("source /etc/profile\n")
    output_file.write("cd %s\n" % parent_dir)
    output_file.write("export PATHONPATH=%s/../\n" % parent_dir)
    
if __name__ == '__main__':
    parent_dir = os.getcwd()
    print (parent_dir)
    parent_dir = parent_dir.replace("\\", "/")
    crontab_result = gen_crontab_sh(parent_dir)
    crontab_cmds = []
    for key, rows in crontab_result.items():
        output_file_name = "%s/start_%s.sh" % (parent_dir, key)
        output_file = codecs.open(output_file_name, "w", "utf8")
        write_file_header(output_file, parent_dir)
        LABLE_NAME_DICT
        for value in rows:
            tmp_file_name = value["name"]
            output_file.write("#=======================start %s===========================\n" % tmp_file_name)
#             print (value["header"], value["value"], parent_dir, key)
            if tmp_file_name in LABLE_NAME_DICT:
                doc_comment = LABLE_NAME_DICT
                output_file.write("#%s\n" % LABLE_NAME_DICT[tmp_file_name])
            output_file.write(value["value"])
            output_file.write("\n#=======================end %s===========================\n" % tmp_file_name)
        crontab_header = get_crontab_header(key)
        crontab_cmd = "%s %s > %s/start_%s.log" % (crontab_header, output_file_name, parent_dir, key)
        crontab_cmds.append(crontab_cmd)
        output_file.close()
    print ("\n".join(crontab_cmds))
    os.system("chmod -R 777 *")
    