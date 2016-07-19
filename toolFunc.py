#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import os
import wx
import datetime
import types
import logging
import json

date_str_format = "%Y-%m-%d"

def pydate2wxdate(date):
    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTimeFromDMY(*dmy)

def wxdate2pydate(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None


def str2wxdate(str):
    try:
        if type(str) == types.StringType and not str == '':
            date = datetime.datetime.strptime(str, date_str_format)
            tt = date.timetuple()
            dmy = (tt[2], tt[1]-1, tt[0])
            return wx.DateTimeFromDMY(*dmy)
        else:
            logging.warning('fail to covert！', str)
            return None
    except:
        logging.warning('fail to covert！', str)
        return None

def wxdate2str(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        return date.FormatISODate()
    else:
        return None


def get_files_list(path_list, exts):
    from os.path import join, getsize
    new_file_list = []
    for path in path_list:
        for root, dirs, files in os.walk(path):
            for file in files:
                for ext in exts:
                    if (file.endswith(ext)):
                        new_file_list.append({'name':file, 'files':join(root, file)})
                        break
    return new_file_list


#json file read/write
def json_store_file(name, json_file):
    with open(name, 'w') as f:
        f.write(json.dumps(json_file))
        logging.debug('write data %s to jason file %s' % (json_file, name))

def json_read_file(name):
     ret_file = None
     with open(name, 'r') as f:
        ret_file = json.load(f)
        logging.debug('read data %s from jason file %s' % (ret_file, name))
     return ret_file



#menu bar
#menu data sample
# [("&File", (             #1st level menu
#                            ("&New", "New paint file", self.OnNew),             #2nd level menu
#                            ("&Open", "Open paint file", self.OnOpen),
#                            ("&Save", "Save paint file", self.OnSave),
#                            ("", "", ""),                                       #seperator
#                            ("&Color", (
#                                        ("&Black", "", self.OnColor, wx.ITEM_RADIO),  #3nd level menu
#                                        ("&Red", "", self.OnColor, wx.ITEM_RADIO),
#                                        ("&Green", "", self.OnColor, wx.ITEM_RADIO),
#                                        ("&Blue", "", self.OnColor, wx.ITEM_RADIO))),
#                            ("", "", ""),
#                            ("&Quit", "Quit", self.OnCloseWindow)))
#                ]
def CreateMenuBar(wxFrame,menuData):
    '''
    创建菜单
    '''
    menuBar = wx.MenuBar()
    for eachMenuData in menuData:
        menuLabel = eachMenuData[0]
        menuItems = eachMenuData[1]
        menuBar.Append(CreateMenu(wxFrame,menuItems), menuLabel)
    wxFrame.SetMenuBar(menuBar)

def CreateMenu(wxFrame,menuData):
    '''
    创建一级菜单
    '''
    menu = wx.Menu()
    for eachItem in menuData:
        if len(eachItem) == 2:
            label = eachItem[0]
            subMenu = CreateMenu(wxFrame,eachItem[1])
            menu.AppendMenu(wx.NewId(), label, subMenu) #next level
        else:
            CreateMenuItem(wxFrame,menu, *eachItem)
    return menu

def CreateMenuItem(wxFrame,menu, label, status, handler, kind = wx.ITEM_NORMAL):
    '''
    creat menu item
    '''
    if not label:
        menu.AppendSeparator()
        return
    menuItem = menu.Append(-1, label, status, kind)
    wxFrame.Bind(wx.EVT_MENU, handler,menuItem)