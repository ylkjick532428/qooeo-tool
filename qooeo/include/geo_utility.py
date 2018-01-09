# -*- coding: utf-8 -*-
import os
import gc
import sys
import math
import time
import random
import pickle
import logging
import zipfile
import argparse
import functools
import datetime
import simplejson as json

from dateutil import rrule, parser

#===============================================================================
# GeoUtility : 坐标工具类
#===============================================================================
class GeoUtility(object):

    def __init__(self):
        pass
#         self.A = 6378245.0
#         self.EE = 0.00669342162296594323

    #===========================================================================
    # A : 地球半径
    #===========================================================================
    def A(self):
        return 6378245.0

    def EE(self):
        return 0.00669342162296594323

    #===========================================================================
    # trans_wgs84_gcj02 : 84转火星坐标
    #===========================================================================
    def trans_wgs84_gcj02(self, lat, lon):
        dlat = self.trans_lat(lon - 105.0, lat - 35.0)
        dlon = self.trans_lon(lon - 105.0, lat - 35.0)
        radLat = lat / 180 * math.pi
        magic = math.sin(radLat)
        magic = 1 - self.EE() * magic * magic
        sqrtMagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.A() * (1 - self.EE())) / (magic * sqrtMagic) * math.pi)
        dlon = (dlon * 180.0) / (self.A() / sqrtMagic * math.cos(radLat) * math.pi)
        mglat = lat + dlat
        mglon = lon + dlon
        return (float("%0.6f" % float(mglat)), float("%0.6f" % float(mglon)))

    def trans_lat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret

    def trans_lon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret
    
    #===========================================================================
    # trans_gcj02_bd09 : 火星坐标转百度坐标
    #===========================================================================
    def trans_gcj02_bd09(self):
        pass

    #===========================================================================
    # trans_bd09_gcj02 :　百度坐标转火星坐标
    #===========================================================================
    def trans_bd09_gcj02(self):
        pass

    #===========================================================================
    # p2p_distance　: 两点坐标距离计算
    #===========================================================================
    def p2p_distance(self, lon1, lat1, lon2, lat2):
        radius = 6371  # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        A = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(A), math.sqrt(1 - A))
        d = radius * c
        return float("%0.6f" % float(d))
    
    #===========================================================================
    # is_point_in_polygon : 判断某个点是否在不规则多边形中
    #===========================================================================
    def is_point_in_polygon(self, point, poly):
        # point is a (x,y) tuple; poly is a [(x,y),(x,y),(x,y),(x,y),(x,y)] list

        num = len(poly)
        ii = 0
        jj = num - 1
        result = False
        for ii in range(num):
                if  ((poly[ii][1] > point[1]) != (poly[jj][1] > point[1])) and \
                    (point[0] < (poly[jj][0] - poly[ii][0]) * (point[1] - poly[ii][1]) / (poly[jj][1] - poly[ii][1]) + poly[ii][0]):
                        # print((poly[ii][1] > point[1]) != (poly[jj][1] > point[1]))
                        result = not result
                jj = ii
        return result
    
    
    #===========================================================================
    # wgs84_trans_utm
    #===========================================================================
    def wgs84_trans_utm(self, lon, lat):
        a = 6378137
        b = 6356752.3142
        f = float(1/298.257223563)
        Ln=int(lon/6)+1+30  
        lonOrigin=6*(Ln-30)-3
        return self.LL2UTM_USGS(a, f, lat, lon, lonOrigin,0)
        
    #===========================================================================
    # LL2UTM_USGS :从经纬度转换为UTM坐标（USGS方法）
    # 
    #===========================================================================
    def LL2UTM_USGS(self, a, f, lat, lon, lonOrigin, FN):

        '''
        ** Input：(a, f, lat, lon, lonOrigin, FN)
        ** a 椭球体长半轴
        ** f 椭球体扁率 f=(a-b)/a 其中b代表椭球体的短半轴
        ** lat 经过UTM投影之前的纬度
        ** lon 经过UTM投影之前的经度
        ** lonOrigin 中央经度线
        ** FN 纬度起始点，北半球为0，南半球为10000000.0m
        ---------------------------------------------
        ** Output:(UTMNorthing, UTMEasting)
        ** UTMNorthing 经过UTM投影后的纬度方向的坐标
        ** UTMEasting 经过UTM投影后的经度方向的坐标
        ---------------------------------------------
        ** 功能描述：UTM投影
        ** 作者： Ace Strong
        ** 单位： CCA NUAA
        ** 创建日期：2008年7月19日
        ** 版本：1.0
        ** 本程序实现的公式请参考
        ** "Coordinate Conversions and Transformations including Formulas" p35.
        ** & http://www.uwgb.edu/dutchs/UsefulData/UTMFormulas.htm
        '''
    
        # e表示WGS84第一偏心率,eSquare表示e的平方
        eSquare = 2*f - f*f
        k0 = 0.9996
    
        # 确保longtitude位于-180.00----179.9之间
        lonTemp = (lon+180)-int((lon+180)/360)*360-180
        latRad = math.radians(lat)
        lonRad = math.radians(lonTemp)
        lonOriginRad = math.radians(lonOrigin)
        e2Square = (eSquare)/(1-eSquare)
        
        V = a/math.sqrt(1-eSquare*math.sin(latRad)**2)
        T = math.tan(latRad)**2
        C = e2Square*math.cos(latRad)**2
        A = math.cos(latRad)*(lonRad-lonOriginRad)
        M = a*((1-eSquare/4-3*eSquare**2/64-5*eSquare**3/256)*latRad
        -(3*eSquare/8+3*eSquare**2/32+45*eSquare**3/1024)*math.sin(2*latRad)
        +(15*eSquare**2/256+45*eSquare**3/1024)*math.sin(4*latRad)
        -(35*eSquare**3/3072)*math.sin(6*latRad))
    
        # x
        UTMEasting = k0*V*(A+(1-T+C)*A**3/6
        + (5-18*T+T**2+72*C-58*e2Square)*A**5/120)+ 500000.0
        # y
        UTMNorthing = k0*(M+V*math.tan(latRad)*(A**2/2+(5-T+9*C+4*C**2)*A**4/24
        +(61-58*T+T**2+600*C-330*e2Square)*A**6/720))
        # 南半球纬度起点为10000000.0m
        UTMNorthing += FN
        return (UTMEasting, UTMNorthing)
    
    
if __name__ == '__main__':
    geo = GeoUtility()


