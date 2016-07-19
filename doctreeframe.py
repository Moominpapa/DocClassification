#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import types
import wx
import wx.gizmos
import os
import datetime
import logging

from docctrl import *
from FilterWin import *
from EditWin import *
from NewWin import *
from ImageWin import *
from OwnerWin import *
from PathWin import *


#Colum list
col_def = ({'name':u"文件",'width':200,'def':'name'},\
           {'name':u"描述",'width':180,'def':'de'},\
           {'name':u"形成时间",'width':100,'def':'time'},\
           {'name':u"所有者",'width':100,'def':'owner'})

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[func:%(funcName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

class MainTreeList(wx.Frame):
    def __init__(self):
        #class tree  {name, keyword, tree node object}
        self.c_tree = {}
        self.unpacked_class_node = None
        self.unpacked_file_list = None
        self.packed_file_list = []
        self.owner_list = []
        self.class_list = []
        self.docctrl=docctrl()
        #windows handler
        self.image_win = None
        self.filter_win  = None
        wx.Frame.__init__(self, None, title=u"文档管理", pos = (0,0), size=(600, 700))
        #create image list
        il = wx.ImageList(16,16)
        # add image to list
        self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,wx.ART_OTHER, (16,16)))
        self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,wx.ART_OTHER, (16,16)))
        self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,wx.ART_OTHER, (16,16)))

        win_width = 0
        self.tree = wx.gizmos.TreeListCtrl(self, style = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_SINGLE)
        self.tree.AssignImageList(il)

        #add column
        for i in range(0,len(col_def)):
            self.tree.AddColumn(col_def[i]['name'])
            self.tree.SetColumnWidth(i, col_def[i]['width'])
            win_width += col_def[i]['width']

        self.root = self.tree.AddRoot(u"所有类别")
        self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.UpdateTree()

        # Bind events
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)

        #creat menu
        # menuBar = wx.MenuBar()# 创建一个菜单栏
        # data_menu = wx.Menu()
        # menuBar.Append(data_menu, u"数据")
        # filter_menu = data_menu.Append(-1,u"过滤器")
        # search_menu = data_menu.Append(-1,u'搜索器')
        # menu = wx.Menu()# 创建一个菜单
        # menuBar.Append(menu, u"编辑")# 添加菜单到菜单栏
        # new_menu = menu.Append(-1, u"创建")
        # edit_menu = menu.Append(-1, u"修改")
        # #remove_menu = menu.Append(-1, u"删除")
        # menu = wx.Menu()# 创建一个菜单
        # menuBar.Append(menu, u"配置")# 添加菜单到菜单栏
        # cfg_path_menu = menu.Append(-1, u"工作路径设置")
        # cfg_seperate_bar = menu.Append(-1, u"")
        # cfg_owner_menu = menu.Append(-1, u"人员列表")
        # cfg_class_menu = menu.Append(-1, u"文档类别")
        # self.Bind(wx.EVT_MENU, self.OnMenuFilter,filter_menu)
        # self.Bind(wx.EVT_MENU, self.OnFileNew, new_menu)
        # self.Bind(wx.EVT_MENU, self.OnFileEdit, edit_menu)
        # self.Bind(wx.EVT_MENU, self.OnCfgOwner, cfg_owner_menu)
        # self.Bind(wx.EVT_MENU, self.OnCfgClass, cfg_class_menu)
        # self.SetMenuBar(menuBar)

        menuData = ((u"数据",((u"过滤器", "", self.OnMenuFilter),\
                    (u"搜索器", "", None))),\
         (u"编辑",((u"创建", "", self.OnFileNew),\
                    (u"修改", "", self.OnFileEdit),\
                     (u"删除", "", None))),\
         (u"配置",((u"工作路径设置", "", self.OnCfgPath),\
                    (u"", "", None),\
                    (u"人员列表", "", self.OnCfgOwner),\
                    (u"文档类别", "", self.OnCfgClass)))\
         )

        toolFunc.CreateMenuBar(self,menuData)


    def UpdateTree(self):
        self.tree.DeleteChildren(self.root)
        self.c_tree = {}
        self.unpacked_class_node = None
        self.unpacked_file_list = None
        self.packed_file_list = []
        self.owner_list = []
        self.class_list = []

        #TODO
        #self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)

        (self.packed_file_list, self.unpacked_file_list) = self.get_file_list()
        self.build_class_tree('',self.root, self.docctrl.get_class_definition())
        self.bulid_file_tree(col_def, (self.packed_file_list, self.unpacked_file_list ))
        # Expand the first level
        self.tree.Expand(self.root)


    #=====================TreeList event=========================================
    def OnItemExpanded(self, evt):
        print "OnItemExpanded: ", self.GetItemText(evt.GetItem())

    def OnItemCollapsed(self, evt):
        print "OnItemCollapsed:", self.GetItemText(evt.GetItem())

    def OnSelChanged(self, evt):
        image_path = None
        data =  self.tree.GetItemPyData(evt.GetItem())
        print "OnSelChanged: ", self.GetItemText(evt.GetItem()),data
        if data:
            if data['type'] == "file_group_node":
            #a files group node
                pass
            else:
                if self.image_win == None:
                    self.image_win = ImageWin(self, data['file'])
                    self.Bind(wx.EVT_CLOSE, self.OnImageWinClosed, self.image_win)
                else:
                    self.image_win.load_image(data['file'])
                self.image_win.Show()

    def OnImageWinClosed(self, evt):
        print "image win closed"

    def OnActivated(self, evt):
        print "OnActivated: ", self.GetItemText(evt.GetItem())

    #============================Menu Event========================================
    def OnMenuFilter(self,evt):
        if self.filter_win == None:
            self.filter_win = FilterWin(self.owner_list,self.class_list)
        result = self.filter_win.ShowModal()
        if result == wx.ID_OK:
            (class_list,owner_list,time_range) =self.filter_win.GetFilterData()
            self.FilterFileTree(class_list, owner_list, time_range)

    def OnMenuSearch(self,evt):
        self.OnEdit('')

    #file control
    def OnFileNew(self,evt):
        new_win = NewWin(self.docctrl.get_owner_list(),self.c_tree.keys(),self.unpacked_file_list)
        result = new_win.ShowModal()
        if result  == wx.ID_OK:
            new_file = new_win.GetNewData()
            new_file['id'] = -1
            self.docctrl.pack_file(new_file)
            self.UpdateTree()

    def OnFileEdit(self, evt):
        item_data =  self.tree.GetItemPyData(self.tree.GetSelection())
        if item_data:
            data = item_data['file']
            if data and item_data['type'] == 'file_group_node':
                edit_win = NewWin(self.docctrl.get_owner_list(),self.c_tree.keys(),self.unpacked_file_list, packed_file_list = data['files'], \
                        win_title = u"编辑文件", file_name = data['name'], packed_file_id=data['id'],cs = data['class'], owner = data['owner'],de=data['de'], time = data['time'])
                result = edit_win.ShowModal()
                if result  == wx.ID_OK:
                    new_file = edit_win.GetNewData()
                    new_file['id'] = data['id']
                    self.docctrl.pack_file(new_file)
                    self.UpdateTree()
            else:#invalid file node
                dlg = wx.MessageDialog(None, u"请选择可修改的文档",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
        else:#invalid file node
                dlg = wx.MessageDialog(None, u"请选择可修改的文档",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()

    #system configuration
    def OnCfgPath(self,evt):
        path_win = PathWin(self.docctrl.get_scan_path_list())
        result = path_win.ShowModal()
        if result  == wx.ID_OK:
            self.docctrl.set_scan_path_list(path_win.GetNewData())

    def OnCfgOwner(self,evt):
        owner_win = OwnerWin(self.docctrl.get_owner_list())
        result = owner_win.ShowModal()
        if result  == wx.ID_OK:
            self.docctrl.set_owner_list(owner_win.GetNewData())

    def OnCfgClass(self,evt):
        pass

    #============================tree===================================================
    #get file list from doc module and verify its format
    def get_file_list(self):
        (packed_file_list,unpacked_file_list) = self.docctrl.get_files_list()
        for file in packed_file_list:
            #check necessary keys
            if file.has_key('owner') and file.has_key('name') and file.has_key('class'):
                pass
            else:
                print "error file:",file
                packed_file_list.remove(file)

        for file in unpacked_file_list:
            #check necessary keys
            if file.has_key('name') and file.has_key('files'):
                pass
            else:
                print "error file:",file
                unpacked_file_list.remove(file)

        return (packed_file_list, unpacked_file_list)

    def build_class_tree(self, pc_str, parenttree, cd):
        self.build_class_tree_int(pc_str,parenttree,cd)
        #add unpacked class node
        self.unpacked_class_node = self.tree.AppendItem(parenttree, unicode(u'未归档'))
        self.tree.SetItemText(self.unpacked_class_node,u'未归档文件' , 1)
        self.tree.SetItemImage(self.unpacked_class_node, self.fldridx, wx.TreeItemIcon_Normal)

    #pc_str-parent class str, cd-class definition
    def build_class_tree_int(self, pc_str, parenttree, cd):
        for c_item in cd:
            if c_item:
                class_str = pc_str + c_item['name']
                sc_node = self.tree.AppendItem(parenttree, unicode(c_item['name']))
                self.tree.SetItemText(sc_node,c_item['de'] , 1)
                self.tree.SetItemImage(sc_node, self.fldridx, wx.TreeItemIcon_Normal)# 设置根的图像
                #TODO
                #self.tree.SetItemImage(sc_node, self.fldropenidx, wx.TreeItemIcon_Expanded)
                if self.c_tree.has_key(class_str):
                    print "Duplicated class:",class_str
                else:
                    self.c_tree[class_str] = {'node':sc_node}
                #build sub class
                if c_item['sc']:
                    self.build_class_tree_int(class_str + '->',sc_node, c_item['sc'])

    #build file tree and generate self.owner_list, self.class_list
    def bulid_file_tree(self, col_def, files_list):
        packed_file_list = files_list[0]
        de_matrix = {}
        for i in range(0, len(col_def)):
            de_matrix[col_def[i]['def']] = i

        for file in packed_file_list:
            #find class node in c_tree
            if type(file['files']) == types.ListType:
                #add file group node
                file_group_node = self.tree.AppendItem(self.c_tree[file['class']]['node'], '',data= wx.TreeItemData({"file":file,"type":"file_group_node"}))
                self.tree.SetItemImage(file_group_node, self.fldropenidx, wx.TreeItemIcon_Normal)
                #add others column
                for item in de_matrix:
                    if file.has_key(item):
                        self.tree.SetItemText(file_group_node,file[item] , de_matrix[item])

                if not filter(lambda item:item == file['owner'],self.owner_list):
                    self.owner_list.append(file['owner'])
                if not filter(lambda item:item == file['class'],self.class_list):
                    self.class_list.append(file['class'])

                for file in file['files']:
                    if file:
                        file_node = self.tree.AppendItem(file_group_node, file['name'],data= wx.TreeItemData({'file':file['files'],'type':"file"}))
                        self.tree.SetItemImage(file_node, self.fileidx, wx.TreeItemIcon_Normal)

        unpacked_file_list = files_list[1]
        for file in unpacked_file_list:
            file_node = self.tree.AppendItem(self.unpacked_class_node, file['name'],data= wx.TreeItemData({'file':file['files'],'type':"file"}))
            self.tree.SetItemImage(file_node, self.fileidx, wx.TreeItemIcon_Normal)


                # else:
                #     #add file node, generally 'unpacked' file
                #     file_node = self.tree.AppendItem(self.c_tree[file['class']]['node'], '',data= wx.TreeItemData({'file':file_name[0],'type':"file"}))
                #     self.tree.SetItemImage(file_node, self.fileidx, wx.TreeItemIcon_Normal)
                #     #add others column
                #     for item in de_matrix:
                #         if file.has_key(item):
                #             self.tree.SetItemText(file_group_node,file[item] , de_matrix[item])
                #
                #     if not filter(lambda item:item == file['owner'],self.owner_list):
                #         self.owner_list.append(file['owner'])
                #     if not filter(lambda item:item == file['class'],self.class_list):
                #         self.class_list.append(file['class'])

                #add file node, generally 'unpacked' file


    def FilterFileTree(self, req_class_list,req_owner_list, time_range):
        #remove all files

        # for c_item in self.c_tree:
        #     self.tree.DeleteChildren(self.c_tree[c_item]['node'])
        self.c_tree = {}
        self.tree.DeleteChildren(self.root)
        self.build_class_tree('',self.root,self.docctrl.get_class_definition())
        start_time_stamp = datetime.datetime.strptime(time_range[0], "%Y-%m-%d")
        end_time_stamp = datetime.datetime.strptime(time_range[1], "%Y-%m-%d")
        filter_file_list = []
        for file in self.file_list:
            #find file with certain owner and class
            if file['class'] ==  u'未处理文件':
                filter_file_list.append(file)
            else:
                file_time_stamp = datetime.datetime.strptime(file['time'], "%Y-%m-%d")

                if filter(lambda item:item == file['owner'],req_owner_list) and \
                        filter(lambda item:item == file['class'],req_class_list) and \
                            (file_time_stamp - start_time_stamp).days >= 0 and \
                                (end_time_stamp - file_time_stamp).days >= 0:
                    filter_file_list.append(file)
        self.bulid_file_tree(col_def, filter_file_list)

    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""

class MainApp(wx.App):
    '''''
    创建一个App类
    '''
    def __init__(self, redirect = True, filename = None):
        print "APP __init__"
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        self.frame = MainTreeList()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(redirect = False) #开始重定向
    print u"begin MainLoop"
    app.MainLoop()
    print u"after MainLoop"


