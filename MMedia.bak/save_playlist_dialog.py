#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class SavePlaylistDialog( wx.Dialog ):
	def __init__( self, parent, title ):
		wx.Dialog.__init__( self, parent=parent, title=title, size=(250, 100))

		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.playlist_name_ctrl = wx.TextCtrl( panel)
		dataSizer = wx.FlexGridSizer( 1, 2 )
		dataSizer.AddMany([
			wx.StaticText( panel, label='Playlist Name:' ), ( self.playlist_name_ctrl, 1, wx.EXPAND )
			])
		
		dataSizer.AddGrowableCol(1, 1)
		panel.SetSizer( dataSizer )
		
		hbox2 = wx.StdDialogButtonSizer() #wx.BoxSizer(wx.HORIZONTAL)
		okButton = wx.Button(self, wx.ID_OK, '')
		closeButton = wx.Button(self, wx.ID_CANCEL, '')
		hbox2.AddButton(okButton)
		hbox2.AddButton(closeButton) #, flag=wx.LEFT, border=5)
		hbox2.SetAffirmativeButton(okButton)
		hbox2.SetCancelButton(closeButton)
		hbox2.Realize()

		vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
		vbox.Add(hbox2, flag= wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

		self.SetSizer(vbox)

		okButton.Bind(wx.EVT_BUTTON, self.OnOk)
		closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

	def OnOk( self,e ):
		self.EndModal(e.GetId())
			
	def OnClose(self, e):
		self.Destroy()
		
	def GetPlaylistName( self ):
		return self.playlist_name_ctrl.GetValue().strip()
		
