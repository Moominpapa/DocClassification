#!/usr/bin/env python
#-*-coding:cp936-*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import sys

#type   3-level  sample: 9-1-2
#name
#





#image path
image_path = u'C:\project\APP\doctree\PIC'

class docctrl():
    def __init__(self):
        self.docdata = []


    def update_doc_data(self):
        data = {}
        data[u"????1"] = []
        data[u"????2"] = []
        data[u"????3"] = [{u'file':u'Garden',u'path':u'C:\project\APP\doctree\PIC\Garden.jpg', u'Description':'aaa'},{u'file':u'???2',u'path':u'C:\project\APP\doctree\PIC\GreenBubbles.jpg'}]
        return data
        #return [[u"??1",1],[u"??2",2],[u"??3",[u'ddd',u'eee']]]


if __name__ == '__main__':
    app = docctrl()
    print app.update_doc_data()