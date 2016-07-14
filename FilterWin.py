#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx
import wx.calendar as cal
import datetime

class FilterWin(wx.Dialog):
    def __init__(self, owner_list, class_list):
        self.class_selections = []
        self.owner_selections = []
        self.class_selection_strings = []
        self.owner_selection_strings = []

        wx.Dialog.__init__(self, None, -1,u"文件过滤器",size=(1000, 2000))
        okButton = wx.Button(self, wx.ID_OK, u"确认", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, u"放弃", pos=(115, 15))
        class_list.insert(0, u"全选")
        owner_list.insert(0, u"全选")

        self.class_label = wx.StaticText(self, -1, u"类别")
        self.class_choice = wx.CheckListBox(self, -1, size = (150,100),choices=class_list)
        self.class_choice.SetChecked(range(0,len(class_list)))

        self.owner_label = wx.StaticText(self, -1, u"所有者")
        self.owner_choice = wx.CheckListBox(self, -1, size = (150,100),choices=owner_list)
        self.owner_choice.SetChecked(range(0,len(owner_list)))

        self.calstart_label = wx.StaticText(self, -1, u"起始时间")
        self.calstart = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_SHOW_HOLIDAYS| cal.CAL_SEQUENTIAL_MONTH_SELECTION)

        self.calend_label = wx.StaticText(self, -1, u"结束时间")
        self.calend = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_SHOW_HOLIDAYS| cal.CAL_SEQUENTIAL_MONTH_SELECTION)

        sizer = wx.GridBagSizer(hgap=5, vgap=0)
        sizer.Add(self.class_label, pos=(1,1), span=(1,1))
        sizer.Add(self.class_choice, pos=(2,1), span=(2,2))
        sizer.Add(self.owner_label, pos=(1,6), span=(1,1))
        sizer.Add(self.owner_choice, pos=(2,6), span=(2,2))
        sizer.Add(self.calstart_label, pos = (5,1), span = (1,1))
        sizer.Add(self.calstart, pos = (6,1), span = (3,3))
        sizer.Add(self.calend_label, pos = (5,6), span = (1,1))
        sizer.Add(self.calend, pos = (6,6), span = (3,3))

        sizer.Add(okButton, pos=(10,6))
        sizer.Add(cancelButton, pos=(10,7))
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_SHOW,self.OnWinShow,self)
        self.Bind(wx.EVT_BUTTON, self.OnOKClick, okButton)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckItem, self.class_choice)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckItem, self.owner_choice)


    def OnWinShow(self,evt):
        self.class_choice.SetChecked(self.class_selections)
        self.owner_choice.SetChecked(self.owner_selections)
        self.calstart.SetDate(self.calstart_time)
        self.calend_time.SetData(self.calend_time)
        evt.Skip()

    def OnOKClick(self,evt):
        self.class_selections = self.class_choice.GetChecked()
        self.owner_selections = self.owner_choice.GetChecked()
        self.class_selection_strings = self.class_choice.GetCheckedStrings()
        self.owner_selection_strings = self.owner_choice.GetCheckedStrings()
        self.calstart_time = self.calstart.GetDate()
        self.calend_time = self.calend.GetDate()
        evt.Skip()

    def OnCheckItem(self,evt):
        if evt.Selection == 0:
            if evt.EventObject.GetChecked()[0] == 0:
                evt.EventObject.SetChecked(range(0, evt.EventObject.GetCount()))
            else:
                evt.EventObject.SetChecked([])
        print evt.EventObject.GetChecked()

    def GetFilterData(self):
        return self.class_selection_strings, self.owner_selection_strings, (self.calstart_time.FormatISODate(),self.calend_time.FormatISODate())