#!/usr/bin/env python
"""A wxpython practice"""
__author__ = 'GYG'

import wx

class BitmapFrame(wx.Frame):
    """Frame class that displays an image."""
    def __init__(self,image,parent=None,id=-1,pos=wx.DefaultPosition,title='Hello,xwPython'):
        temp=image.ConvertToBitmap()
        size=temp.GetWidth(),temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,(1000,2000))
        self.bmp=wx.StaticBitmap(parent=self,bitmap=temp)

class App(wx.App):
    def OnInit(self):
        image=wx.Image('ASPdotNET_logo.jpg',wx.BITMAP_TYPE_JPEG)
        self.frame=BitmapFrame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def bitmap_demo():
    app = App()
    app.MainLoop()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class InsertFrame(wx.Frame):
    def __init__(self,parent=None,id=-1,pos=wx.DefaultPosition,title='Frame With Button'):

        #wx.Frame.__init__(self,parent,id,title,pos,(1000,2000))
        wx.Frame.__init__(self,parent,id,'Frame With Button',pos, (300,100))
        panel=wx.Panel(self,-1)
        button=wx.Button(panel,label="Close",pos=(0,0),size=(50,50))
        self.Bind(wx.EVT_BUTTON,self.OnCloseMe,button)
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)

    def OnCloseMe(self,event):
        self.Close(True)

    def OnCloseWindow(self,event):
        self.Destroy()

class App1(wx.App):
    def OnInit(self):
        self.frame=InsertFrame(parent=None,id=-1)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def button_demo():
    app = App1()
    app.MainLoop()

    #app = wx.PySimpleApp()
    #frame=InsertFrame(parent=None,id=-1)
    #frame.Show()
    #app.SetTopWindow(app)
    #app.MainLoop()

if __name__=='__main__':
    #bitmap_demo()
    button_demo()
