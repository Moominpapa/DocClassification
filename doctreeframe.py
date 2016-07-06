#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""doc tree display and command response"""
__author__ = 'moominpapa'

import wx
import os
from docctrl import *

class ImageDisplay(wx.Frame):
#image window
    def __init__(self, parent,image_path):
        #define window position
        size = parent.Size
        pos = parent.GetPosition()
        pos[0] += size[0]
        wx.Frame.__init__(self,parent,-1,u'???', pos,(0,0))
        #load image
        self.load_image(image_path)

    def load_image(self,image_path):
        #features display
        panel = wx.Panel(self, -1)
        type_label = wx.StaticText(panel, -1, "Type")
        type_text = wx.TextCtrl(panel, -1,"Here is a looooooooooooooon")
        type_text.SetInsertionPoint(0) #���ò����
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
        sizer.Add(type_label, pos=(1,0), span=(1,1),border = 5)
        sizer.Add(type_text, pos=(1,2), span=(1,3))
        # sizer.Add(richLabel, pos=(14,0), span=(2,1), flag=wx.EXPAND)
        # sizer.Add(richText, pos=(14,2), span=(2,3), flag=wx.EXPAND)
        sizer.Add(bmp, pos=(2,0), span = (20,10),flag=wx.EXPAND)
        sizer.AddGrowableRow(15)
        panel.SetSizer(sizer)
        panel.Fit()

class MainFrame(wx.Frame):
    def __init__(self):
        #class tree  {name, keyword, tree node object}
        self.c_tree = []
        self.image_win = None
        self.docctrl=docctrl()
        wx.Frame.__init__(self, None, title="simple tree", size=(400, 700))
        # Create the tree
        self.tree = wx.TreeCtrl(self)
        # Add a root node
        root = self.tree.AddRoot(unicode(u"所有类别"))
        # Add nodes from our data set
        #self.AddTreeNodes(root, self.docctrl.update_doc_data())
        self.build_class_tree('',root, self.docctrl.get_class_definition())
        self.claasify_files(self.docctrl.get_files_list())

        #self.UpdateTree(root, self.docctrl.update_doc_data())
        # Expand the first level
        self.tree.Expand(root)
        # Bind some interesting events
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)

    #pc_str-parent class str, cd-class definition
    def build_class_tree(self, pc_str, parenttree, cd):
        for c_item in cd:
            if c_item:
                class_str = pc_str + '->' + c_item['name']
                sc_node = self.tree.AppendItem(parenttree, unicode(c_item['name']))
                self.c_tree.append({'name':class_str, 'kw':c_item['kw'], 'node':sc_node})
                if c_item['sc']:
                    self.build_class_tree(class_str,sc_node, c_item['sc'])

    def classify_files(self, files_list):
        for file in files_list:
            for c in self.c_tree:



            print os.path.basename(file)


    #Type and Description window
    def UpdateTree(self,root,data):
        for type in data.keys():
            typenode = self.tree.AppendItem(root, unicode(type))
            for file in data[type]:
                id = wx.NewId()
                a = self.tree.pendItem(typenode, unicode(file['file']),data= wx.TreeItemData(file['path']))
                print file['file'],a

    def AddTreeNodes(self, parentItem, items):
        """
        Recursively traverses the data structure, adding tree nodes to
        match it.
        """
        for item in items:
            if type(item) == str or type(item) == unicode:
                a = self.tree.AppendItem(parentItem, unicode(item))
                print a.Getid()
            else:
                newItem = self.tree.AppendItem(parentItem, unicode(item[0]))
                b = self.AddTreeNodes(newItem, item[1])
                print b.Getid()

    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""

    def OnItemExpanded(self, evt):
        print "OnItemExpanded: ", self.GetItemText(evt.GetItem())

    def OnItemCollapsed(self, evt):
        print "OnItemCollapsed:", self.GetItemText(evt.GetItem())

    def OnSelChanged(self, evt):
        data =  self.tree.GetItemPyData(evt.GetItem())
        print "OnSelChanged: ", self.GetItemText(evt.GetItem()),data
        if data:
            if self.image_win == None:
                self.image_win = ImageDisplay(self, data)
            else:
                self.image_win.load_image(data)
            self.image_win.Show()

    def OnActivated(self, evt):
        print "OnActivated: ", self.GetItemText(evt.GetItem())

app = wx.PySimpleApp(redirect=True)
frame = MainFrame()
frame.Show()
app.MainLoop()
