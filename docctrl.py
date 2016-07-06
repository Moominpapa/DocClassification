#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import sys
import os


#kw-keyword  #sc-sub class
class_definition=[{"name":u"类型1","kw": u"aa","sc":[]}, \
                  {"name":u"类型2","kw": u"bb","sc":[]}, \
                  {"name":u"类型3","kw": u"cc","sc":[ \
                      {"name":u"子类型1","kw": u"dd","sc":[]}, \
                      {"name":u"子类型2","kw": u"ee","sc":[]}] }, \
                  {"name":u"未知","kw": u"","sc":[]}
                  ]

file_path='E:\project\DocClassification\PIC'



class docctrl():
    def __init__(self):
        self.docdata = []

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
        file_list = self.get_file_names(file_path)
        for file in file_list:
            f = open(file,"rb")
            if f:
                f.seek(-6, 2)
                buff = f.read(1)
                print ord(buff)
        return

if __name__ == '__main__':
    app = docctrl()
    print app.get_files_list()
    print app.get_class_definition()