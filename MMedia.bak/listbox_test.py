#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class ListBoxTest( wx.Frame ):
	def __init__( self, parent, title ):
		wx.Frame.__init__(self, id=-1, name='', parent=parent, pos=wx.Point(358, 184), size=wx.Size(299, 387), style=wx.DEFAULT_FRAME_STYLE, title=u'ListBox Test' )
		self.SetClientSize(wx.Size(291, 347))
		self.SetBackgroundColour(wx.Colour(0, 128, 0))

		panel = wx.Panel( self )
		sizer = wx.BoxSizer( wx.VERTICAL )
		panel.SetSizer( sizer )
		
		mylist = wx.ListBox(panel,choices=['0','1','2','3','4','5','6','7','8','9','10'])
		#mylist.SetBackgroundColour(wx.Colour(255, 255, 128))
		mylist.SetSelection( 3 )
		sizer.Add( mylist )
		
		sizer.Add( wx.Button( panel, -1, label='Test' ) )
		
		self.Show()
		
if __name__ == '__main__':
	app = wx.App()
	ListBoxTest(None, title="ListBoxTest")
	app.MainLoop()
