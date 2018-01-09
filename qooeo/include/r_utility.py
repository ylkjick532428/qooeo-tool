# -*- coding: utf-8 -*-

import os
import sys
import datetime
import re
import time
import timeit
import platform
from time import clock
from qooeo.include.patterns import Singleton
from qooeo.include.osutils import OSUtility
import codecs

#===============================================================================
# RUtility
#===============================================================================
class RUtility(Singleton):
    def __init__(self):
        plat_str = platform.system()
        if plat_str == "Darwin":
            self.R3_path = "/usr/bin/Rscript"
        else:
            self.R3_path = "/usr/local/R3/lib64/R/bin/Rscript"
        
    #===========================================================================
    # execute_r_command : 执行R命令
    #===========================================================================
    def __execute_r_command(self, tmp_file_path="command.r"):
        print ("R CMD BATCH --args %s" % tmp_file_path)
        os.system("R CMD BATCH --args %s" % tmp_file_path)
        
    #===========================================================================
    # execute_r3_command : 执行R命令
    #===========================================================================
    def execute_r3_command(self, r_path, args=[]):
        cmd_str = "%s --slave %s %s" % (self.R3_path, r_path, " ".join(args))
        print (cmd_str)
        os.system(cmd_str)
        
    #===========================================================================
    # input_r_result : 导入R运行结果
    #===========================================================================
    def __input_r_result(self):
        file_object = open('command.r.Rout', "r")
        all_the_text = file_object.read()
        lines = all_the_text.split("\n");
        tmp_str = ""
        start_tag = False
        for line in lines:
            if line and line.find("Coefficients:") != -1:
                start_tag = True
                continue
            
            if line and line.find("Degrees of Freedom:") != -1:
                break
            
            if line and start_tag:
                tmp_str = "%s\n%s" % (tmp_str, line)
        file_object.close()
        #os.system("rm -rf command.r.Rout")
        return tmp_str

    #===========================================================================
    # __output_commands : 写入R命令到文件中
    #===========================================================================
    def __output_commands(self, one_commands, tmp_file_path=False):
        if tmp_file_path:
            output = open(tmp_file_path, 'w')
        else:
            output = open('command.r', 'w')
        result = {}
        for one in one_commands:
            output.write("%s\n" % one)
        output.write("\r\n")
        output.flush()
        output.close()
    
    #===========================================================================
    # main : anlyse_func为分析r运行结果的函数
    #===========================================================================
    def main(self, commands, r_path, anlyse_func=""):
        self.__output_commands(commands, r_path)
        self.__execute_r_command(r_path)
        if anlyse_func:
            input_file = open("%sout" % r_path, "r")
            text = input_file.read()
            input_file.close()
            return anlyse_func(text)
            
        return True

    #===========================================================================
    # main3 : anlyse_func为分析r运行结果的函数
    #===========================================================================
    def main3(self, commands, r_path, anlyse_func="", args=[]):
        output = codecs.open(r_path, 'w', "utf8")
        output.write(commands)
        output.close()
        print (r_path)
        self.execute_r3_command(r_path, args)
        return True
    
if __name__ == "__main__":
    print(timeit.timeit("test()", setup="from __main__ import test", number=1))
    #commands = r_utility.get_train_commands(file_path, fileds_name)
    #for command in commands:
    #    print (command)
    #commands = r_utility.get_prediction_commands(file_path, "result.txt", train_args, fileds_name)
    #print ("===========================")
    #for command in commands:
    #    print (command)
