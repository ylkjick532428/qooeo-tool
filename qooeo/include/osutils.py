# -*- coding: utf-8 -*-
"""
OS 相关操作
"""

import os
import pickle
import zipfile
import json
import string
import random
from qooeo.include.patterns import Singleton

#===============================================================================
# OSUtility : 系统工具类
#===============================================================================
class OSUtility(Singleton):

    def __init__(self):
        pass

    
    def fingerprint(self, length=15):
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for i in range(length)])
    
    #===========================================================================
    # read : 读文件
    #===========================================================================
    def read(self, path, filetype=None):
        if self.is_file_exist(path) is True:
            if filetype == "json":
                with open(path, mode="r", encoding="utf-8") as fp:
                    data = fp.read()
                    data = data.replace("\n","")
                    data = json.loads(data)
                return data

            if filetype == "txt" or filetype == "csv":
                with open(path, mode="r", encoding="utf-8") as fp:
                    data = fp.readlines()
                return data

            if filetype == "pck":
                with open(path, mode="rb") as fp:
                    data = pickle.load(fp)
                return data
        else:
            output_string = "%s path is not exist! Please Check the path is correct!"

    #===========================================================================
    # reverse_dict : 字典键值互换
    #===========================================================================
    def reverse_dict(self, tmp_dict):
        result = {}
        for key in tmp_dict.keys():
            value = tmp_dict[key]
            result[value] = key
        return result

    #===========================================================================
    # save_rows_cells : 写入行列数据
    #===========================================================================
    def save_rows_cells(self, rows, path, split=",", headers=[]):
        output_file = open(path, "w")
        if headers:
            line = split.join(headers) + "\n"
            output_file.write(line)
        for row in rows:
            row = [str(cel) for cel in row]
            line = split.join(row) + "\n"
            output_file.write(line)
        output_file.close()
        
    #===========================================================================
    # save : 写文件
    #===========================================================================
    def save(self, data, path, filetype=None):

        if filetype == "csv" or filetype == "txt":
            with open(path, mode="w", encoding="utf-8") as fp:
                data = u"%s" % (data)
                fp.write(data)

        if filetype == "json":
            with open(path, mode="w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=3)

        if filetype == "pck":
            with open(path, mode="w") as fp:
                pickle.dump(data, fp)

        return True

    #===========================================================================
    # is_file_exist : 文件是否存在
    #===========================================================================
    def is_file_exist(self, path):
        return (os.path.isfile(path))

    #===========================================================================
    # is_directory_exist : 目录是否存在
    #===========================================================================
    def is_directory_exist(self, path):
        return(os.path.isdir(path))

    #===============================================================================
    # is_dir : 检查文件夹路径是否存在，不存在的话创建文件夹
    #===============================================================================
    def is_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
            print ("%s make floder success!" % dir_path)
        else:
            print ("%s floder has exist!" % dir_path)

    #===========================================================================
    # mkdir : 创建目录
    #===========================================================================
    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    #===========================================================================
    # touch : 创建文件
    #===========================================================================
    def touch(self, path):
        if not os.path.exists(path):
            open(path, "a").close()

    #===========================================================================
    # rm : 移除路径
    #===========================================================================
    def rm(self, path):
        if os.path.exists(path):
            os.remove(path)

    #===========================================================================
    # zip : change filenames in zip file
    #===========================================================================
    def zip(self, path):
        target_file = os.path.basename(path) + ".zip"
        filenames = os.listdir(path)
        filenames = [os.path.join(path, x) for x in filenames]

        zipfiles = zipfile.ZipFile(
            os.path.join(os.path.abspath(os.path.join(path, os.pardir)), target_file), 'w', compression=zipfile.ZIP_DEFLATED)

        for filename in filenames:
            zipfiles.write(filename)
        zipfiles.close()


    #===========================================================================
    # unzip : change filenames in zip file
    #===========================================================================
    def unzip(self, path, filename):
        zipfiles = zipfile.ZipFile(filename, "r")
        zipfiles.extractall(
            os.path.join(path, os.path.basename(os.path.splitext(filename)[0])))
        zipfiles.close()

    #===============================================================================
    # get_year_from_str : 获得dates_str字符串中最大的时间或最小的时间
    #===============================================================================
    def get_year_from_str(self, dates_str, max=False, min=False):
        import re
        date_pattern = re.compile("(\d{8})")
        matchs = date_pattern.findall(dates_str)
        if max:
            max_date=0
            for match in matchs:
                if int(match) > max_date:
                    max_date = int(match)
            return max_date
        if min:
            min_date=20300202
            for match in matchs:
                if int(match) < min_date:
                    min_date = int(match)
            return min_date

    #===============================================================================
    # get_args_date : 提取字符串中的日期数据
    #===============================================================================
    def get_args_date(self, dates_str):
        import re
        date_pattern = re.compile("^(\d\d\d\d)(\d\d)(\d\d)$")
        dates_str_array = dates_str.split(";")
        results = []
        for one_dates_str in dates_str_array:
            tmp_dates_str = one_dates_str.split("-")
            result = []
            for date_str in tmp_dates_str:
                match = date_pattern.search(date_str)
                if match:
                    date_str = "%s-%s-%s" % (match.group(1),match.group(2),match.group(3))
                    date_str = "%s%s%s" % (match.group(1),match.group(2),match.group(3))
                    result.append(int(date_str))
            results.append(result)
        return results

    #===============================================================================
    # sort_by_value : 字典按值排序
    #===============================================================================
    def sort_by_value(self, d):
        items=d.items()
        backitems=[[v[1],v[0]] for v in items]
        backitems.sort(reverse=True)
        return [ backitems[i][1] for i in range(0,len(backitems))]

    #===========================================================================
    # statistic_list : 计算数组中值次数
    #===========================================================================
    def statistic_list(self, input_list):
        result = {}
        for i in input_list:
            index = str(i)
            try:
                count = result[index]
                count += 1
                result[index] = count
            except:
                result[index] = 1
        return result

    #===============================================================================
    # sort_rows : 根据日期，和总概率排序
    #===============================================================================
    def sort_rows(self, rows):
        days = [row[0] for row in rows]
        days = list(set(days))
        days.sort()
    #    days.sort(reverse = True)
        result = []
        for day in days:
            tmp_results = {}
            tmp_results_rows = {}
            index = 1
            for row in rows:
                if day == row[0]:
                    key = str(index)
                    tmp_results[key] = row[5]
                    tmp_results_rows[key] = row
                    index += 1
            tmp_rows = self.sort_by_value(tmp_results)
            for key in tmp_rows:
                result.append(tmp_results_rows[key])
        return result
