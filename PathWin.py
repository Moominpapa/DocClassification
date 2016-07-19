#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx
import copy
import os

class PathWin(wx.Dialog):
    def __init__(self, path_list):
        self.own_list = copy.deepcopy(path_list)
        wx.Dialog.__init__(self, None, -1,u"文档路径设置",size=(1000, 2000))
        #self.path_label = wx.StaticText(self, -1, u"成员名")
        self.path_list_ctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.path_list_ctrl.InsertColumn(0, u"路径")
        self.path_list_ctrl.SetColumnWidth(0, 300)#设置列的宽度
        for i in range(0,len(self.own_list)):
            self.path_list_ctrl.InsertStringItem(i, self.own_list[i])
        okButton = wx.Button(self, wx.ID_OK, u"确认")
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, u"放弃")
        deleButton = wx.Button(self, -1, u"删除")
        addButton = wx.Button(self, -1, u"添加")

        sizer = wx.GridBagSizer(hgap=5, vgap=10)
        sizer.Add(addButton, pos=(1,1), span=(1,1))
        sizer.Add(deleButton, pos=(2,1), span=(1,1))
        #sizer.Add(self.path_label, pos=(2,3), span=(1,1))
        sizer.Add(self.path_list_ctrl, pos=(2,2), span=(2,3), flag = wx.EXPAND)
        sizer.Add(okButton, pos=(4,3))
        sizer.Add(cancelButton, pos=(4,4))
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnOKClick, okButton)
        self.Bind(wx.EVT_BUTTON, self.OnDele, deleButton)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, addButton)

    def OnOKClick(self,evt):
        evt.Skip()

    def OnDele(self,evt):
        selected_list = []
        item = self.path_list_ctrl.GetFirstSelected()
        while item >= 0:
            selected_list.append(item)
            item = self.path_list_ctrl.GetNextSelected(item)

        for i in range(0,len(selected_list)):
            self.path_list_ctrl.DeleteItem(selected_list[i] - i)
            del(self.own_list[selected_list[i] - i])

    def OnAdd(self,evt):
        dlg = wx.TextEntryDialog(None,u"请输入新文档位置", u"输入源码位置", "", style=wx.OK|wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetValue()
            if os.path.isdir(path):
                self.path_list_ctrl.InsertStringItem(len(self.own_list), path)
                self.own_list.append(path)
            else:
                dlg = wx.MessageDialog(None, u"请输入正确路径",u"输入错误",wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()

    def GetNewData(self):
        return self.own_list