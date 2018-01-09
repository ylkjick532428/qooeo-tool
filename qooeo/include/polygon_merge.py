# -*- coding: utf-8 -*-
import random, math
import sys,os
import argparse
import json
import sys
import cx_Oracle
import time

from qooeo.include.config import DB_CONFIG_TEMPLATE
from Polygon import *
from Polygon.Shapes import Star, Circle, Rectangle, SierpinskiCarpet
from Polygon.IO import *
from Polygon.Utils import convexHull, tile, tileEqual, tileBSP, reducePoints, reducePointsDP, cloneGrid

#===============================================================================
# polygon_to_str : 多边形数组转字符串
#===============================================================================
def polygon_to_str2(polygon):
    points_str = ""
    for point in polygon:
        if points_str:
            points_str = "%s,%s %s" % (points_str, '{:.6f}'.format(point[0]), '{:.6f}'.format(point[1]))
        else:
            points_str = "%s %s" % ('{:.6f}'.format(point[0]), '{:.6f}'.format(point[1]))
            
    return points_str

#===============================================================================
# polygon_to_str : 多边形数组转字符串
#===============================================================================
def polygon_to_str(polygon):
    points_str = ""
    for point in polygon:
        if points_str:
            points_str = "%s,%s %s" % (points_str, '{:.5f}'.format(point[0]), '{:.5f}'.format(point[1]))
        else:
            points_str = "%s %s" % ('{:.5f}'.format(point[0]), '{:.5f}'.format(point[1]))
            
    return points_str

#===============================================================================
# str_to_polygon : 字符串转多边形数组
#===============================================================================
def str_to_polygon(polygon_str):
    polygon = []
    points = polygon_str.split(",")
    for point in points:
        point = point.split(" ")
        polygon.append((float(point[0]), float(point[1])))
        
    return polygon

#===============================================================================
# merge_polygon : 合并两个多边形
#===============================================================================
def merge_polygon(polygon1, polygon2):
    p1 = Polygon(polygon1)
    p2 = Polygon(polygon2)
    p3 = p1 + p2
    return list(p3)

#===============================================================================
# merge_polygons : 合并多个多边形
#===============================================================================
def merge_polygons(polygons):
    count = len(polygons)
    result = Polygon()
    for i in range(0, count, 1):
        result = result + Polygon(polygons[i]) 
    return list(result)
    
#===============================================================================
# print_polygon: 输出多边形
#===============================================================================
def print_polygon_str(polygons):
    max_str = ""
    max_len = 0
    for i in range(0, len(polygons), 1):
        points_str = polygon_to_str(polygons[i])
        points_len = len(points_str)
        if points_len > max_len:
            max_len = points_len
            max_str = points_str
        print ("===========================polygon%s===========================" % str(i))
        print (points_str)
    return max_str

#===============================================================================
# print_polygon: 输出多边形
#===============================================================================
def print_polygon_str2(polygons):
    tmp = []
    for i in range(0, len(polygons), 1):
        points_str = polygon_to_str(polygons[i])
        tmp.append(points_str)
    return ",".join(tmp)

def example():
    tmp_str = """120.592917 31.346308,120.637351 31.355341,120.639792 31.333612,120.598533 31.326532,120.593162 31.340204,120.592917 31.346308;120.624867 31.341612,120.652577 31.346128,120.660878 31.301939,120.660878 31.285215,120.643056 31.282530,120.638783 31.311827,120.635243 31.332945,120.630483 31.337217,120.624867 31.341612"""
    rows = tmp_str.split(";")
    polygons = []
    for row in rows:
        polygon = str_to_polygon(row)
        polygons.append(polygon)
    polygons = merge_polygons(polygons)
    print_polygon_str(polygons)
    
def get_police_department(pd_id):
    oracle = DataBaseDrive().oracle
    sql_str = "select * from police_department where pd_id=%s " % (str(pd_id))
    rows = oracle.query(sql_str)
    if len(rows) < 1:
        return False
    else:
        return rows[0]


def test():
    input_file = open("polices.txt","r")
    
    district = {"center":[49,44,43,46,51,53],
                "west":[58,57,56,59],
                "north":[47,48,63,45],
                "south":[54,52,55]}
    result = {}
    tmps = {}
    for line in input_file:
        line = line.strip()
        if not line:
            continue
        police = line.split("\t")
        pd_id = int(police[1])
        for key in district.keys():
            pd_ids = district[key]
            if key not in result:
                    result[key] = []
            if pd_id in pd_ids:
                polygon = str_to_polygon(police[8])
                result[key].append(polygon)
    final_result = {}
    for key in result.keys():
#         print (key, len(result[key]), result[key])
        polygon = merge_polygons(result[key])
        print (key, polygon_to_str(polygon[0]))
#         writeSVG('test1/CookieTiled_%s.svg' % str(key), polygon)
#         print (key, polygon)
#         print (police[1], police[2])
#         print (police[8])



#===============================================================================
# get_args : 获得命令行参数
#===============================================================================
def get_args():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description=u'多边形合并')
    parser.add_argument('--data', help=u'data, split :',default="")
    parser.add_argument('--pd_id', help=u'派出所id,逗号分隔',default="")
    parser.add_argument('--district', help=u"姑苏派出所合并辖区合并策略", default="", choices=["center", "west", "north", "south", "", "huqiu"])
    args = parser.parse_args()
    
    return args                


