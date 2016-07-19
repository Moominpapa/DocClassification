#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx
import sys
import os
import datetime
import copy
import toolFunc


# data_str_format = "%Y-%m-%d"
#
# #kw-keyword  sc-sub class De-Description
# class_definition=[{"name":u"第一类","de":u"履历材料","sc":[
#                         {"name":u"1-1","de":u"干部履历表","sc":[]}, \
#                         {"name":u"1-2","de":u"职工登记表","sc":[]}, \
#                         {"name":u"1-3","de":u"干部履历表","sc":[]}]}, \
#                   {"name":u"第二类","de":u"自传","sc":[]}, \
#                   {"name":u"第三类","de":u"鉴定、考察、考核材料","sc":[ \
#                         {"name":u"3-1","de":u"中学生社会实践活动表","sc":[]}, \
#                         {"name":u"3-2","de":u"2005年度考核登记表","sc":[]}, \
#                         {"name":u"3-3","de":u"2006年度考核登记表","sc":[]}, \
#                         {"name":u"3-4","de":u"2007年度考核登记表","sc":[]}, \
#                         {"name":u"3-5","de":u"2008年度考核登记表","sc":[]}, \
#                         {"name":u"3-6","de":u"2009年度考核登记表","sc":[]}, \
#                         {"name":u"3-7","de":u"20010年度考核登记表","sc":[]}, \
#                         {"name":u"3-8","de":u"20011年度考核登记表","sc":[]}, \
#                         {"name":u"3-9","de":u"20012年度考核登记表","sc":[]}, \
#                         {"name":u"3-10","de":u"2013年度考核登记表","sc":[]}, \
#                         {"name":u"3-11","de":u"2015年度考核登记表","sc":[]}]}
#                   ]
#
# class_definition_history = [class_definition]
#
# #file_path=u'E:\project\DocClassification\PIC'
# file_path=u'C:\project\APP\DocClassification\PIC'
#
# PackedFileList = [{'name':u'小a的自传','class':u'第二类', 'de':u'自传', "owner":u"小a","time":"2015-07-02",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\aa.jpg", 'name':u'第1页', 'id':-1, 'page':1}]}, \
#             {'name':u'ee','class':u'第二类', 'de':u'申请表', "owner":u"小c","time":"2015-05-09",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\ee.jpg", 'name':u'第1页', 'id':-1, 'page':1}]}, \
#             {'name':u'pp','class':u'第三类->3-1', 'de':u'处理单据', "owner":u"小c", "time":"2015-07-08",'files':[{'files':ur"C:\project\APP\DocClassification\PIC\kk\pp.jpg", 'name':u'第1页', 'id':-1, 'page':1},\
#                                                                                                                                 None,\
#                                                                                                                                  {'files':ur"C:\project\APP\DocClassification\PIC\kk\aa.jpg", 'name':u'第3页', 'id':-1, 'page':3}]}, \
#             ]
# UnpackedFileList = [{'name':u'IMG01','files':ur"C:\project\APP\DocClassification\PIC\IMG01.jpg"}, \
#                         {'name':u'IMG02','files':ur"C:\project\APP\DocClassification\PIC\IMG02.jpg"}, \
#                         {'name':u'IMG03','files':ur"C:\project\APP\DocClassification\PIC\IMG03.jpg"}, \
#                         {'name':u'IMG04','files':ur"C:\project\APP\DocClassification\PIC\IMG04.jpg"}, \
#                         {'name':u'IMG05','files':ur"C:\project\APP\DocClassification\PIC\IMG05.jpg"}, \
#                         ]
# OwnerList = [u'小a',\
#              u'小c',\
#              u'小d']

sys_cfg_file_name = 'sys_cfg.json'
files_list_file_name = 'files_cfg.json'

class docctrl():
    def __init__(self):
        self.sys_cfg = toolFunc.json_read_file(sys_cfg_file_name)
        self.files_list = toolFunc.json_read_file(files_list_file_name)

    def get_class_definition(self):
        return copy.deepcopy(self.sys_cfg['class_definition'][0])

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
        return copy.deepcopy((self.files_list['PackedFileList'],self.files_list['UnpackedFileList']))

    def get_owner_list(self):
        return copy.deepcopy(self.sys_cfg['OwnerList'])

    def set_owner_list(self, OwnerList):
        self.sys_cfg['OwnerList'] = copy.deepcopy(OwnerList)
        toolFunc.json_store_file(sys_cfg_file_name, self.sys_cfg)

    def get_scan_path_list(self):
        return copy.deepcopy(self.sys_cfg['file_scan_path'])

    def set_scan_path_list(self, PathList):
        self.sys_cfg['file_scan_path'] = copy.deepcopy(PathList)
        toolFunc.json_store_file(sys_cfg_file_name, self.sys_cfg)

    def parse_file(self):
        self.files_list['UnpackedFileList'] = toolFunc.get_files_list(self.sys_cfg['file_scan_path'], ['jpg','JPG'])
        self.update_id(self.files_list['PackedFileList'])
        self.update_id(self.files_list['UnpackedFileList'])

    def update_id(self, file_list):
        for i in range(0, len(file_list)):
            file_list[i]['id'] = i

    def pack_file(self, pack_file):
        PackedFileList = self.files_list['PackedFileList']
        UnpackedFileList = self.files_list['UnpackedFileList']

        #==============================generate new pack file=====================================
        if pack_file['id'] == -1: #a new file
            new_file  = {'name':pack_file['name'],'class':pack_file['class'], 'de':pack_file['de'], "owner":pack_file['owner'],"time":pack_file['time'],'files':[], 'id':(len(PackedFileList) + 1)}
            PackedFileList.append(new_file)
        else:
            PackedFileList[pack_file['id']] = {'name':pack_file['name'],'class':pack_file['class'], 'de':pack_file['de'], "owner":pack_file['owner'],"time":pack_file['time'],'files':[], 'id':pack_file['id']}
            new_file = PackedFileList[pack_file['id']]
        file_id_list = []
        pack_file_list = pack_file['packed_files']
        #rename pack files to *docs
        for file in pack_file_list:
            if not file['files'].endswith('sdoc'):
                os.rename(file['files'], file['files'] + 'sdoc')
                file['files'] += 'sdoc'


        #get files remove from the pack file
        i = 1
        for file in pack_file_list:
            if file == None:
                new_file['files'].append(None)
            elif file.has_key('page'): # a existing file
                file['page'] = i
                file['id'] = pack_file['id']
                new_file['files'].append(file)
            else:#unpacked file
                new_file['files'].append({'files':file['files'], 'name':u'第%d页' % i, 'id':pack_file['id'], 'page':i})
                #remove file from unpacked file list
                file_id_list.append(file['id'])
            i += 1

        #update unpacked file list
        file_id_list = sorted(file_id_list)
        for i in range(0, len(file_id_list)):
            del(UnpackedFileList[file_id_list[i] - i])
        for file in pack_file['unpacked_files']:
            if file.has_key('page'):
                UnpackedFileList.append({'files':file['files'], 'name':os.path.basename(file['files'])})
        self.update_id(UnpackedFileList)
        toolFunc.json_store_file(files_list_file_name, self.files_list)

if __name__ == '__main__':
    app = docctrl()
    print app.get_files_list()
    print app.get_class_definition()