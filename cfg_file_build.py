#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import toolFunc
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[func:%(funcName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

#kw-keyword  sc-sub class De-Description
class_definition_V1=[{"name":u"第一类","de":u"履历材料","sc":[
                        {"name":u"1-1","de":u"干部履历表","sc":[]}, \
                        {"name":u"1-2","de":u"职工登记表","sc":[]}, \
                        {"name":u"1-3","de":u"干部履历表","sc":[]}]}, \
                  {"name":u"第二类","de":u"自传","sc":[]}, \
                  {"name":u"第三类","de":u"鉴定、考察、考核材料","sc":[ \
                        {"name":u"3-1","de":u"中学生社会实践活动表","sc":[]}, \
                        {"name":u"3-2","de":u"2005年度考核登记表","sc":[]}, \
                        {"name":u"3-3","de":u"2006年度考核登记表","sc":[]}, \
                        {"name":u"3-4","de":u"2007年度考核登记表","sc":[]}, \
                        {"name":u"3-5","de":u"2008年度考核登记表","sc":[]}, \
                        {"name":u"3-6","de":u"2009年度考核登记表","sc":[]}, \
                        {"name":u"3-7","de":u"20010年度考核登记表","sc":[]}, \
                        {"name":u"3-8","de":u"20011年度考核登记表","sc":[]}, \
                        {"name":u"3-9","de":u"20012年度考核登记表","sc":[]}, \
                        {"name":u"3-10","de":u"2013年度考核登记表","sc":[]}, \
                        {"name":u"3-11","de":u"2015年度考核登记表","sc":[]}]}
                  ]

#file_path=u'E:\project\DocClassification\PIC'
file_path=[u'C:\project\APP\DocClassification\PIC']

UnpackedFileList = [{'name':u'IMG01','files':ur"C:\project\APP\DocClassification\PIC\IMG01.jpg"}, \
                        {'name':u'IMG02','files':ur"C:\project\APP\DocClassification\PIC\IMG02.jpg"}, \
                        {'name':u'IMG03','files':ur"C:\project\APP\DocClassification\PIC\IMG03.jpg"}, \
                        {'name':u'IMG04','files':ur"C:\project\APP\DocClassification\PIC\IMG04.jpg"}, \
                        {'name':u'IMG05','files':ur"C:\project\APP\DocClassification\PIC\IMG05.jpg"}, \
                        ]
OwnerList = [u'小a',\
             u'小c',\
             u'小d']

PackedFileList = [{'name':u'小a的自传','class':u'第二类', 'de':u'自传', "owner":u"小a","time":"2015-07-02",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\aa.jpg", 'name':u'第1页', 'id':-1, 'page':1}]}, \
            {'name':u'ee','class':u'第二类', 'de':u'申请表', "owner":u"小c","time":"2015-05-09",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\ee.jpg", 'name':u'第1页', 'id':-1, 'page':1}]}, \
            {'name':u'pp','class':u'第三类->3-1', 'de':u'处理单据', "owner":u"小c", "time":"2015-07-08",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\kk\pp.jpg", 'name':u'第1页', 'id':-1, 'page':1},\
                                                                                                                                None,\
                                                                                                                                 {'files':ur"C:\project\APP\DocClassification\PIC\kk\aa.jpg", 'name':u'第3页', 'id':-1, 'page':3}]}, \
            ]

sys_cfg = {'class_definition':[class_definition_V1], \
           'file_scan_path':file_path,\
           'OwnerList':OwnerList}

file_list = {'PackedFileList':PackedFileList, \
           'UnpackedFileList':UnpackedFileList,}

if __name__ == '__main__':
    toolFunc.json_store_file('sys_cfg.json', sys_cfg)
    toolFunc.json_store_file('files_cfg.json', file_list)

    print toolFunc.json_read_file('sys_cfg.json')
    print toolFunc.json_read_file('files_cfg.json')