def init_pd_map(oracle):
    data = {}
    sql ='select p.PD_ID,p.ORI_PD_ID from POLICE_DEPARTMENT_MAP p'
    rows = oracle.query(sql)
    for row in rows:
        data[row['ori_pd_id']] = row['pd_id']
    return data

def get_file():
    oracle = DataBaseDrive().oracle
    depart_map = init_pd_map(oracle)
    input_file = open("t1.csv", "r")
    pd_ids = "4,6,11,54,208,8,9,10,53,7,3,30,5".split(",")
    pd_ids = [int(pd_id) for pd_id in pd_ids]
    result_ids = []
    for line in input_file:
        line = line.split(";")
        
        line[0] = line[0].replace('MULTIPOLYGON(((', "").replace(')))"',"").replace('"',"")
        if line[0].find(")") != -1:
            #print (line)
            continue
        lon_lat = line[0].split(',')
        lon_lat_result = []
        for tmp in lon_lat:
            tmp_tmp = tmp.split(' ')
            lon, lat = float(tmp_tmp[0]), float(tmp_tmp[1])
            lon = '{:.6f}'.format(lon)
            lat = '{:.6f}'.format(lat)
            lon_lat_result.append(" ".join([lon,lat]))
        line[1] = line[1].replace('MULTIPOLYGON(((', "").replace(')))"',"").replace('"',"")
        line[2] = line[2].replace('MULTIPOLYGON(((', "").replace(')))"',"").replace('"',"")
        if line[1] not in depart_map:
            #print("key", line)
            continue        
        pd_id = depart_map[line[1]]
        if pd_id in pd_ids:
            print ({"pd_id":pd_id})
            continue
        result_ids.append(pd_id)
        sql_str = "update police_department set polygon='%s' where pd_id=%s and ready is null" % (",".join(lon_lat_result),pd_id)
        print (sql_str, line[2])
        #oracle.update(sql_str)
        #break
    print (result_ids)
    

def get_departments_ids(oracle, parent_id):
    sql_str = "select * from police_department where parent_id=%s" % str(parent_id)
    print (sql_str)
    rows = oracle.query(sql_str)
    return [int(row["pd_id"]) for row in rows]

def get_police_department_branch(oracle):
    sql_str = "select * from police_branch"
    rows = oracle.query(sql_str)
    return [int(row["id"]) for row in rows]

def update_department_branch(oracle, parent_id, polygon_str):
#     new_clob = oracle.db_cursor.var(cx_Oracle.CLOB)
#     new_clob.setvalue(0,polygon_str)
#     key_id = oracle.db_cursor.var(cx_Oracle.NUMBER)
#     key_id.setvalue(0,parent_id)
#     oracle.db_cursor.execute("""UPDATE police_branch
#                       SET    test = :p_clob
#                       WHERE  id= :p_key"""
#     ,              p_clob = new_clob
#     ,              p_key = key_id
#                    )
#     oracle.db_conn.commit()
    
    tmp_polygon_str = polygon_str.split(",")
    tmp_polygon_str = ",".join(tmp_polygon_str[:210])
    sql_str = "update police_branch set polygon='%s' where id=%s" % (tmp_polygon_str, parent_id)
    print (sql_str)
    #oracle.update(sql_str)
    print ("update")
    
#===============================================================================
# branch_main :update police_branch polygon
#===============================================================================
def branch_main():
    oracle = DataBaseDrive().oracle
    branch_ids = get_police_department_branch(oracle)
    for branch_id in branch_ids:
#         if branch_id != 320505:
#             continue
        pd_ids = get_departments_ids(oracle, branch_id)
        polygons = []
        for pd_id in pd_ids:
            police = get_police_department(pd_id)
            if police:
                if police["polygon"]:
                    polygon = str_to_polygon(police["polygon"])
                    polygons.append(polygon)
        polygons = merge_polygons(polygons)
        print (polygons)
        result = print_polygon_str(polygons)
        polygons
        print (branch_id, pd_ids)
        update_department_branch(oracle, branch_id, result)
        print ("==============8888888888888888===========")
        time.sleep(5)

if __name__ == '__main__':
    #branch_main()
    #sys.exit(0)
    
    args = get_args()
    if args.district:
        district = {"center":[49,44,43,46,51,53],
                "west":[58,57,56,59],
                "north":[47,48,63,45],
                "south":[54,52,55],
                "huqiu":[4,6,7,11,3,8,5,9,10]}
        pd_ids = [str(pd_id) for pd_id in district[args.district]]
        args.pd_id = ",".join(pd_ids)


    if args.data:
        rows = args.data.split(";")
        polygons = []
        for row in rows:
            polygon = str_to_polygon(row)
            polygons.append(polygon)
        polygons = merge_polygons(polygons)
        print_polygon_str(polygons)
        
    if args.pd_id:
        pd_ids = args.pd_id.strip().split(",")
        polygons = []
        for pd_id in pd_ids:
            police = get_police_department(pd_id)
            if police:
                print (police["polygon"])
                if str(police["polygon"])  == "NULL":
                    continue
                polygon = str_to_polygon(police["polygon"])
                polygons.append(polygon)
        polygons = merge_polygons(polygons)
        result = print_polygon_str(polygons)
        oracle = DataBaseDrive().oracle
        update_department_branch(oracle, 320593, result)
   
    
        
    

