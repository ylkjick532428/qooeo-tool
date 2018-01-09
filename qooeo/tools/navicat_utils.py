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
    for file in files:
        input_file = codecs.open("%s/%s" % (dir_name, file), "r", "utf8")
        table_name, table_name_end = file.split(".")
        re_pattern = re.compile('."%s"."(\w+)" IS \'(.*)\'' % table_name)
        table_re_pattern = re.compile('"%s" IS \'(.*)\'' % table_name)
        result[table_name] = {}
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            
            match = re_pattern.search(line)
            if match:
                tmp_filed_name = match.group(1)
                result[table_name][tmp_filed_name] = match.group(2)
            
            match = table_re_pattern.search(line)
            if match:
                result[table_name]["表注释"] = match.group(1)
            
    return result

#===============================================================================
# get_sql_fileds
#===============================================================================
def get_sql_fileds(dir_name):
    files = os.listdir(dir_name)
    result = {}

    filed_pattern = re.compile('"(\w+)" ([\w,\d]+)')
    for file in files:
        input_file = codecs.open("%s/%s" % (dir_name, file), "r", "utf8")
        table_name, table_name_end = file.split(".")
        result[table_name] = {}
        start_str = 'CREATE TABLE '
        end_str = ")"
        text = ""
        start_single = False
        end_single = False
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            if line.find(start_str) != -1:
                start_single = True
                continue
            
            if line == ")":
                end_single = True
                
            if start_single and not end_single:
                text = "%s\n%s" % (text, line)
        for line in text.split("\n"):
            match = filed_pattern.search(line)
            if match:
                key, value = match.group(1), match.group(2)
                result[table_name][key] = value
#         print(json.dumps(result[table_name], ensure_ascii=False, sort_keys=True, indent=1))
    return result

if __name__ == '__main__':
    try:
        dir_name = sys.argv[1]
    except:
        dir_name = "data"
        
    navicate_sql_floder = "%s_out" % (dir_name)
    table_comments = get_sql_comments(navicate_sql_floder)
    fileds_type = get_sql_fileds(navicate_sql_floder)
    output_file = codecs.open("comments.txt", "w", "utf8")
    output_file.write("\t".join(["表名", "字段", "注释", "类型"]) + "\n")
    output_file2 = codecs.open("comments_dict.txt", "w", "utf8")
    output_file3 = codecs.open("comments_table.txt", "w", "utf8")
    output_file3.write("\t".join(["表名", "注释"]) + "\n")
    result = {}
    for table_name, table_fileds in fileds_type.items():
        result[table_name] = {}
        tmp_table_comments = table_comments[table_name]
        for table_filed, table_type in table_fileds.items():
            if table_filed in tmp_table_comments:
                tmp_filed_comment = tmp_table_comments[table_filed]
            else:
                tmp_filed_comment = "无注释"
            result[table_name][table_filed] = {"comment":tmp_filed_comment, "type":table_type}
            tmp = [table_name, table_filed, tmp_filed_comment, fileds_type[table_name][table_filed]]
            output_file.write("\t".join(tmp) + "\n")
        if "表注释" in tmp_table_comments:
            tmp = [table_name, "表注释", tmp_table_comments["表注释"], "", ""]
        else:
            tmp = [table_name, "表注释", "", "", ""]
        output_file3.write("\t".join([tmp[0], tmp[2]]) + "\n")
    output_file3.close()
    output_file.close()
    output_file2.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1))
    output_file2.close()
    print ("处理完成")
    print ("字段注释comments.txt")
    print ("注释字典comments_dict.txt")
    print ("注释字典comments_table.txt")

