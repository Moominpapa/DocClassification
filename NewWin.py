#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import copy
import types
import wx
import wx.calendar as cal
from ImageWin import *

class NewWin(wx.Dialog):
    def __init__(self, owner_list, class_list, unpacked_file_list, packed_file_list = [], win_title = u"新建文件", file_name = "", packed_file_id = -1, cs = "", owner = "",de="", time = "" ):
        wx.Dialog.__init__(self, None, -1, win_title,pos=(0,0), size=(1000, 2500))
        self.unpacked_files= copy.deepcopy(unpacked_file_list)
        self.packed_files = copy.deepcopy(packed_file_list)
        # packed_file_list = copy.deepcopy(packed_file_list)
        # self.packed_files = []
        # if packed_file_id >= 0:#valid packed file id
        #     for i in range(0, len(packed_file_list)):
        #         if packed_file_list[i] == None:
        #             self.packed_files.append(None)
        #         else:
        #             self.packed_files.append({'files':packed_file_list[i],'name':u'%s-第%d页'% (file_name,i + 1), 'packed_file_id':packed_file_id})
        self.image_win = None

        self.class_label = wx.StaticText(self, -1, u"类别")
        self.class_choice = wx.Choice(self, -1, size = (100,20), choices=class_list)
        self.class_choice.SetStringSelection(cs)

        self.owner_label = wx.StaticText(self, -1, u"所有者")
        self.owner_choice = wx.Choice(self, -1, size = (100,20),choices=owner_list)
        self.owner_choice.SetStringSelection(owner)

        self.name_label = wx.StaticText(self, -1, u"文件名")
        self.name_text = wx.TextCtrl(self, -1,"")
        self.name_text.SetValue(file_name)
        self.name_text.SetInsertionPoint(len(file_name))

        self.de_label = wx.StaticText(self, -1, u"描述")
        self.de_text = richText = wx.TextCtrl(self, -1,"", size=(200,50),style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.de_text.SetValue(de)
        self.de_text.SetInsertionPoint(len(de))
        #self.de_text.SetStyle(44, 52, wx.TextAttr("white", "black"))

        self.cal_label = wx.StaticText(self, -1, u"形成时间")
        self.cal = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_SHOW_HOLIDAYS| cal.CAL_SEQUENTIAL_MONTH_SELECTION)
        # if not time == "":
        #     cal.CalendarCtrl.SetDate(wx.DateTime(time))

        self.unpacked_file_list_label = wx.StaticText(self, -1, u"未归档文件列表")
        self.unpacked_file_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.unpacked_file_list.InsertColumn(0, u"名字")
        self.unpacked_file_list.SetColumnWidth(0, 200)#设置列的宽度
        for i in range(0,len(unpacked_file_list)):
            self.unpacked_file_list.InsertStringItem(i, self.unpacked_files[i]['name'])

        self.packed_file_list_ctrl_label = wx.StaticText(self, -1, u"文件列表")
        self.packed_file_list_ctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.packed_file_list_ctrl.InsertColumn(0, u"名字")
        self.packed_file_list_ctrl.SetColumnWidth(0, 200)#设置列的宽度
        for i in range(0,len(packed_file_list)):
            if self.packed_files[i] == None:
                self.packed_file_list_ctrl.InsertStringItem(i, u"空白页")
            else:
                self.packed_file_list_ctrl.InsertStringItem(i, self.packed_files[i]['name'])

        insertButton = wx.Button(self, -1, u"添加文件")
        moveupButton = wx.Button(self, -1, u"上移")
        movednButton = wx.Button(self, -1, u"下移")
        delButton = wx.Button(self, -1, u"删除")
        insertBlankButton = wx.Button(self, -1, u"插入空白页")

        okButton = wx.Button(self, wx.ID_OK, u"确认")
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, u"放弃")

        sizer = wx.GridBagSizer(hgap=5, vgap=10)
        sizer.Add(self.name_label, pos=(1,1), span=(1,1))
        sizer.Add(self.name_text, pos=(2,1), span=(1,3), flag = wx.EXPAND)
        sizer.Add(self.class_label, pos=(3,1), span=(1,1))
        sizer.Add(self.class_choice, pos=(4,1), span=(1,1))
        sizer.Add(self.owner_label, pos=(3,2), span=(1,1))
        sizer.Add(self.owner_choice, pos=(4,2), span=(1,1))
        sizer.Add(self.de_label, pos=(5,1), span=(1,1))
        sizer.Add(self.de_text, pos=(6,1), span=(2,3), flag = wx.EXPAND)
        sizer.Add(self.cal_label, pos = (8,1), span = (1,1))
        sizer.Add(self.cal, pos = (9,1), span = (3,3), flag = wx.EXPAND)
        sizer.Add(self.unpacked_file_list_label, pos = (1,5), span = (1,1))
        sizer.Add(self.unpacked_file_list, pos=(2,5), span=(5,3), flag = wx.EXPAND)
        sizer.Add(self.packed_file_list_ctrl_label, pos = (7,5), span = (1,1))
        sizer.Add(self.packed_file_list_ctrl, pos=(8,5), span=(5,3), flag = wx.EXPAND)
        sizer.Add(insertButton, pos = (2,8), span = (1,1))
        sizer.Add(moveupButton, pos = (8,8), span = (1,1))
        sizer.Add(movednButton, pos = (9,8), span = (1,1))
        sizer.Add(delButton, pos = (10,8), span = (1,1))
        sizer.Add(insertBlankButton, pos = (11,8), span = (1,1))
        sizer.Add(okButton, pos=(14,7))
        sizer.Add(cancelButton, pos=(14,8))
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnOKClick, okButton)
        self.Bind(wx.EVT_BUTTON, self.OnInsertClick, insertButton)
        self.Bind(wx.EVT_BUTTON, self.OnMpClick, moveupButton)
        self.Bind(wx.EVT_BUTTON, self.OnMdClick, movednButton)
        self.Bind(wx.EVT_BUTTON, self.OnDelClick, delButton)
        self.Bind(wx.EVT_BUTTON, self.OnInsertBlankClick, insertBlankButton)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnUnpackedSelect, self.unpacked_file_list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnpackedSelect, self.packed_file_list_ctrl)

    def OnOKClick(self,evt):
        if self.name_text.GetValue() == '':
            dlg = wx.MessageDialog(None, u"请输入正确的名字",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        elif self.class_choice.GetStringSelection() == '':
            dlg = wx.MessageDialog(None, u"请输入正确的类别",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        elif self.owner_choice.GetStringSelection() == '':
            dlg = wx.MessageDialog(None, u"请输入正确的文档所有者",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        else:
            evt.Skip()

    def OnMpClick(self,evt):
        selected_list = []
        item = self.packed_file_list_ctrl.GetFirstSelected()
        pre_item = item - 1
        while item >= 0:
            if not (item - pre_item) == 1:
                #uncontinous items
                dlg = wx.MessageDialog(None, u"请选择连续的文件",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
            selected_list.append(item)
            pre_item = item
            item = self.packed_file_list_ctrl.GetNextSelected(item)
        if selected_list:
            if selected_list[0] == 0:
                dlg = wx.MessageDialog(None, u"已经在最前面，无法执行上移操作",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
            else:
                start_row = selected_list[0]
                end_row = selected_list[len(selected_list) - 1]
                md_row = self.packed_files[start_row - 1]
                self.packed_file_list_ctrl.DeleteItem(start_row - 1)
                del(self.packed_files[start_row - 1])
                if md_row == None:
                    self.packed_file_list_ctrl.InsertStringItem(end_row, u'空白页')
                else:
                    self.packed_file_list_ctrl.InsertStringItem(end_row, md_row['name'])
                self.packed_files.insert(end_row,md_row)

    def OnMdClick(self,evt):
        selected_list = []
        item = self.packed_file_list_ctrl.GetFirstSelected()
        pre_item = item - 1
        while item >= 0:
            if not (item - pre_item) == 1:
                #uncontinous items
                dlg = wx.MessageDialog(None, u"请选择连续的文件",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
            selected_list.append(item)
            pre_item = item
            item = self.packed_file_list_ctrl.GetNextSelected(item)
        if selected_list:
            if selected_list[len(selected_list) - 1] == (len( self.packed_files) - 1):
                dlg = wx.MessageDialog(None, u"已经在最后面，无法执行下移操作",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
            else:
                start_row = selected_list[0]
                end_row = selected_list[len(selected_list) - 1]
                mu_row = self.packed_files[end_row + 1]
                self.packed_file_list_ctrl.DeleteItem(end_row + 1)
                del(self.packed_files[end_row + 1])
                if mu_row == None:
                    self.packed_file_list_ctrl.InsertStringItem(end_row, u'空白页')
                else:
                    self.packed_file_list_ctrl.InsertStringItem(end_row, mu_row['name'])
                self.packed_files.insert(start_row,mu_row)

    def OnDelClick(self,evt):
        selected_list = []
        item = self.packed_file_list_ctrl.GetFirstSelected()
        while item >= 0:
            selected_list.append(item)
            item = self.packed_file_list_ctrl.GetNextSelected(item)

        for i in range(0,len(selected_list)):
            selected_list[i] -= i

        for index in selected_list:
            if not self.packed_files[index] == None: #don't append none item
                cur_row = self.unpacked_file_list.GetItemCount()
                self.unpacked_file_list.InsertStringItem(cur_row, self.packed_files[index]['name'])
                self.unpacked_files.append(self.packed_files[index])
                #self.packed_file_list_ctrl.SetStringItem(cur_row, 1, )
            self.packed_file_list_ctrl.DeleteItem(index)
            del(self.packed_files[index])

    def OnInsertBlankClick(self, evt):
        item = self.packed_file_list_ctrl.GetFirstSelected()
        last_item = item
        while item >= 0:
            last_item = item
            item = self.packed_file_list_ctrl.GetNextSelected(item)

        #get last selected item
        if last_item >= 0:
            #in first page
            self.packed_file_list_ctrl.InsertStringItem(last_item, u'空白页')
            self.packed_files.insert(last_item, None)
        else:
            self.packed_file_list_ctrl.InsertStringItem(0, u'空白页')
            self.packed_files.insert(0, None)

    def OnInsertClick(self,evt):
        selected_list = []
        item = self.unpacked_file_list.GetFirstSelected()
        while item >= 0:
            selected_list.append(item)
            item = self.unpacked_file_list.GetNextSelected(item)

        for i in range(0,len(selected_list)):
            selected_list[i] -= i

        for index in selected_list:
            cur_row = self.packed_file_list_ctrl.GetItemCount()
            #u"第%s页" % cur_row
            self.packed_file_list_ctrl.InsertStringItem(cur_row, self.unpacked_files[index]['name'])
            self.packed_files.append(self.unpacked_files[index])
            #self.packed_file_list_ctrl.SetStringItem(cur_row, 1, )
            self.unpacked_file_list.DeleteItem(index)
            del(self.unpacked_files[index])

    def OnUnpackedSelect(self,evt):
        file = self.unpacked_files[evt.GetIndex()]
        if file:
            if self.image_win == None:
                self.image_win = ImageWin(self, file)
            else:
                self.image_win.load_image(file)
            self.image_win.Show()

    def OnpackedSelect(self,evt):
        file = self.packed_files[evt.GetIndex()]
        if file:
            if self.image_win == None:
                self.image_win = ImageWin(self, file['files'])
            else:
                self.image_win.load_image(file['files'])
            self.image_win.Show()

    def GetNewData(self):
        return {'name':self.name_text.GetValue(), "class":self.class_choice.GetStringSelection(),\
                'de':self.de_text.GetValue(), "owner":self.owner_choice.GetStringSelection(), \
                "time":self.cal.GetDate().FormatISODate(), "packed_files":self.packed_files, \
                "unpacked_files":self.unpacked_files}

if __name__ == '__main__':
    app = wx.PySimpleApp(redirect=True)
    frame = NewWin([],[])
    frame.Show()
    app.MainLoop()