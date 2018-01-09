# -*- coding: utf-8 -*-
import datetime
import functools
from dateutil import rrule, parser
from qooeo.include.patterns import Singleton
from dateutil.relativedelta import relativedelta

#===============================================================================
# DateUtility : 日期工具类
#===============================================================================
class DateUtility(Singleton):

    def __init__(self):
        pass

    #===========================================================================
    # date_generator : 生成日期数组
    #===========================================================================
    def date_generator(self,start, end):
        return (list(rrule.rrule(rrule.DAILY, dtstart=parser.parse(start), until=parser.parse(end))))

    #===========================================================================
    # date_generator_str : 生成日期数组字符串
    #===========================================================================
    def date_generator_str(self,start, end):
        dates = []
        for date_str in sorted(self.date_generator(start, end)):
            dates.append(date_str.strftime("%Y%m%d"))
        return dates
    
    #===========================================================================
    # get_week_date_dict : 获得周一对应的日期, 默认最近8周
    #===========================================================================
    def get_week_date_dict(self, start="", end=""):
        if start and end:
            date_array = self.date_generator(start, end)
        else:
            end = datetime.datetime.now().strftime("%Y%m%d")
            start = self.get_before_date(end, 7*8)
            date_array = self.date_generator(start, end)
        result = {}
        for tmp_date in date_array:
            if tmp_date.weekday() == 0:
                tmp_date_str = tmp_date.strftime("%Y%m%d")
                week_id = self.week_id(tmp_date_str)
                result[week_id] = tmp_date_str
        return result
    
    #===========================================================================
    # parser
    #===========================================================================
    def parser(self, date_str):
        return parser.parse(date_str)
    
    def today(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def tomorrow(self):
        result_date = datetime.datetime.now() + datetime.timedelta(days = 1)
        return result_date.strftime("%Y%m%d")
    
    #===========================================================================
    # week_id : 获得日期为一年中的第几周
    #===========================================================================
    def week_id(self, date_str):
        tmp_date = parser.parse(date_str)
        zhou_id = str(tmp_date.isocalendar()[1])
        
        zhou_id = zhou_id.zfill(2)
        return "%s%s" % (date_str[:4], int(zhou_id)+1)
    
    #===========================================================================
    # cha_date : 差多少天
    #===========================================================================
    def cha_date(self, start, end):
        start = parser.parse(start)
        end = parser.parse(end)
        return (end-start).days
    
    #===========================================================================
    # date_temporal :　生成日期数组
    #===========================================================================
    def get_temporal_interval(self, start, temporal_interval):
        if temporal_interval == [0]:
            return {0: [start]}
        date_length = functools.reduce(lambda x,y:x+y,temporal_interval) - 1
        end = parser.parse(start) + datetime.timedelta(days = -1)
        start = end + datetime.timedelta(days = -date_length)
        start = start.strftime("%Y%m%d")
        end = end.strftime("%Y%m%d")
        date_list =  self.date_generator_str(start, end)
        result = {}
        for i in range(len(temporal_interval) - 1, -1, -1):
            result[i] = date_list[:temporal_interval[i]]
            date_list = date_list[temporal_interval[i]:]
        return result

    #===========================================================================
    # get_before_minutes
    #===========================================================================
    def get_before_minutes(self, date_str, before):
        result_date = parser.parse(str(date_str)) + datetime.timedelta(minutes = -before)
        return result_date.strftime("%Y%m%d%H%M%S")

    #===========================================================================
    # get_before_hour
    #===========================================================================
    def get_before_hour(self, date_str, before):
        result_date = parser.parse(str(date_str)) + datetime.timedelta(hours = -before)
        return result_date.strftime("%Y%m%d%H%M%S")

    #===========================================================================
    # get_before_date
    #===========================================================================
    def get_before_date(self, date_str, before):
        result_date = parser.parse(str(date_str)) + datetime.timedelta(days = -before)
        return result_date.strftime("%Y%m%d")
    
    #===========================================================================
    # get_before_month
    #===========================================================================
    def get_before_month(self, date_str, before):
        result_date = parser.parse(str(date_str)) + relativedelta(months=-before)
        return result_date.strftime("%Y%m%d")

    #===========================================================================
    # is_holiday : 判断2011年到2014年中的某一天是否为假期,假期包括国家节假日,正常周末
    #===========================================================================
    def is_holiday(self, date_str):
        shangban_dates = ['20110101', '20110102', '20110103', '20111001', '20111002', '20111003',
                           '20111004', '20111005', '20111006', '20111007', '20110202', '20110203',
                            '20110204', '20110205', '20110206', '20110207', '20110208', '20110403',
                             '20110404', '20110405', '20110430', '20110501', '20110502', '20110604',
                              '20110605', '20110606', '20110910', '20110911', '20110912', '20120101',
                               '20120102', '20120103', '20121001', '20121002', '20121003', '20121004',
                                '20121005', '20121006', '20121007', '20120222', '20120223', '20120224',
                                 '20120225', '20120226', '20120227', '20120228', '20120402', '20120403',
                                  '20120404', '20120429', '20120430', '20120501', '20120622', '20120623',
                                   '20120624', '20120930', '20130101', '20130102', '20130103', '20131001',
                                    '20131002', '20131003', '20131004', '20131005', '20131006', '20131007',
                                     '20130209', '20130210', '20130211', '20130212', '20130213', '20130214',
                                      '20130215', '20130404', '20130405', '20130406', '20130429', '20130430',
                                       '20130501', '20130610', '20130611', '20130612', '20130919', '20130920',
                                        '20130921', '20140101', '20140131', '20141001', '20141002', '20141003',
                                         '20141004', '20141005', '20141006', '20141007', '20140201', '20140202',
                                          '20140203', '20140204', '20140205', '20140206', '20140405', '20140501',
                                           '20140502', '20140503', '20140602', '20140908', '20141001', '20141002',
                                            '20141003', '20141004', '20141005', '20141006', '20141007', '20150101',
                                             '20150102', '20150218', '20150219', '20150220', '20150223', '20150224',
                                              '20150406', '20150501', '20150622', '20150928', '20151001', '20151002',
                                               '20151005', '20151006', '20151007']
        bushangban_dates = ['20110130', '20111008', '20111009', '20111231', '20110212', '20110402', '20120221',
                             '20120229', '20120331', '20120401', '20120428', '20120929', '20130105', '20130106',
                              '20131012', '20130216', '20130217', '20130407', '20130427', '20130428', '20130608',
                               '20130609', '20130922', '20130929', '20140126', '20141011', '20140208', '20140407',
                                '20140504', '20140928', '20141011']


        tmp_date = parser.parse(str(date_str))
        tmp_date_str = tmp_date.strftime("%Y%m%d")
        if tmp_date_str in shangban_dates:
            return True
        if tmp_date_str in bushangban_dates:
            return False

        if tmp_date.weekday() in [5,6]:
            return True

        return False

    #==========================================================================
    # get_month_start:获得给定日期的月份开始日期
    #===========================================================================
    def get_month_start(self, date_now=""):
        if date_now:
            date_now = datetime.datetime.strptime(date_now, "%Y%m%d")
        else:
            date_now = datetime.datetime.now()

        y=date_now.year
        m = date_now.month
        month_start_dt = datetime.date(y,m,1)
        month_start_dt = str(month_start_dt).replace("-", "")
        return month_start_dt
    
    #===========================================================================
    # date_generator_new
    #===========================================================================
    def date_generator_new(self, start, end, split_date=5):
        tmp = relativedelta(days=5)
        dt_start = parser.parse(start)
        dt_end = parser.parse(end)
        result = []
        while dt_start < dt_end:
            start_str = dt_start.strftime("%Y%m%d")
            tmp_dt_start = dt_start + tmp
            dt_start = tmp_dt_start 
            result.append(start_str)
        result.append(dt_end.strftime("%Y%m%d"))
        return result

if __name__ == '__main__':
    date_utility = DateUtility()
    print (date_utility.date_generator('20160905', '20160905'))
    print (date_utility.week_id("20161114"))
