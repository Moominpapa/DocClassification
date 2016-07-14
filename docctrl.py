#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import sys
import os
import datetime
import copy

data_str_format = "%Y-%m-%d"



#kw-keyword  sc-sub class De-Description
class_definition=[{"name":u"第一类","de":u"履历材料","sc":[
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

class_definition_history = [class_definition]

#file_path=u'E:\project\DocClassification\PIC'
file_path=u'C:\project\APP\DocClassification\PIC'

PackedFileList = [{'name':u'小a的自传','class':u'第二类', 'de':u'自传', "owner":u"小a","time":"2015-07-02",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\aa.jpg", 'name':u'第一页', 'id':-1, 'page':1}]}, \
            {'name':u'ee','class':u'第二类', 'de':u'申请表', "owner":u"小c","time":"2015-05-09",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\ee.jpg", 'name':u'第一页', 'id':-1, 'page':1}]}, \
            {'name':u'pp','class':u'第三类->3-1', 'de':u'处理单据', "owner":u"小c", "time":"2015-07-08",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\kk\pp.jpg", 'name':u'第一页', 'id':-1, 'page':1},\
                                                                                                                                None,\
                                                                                                                                 {'files':ur"C:\project\APP\DocClassification\PIC\kk\aa.jpg", 'name':u'第三页', 'id':-1, 'page':3}]}, \
            ]
UnpackedFileList = [{'name':u'IMG01','files':ur"C:\project\APP\DocClassification\PIC\IMG01.jpg"}, \
                        {'name':u'IMG02','files':ur"C:\project\APP\DocClassification\PIC\IMG02.jpg"}, \
                        {'name':u'IMG03','files':ur"C:\project\APP\DocClassification\PIC\IMG03.jpg"}, \
                        {'name':u'IMG04','files':ur"C:\project\APP\DocClassification\PIC\IMG04.jpg"}, \
                        {'name':u'IMG05','files':ur"C:\project\APP\DocClassification\PIC\IMG05.jpg"}, \
                        ]

class docctrl():
    def __init__(self):
        self.PackedFileList = PackedFileList
        self.UnpackedFileList = UnpackedFileList

    def get_class_definition(self):
        return class_definition

    def get_file_names(self,dir):
        exts = ['jpg','jpeg']
        files = os.listdir(dir)
        file_names = []
        for name in files:
            fullname = os.path.join(dir, name)
            if (os.path.isdir(fullname)):
            #get sub folder files
                file_names += self.get_file_names(fullname)
            else:
                for ext in exts:
                    if (name.endswith(ext)):
                        file_names.append(fullname)
                        break
        return file_names

    def get_files_list(self):
        # file_list = self.get_file_names(file_path)
        # for file in file_list:
        #     f = open(file,"rb")
        #     if f:
        #         f.seek(-6, 2)
        #         buff = f.read(6)
        #         print ord(buff)
        self.parse_file()
        return copy.deepcopy((self.PackedFileList,self.UnpackedFileList))

    def parse_file(self):
        for i in range(0, len(self.PackedFileList)):
            self.PackedFileList[i]['id'] = i
        for i in range(0, len(self.UnpackedFileList)):
            self.UnpackedFileList[i]['id'] = i

    def pack_file(self, data):
        new_file  = {'name':data['name'],'class':data['class'], 'de':data['de'], "owner":data['owner'],"time":data['time'],'files':[]}
        index = 0
        file_id_list = []
        for file in data['packed_files']:
            new_file['files'].append(file['files'])
            #remove file from unpacked file list
            file_id_list.append(file['id'])
            index+=1
        file_id_list = sorted(file_id_list)
        for i in range(0, len(file_id_list)):
            del(self.UnpackedFileList[file_id_list[i] - i])
        print 'new item', new_file
        self.PackedFileList.append(new_file)
        pass

if __name__ == '__main__':
    app = docctrl()
    print app.get_files_list()
    print app.get_class_definition()