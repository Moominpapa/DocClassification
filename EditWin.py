#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx
import wx.calendar as cal

class EditWin(wx.Dialog):
    def __init__(self, owner_list, class_list):
        self.class_selections = []
        self.owner_selections = []
        self.class_selection_strings = []
        self.owner_selection_strings = []

        wx.Dialog.__init__(self, None, -1,u"新建材料",size=(1000, 2000))
        okButton = wx.Button(self, wx.ID_OK, u"确认", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, u"放弃", pos=(115, 15))

        self.class_label = wx.StaticText(self, -1, u"类别")
        self.class_choice = wx.Choice(self, -1, size = (100,20),choices=class_list)

        self.owner_label = wx.StaticText(self, -1, u"所有者")
        self.owner_choice = wx.Choice(self, -1, size = (100,20),choices=owner_list)

        self.name_label = wx.StaticText(self, -1, u"文件名")
        self.name_text = wx.TextCtrl(self, -1,"")
        self.name_text.SetInsertionPoint(0)

        self.de_label = wx.StaticText(self, -1, u"描述")
        self.de_text = richText = wx.TextCtrl(self, -1,"", size=(300,100),style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.de_text.SetInsertionPoint(0)
        self.de_text.SetStyle(44, 52, wx.TextAttr("white", "black"))

        self.cal_label = wx.StaticText(self, -1, u"形成时间")
        self.cal = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_SHOW_HOLIDAYS| cal.CAL_SEQUENTIAL_MONTH_SELECTION)

        sizer = wx.GridBagSizer(hgap=5, vgap=10)
        sizer.Add(self.name_label, pos=(1,1), span=(1,1))
        sizer.Add(self.name_text, pos=(2,1), span=(1,2))
        sizer.Add(self.class_label, pos=(3,1), span=(1,1))
        sizer.Add(self.class_choice, pos=(4,1), span=(1,1))
        sizer.Add(self.owner_label, pos=(5,1), span=(1,1))
        sizer.Add(self.owner_choice, pos=(6,1), span=(1,1))
        sizer.Add(self.de_label, pos=(7,1), span=(1,1))
        sizer.Add(self.de_text, pos=(8,1), span=(2,3))
        sizer.Add(self.cal_label, pos = (10,1), span = (1,1))
        sizer.Add(self.cal, pos = (11,1), span = (3,3))
        sizer.Add(okButton, pos=(14,3))
        sizer.Add(cancelButton, pos=(14,4))
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_SHOW,self.OnWinShow,self)
        self.Bind(wx.EVT_BUTTON, self.OnOKClick, okButton)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckItem, self.class_choice)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckItem, self.owner_choice)

    def OnWinShow(self,evt):
        # self.class_choice.SetChecked(self.class_selections)
        # self.owner_choice.SetChecked(self.owner_selections)
        self.calstart.SetDate(self.calstart_time)
        self.calend_time.SetData(self.calend_time)
        evt.Skip()

    def OnOKClick(self,evt):
        # self.class_selections = self.class_choice.GetChecked()
        # self.owner_selections = self.owner_choice.GetChecked()
        # self.class_selection_strings = self.class_choice.GetCheckedStrings()
        # self.owner_selection_strings = self.owner_choice.GetCheckedStrings()
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
        return (self.class_selection_strings, self.owner_selection_strings, (self.calstart_time,self.calend_time))

if __name__ == '__main__':
    app = wx.PySimpleApp(redirect=True)
    frame = EditWin([],[])
    frame.Show()
    app.MainLoop()