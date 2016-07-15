#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx

class ImageWin(wx.Frame):
#image window
    def __init__(self, parent,image_path):
        #define window position
        size = parent.Size
        pos = parent.GetPosition()
        pos[0] += size[0]
        wx.Frame.__init__(self,parent,-1,u'文档', pos,(0,0))
        #load image
        self.load_image(image_path)

    def load_image(self,image_path):
        #features display
        panel = wx.Panel(self, -1)
        # type_label = wx.StaticText(panel, -1, "Type")
        # type_text = wx.TextCtrl(panel, -1,"Here is a looooooooooooooon")
        # type_text.SetInsertionPoint(0) #���ò����
        # richLabel = wx.StaticText(panel, -1, "Rich Text")
        # richText = wx.TextCtrl(panel, -1,"If supported by the native control, this is reversed, and this is a different font.", style=wx.TE_MULTILINE|wx.TE_RICH2) #�����ḻ�ı��ؼ�
        # richText.SetInsertionPoint(0)
        # richText.SetStyle(44, 52, wx.TextAttr("white", "black")) #�����ı���ʽ
        # points = richText.GetFont().GetPointSize()
        # f = wx.Font(points + 3, wx.ROMAN, wx.ITALIC, wx.BOLD, True) #����һ������
        # richText.SetStyle(68, 82, wx.TextAttr("blue", wx.NullColour, f)) #��������������ʽ

        # sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
        # sizer.Add(self.tree, 0, wx.EXPAND)
        # sizer.AddMany([multiLabel, multiText, richLabel, richText])

        image = wx.Image(image_path, type=wx.BITMAP_TYPE_ANY)
        temp = image.ConvertToBitmap()
        size= temp.GetWidth(),(temp.GetHeight() + 50)
        self.SetClientSize(size)
        bmp=wx.StaticBitmap(parent=panel,bitmap=temp)

        sizer = wx.GridBagSizer(hgap=0, vgap=0)
        # sizer.Add(type_label, pos=(1,0), span=(1,1),border = 5)
        # sizer.Add(type_text, pos=(1,2), span=(1,3))
        # sizer.Add(richLabel, pos=(14,0), span=(2,1), flag=wx.EXPAND)
        # sizer.Add(richText, pos=(14,2), span=(2,3), flag=wx.EXPAND)
        sizer.Add(bmp, pos=(2,0), span = (20,10),flag=wx.EXPAND)
        sizer.AddGrowableRow(15)
        panel.SetSizer(sizer)
        panel.Fit()