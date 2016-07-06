#!/usr/bin/env python
"""A wxpython practice"""
__author__ = 'GYG'

import wx

class App(wx.App):
    def OnInit(self):
        dlg = wx.MessageDialog(None, 'Is this the coolest thing ever!','MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        return True

if __name__=='__main__':
    app = App()
    app.MainLoop()