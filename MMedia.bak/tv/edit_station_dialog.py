#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class EditStationDialog( wx.Dialog ):
	def __init__( self, parent, title, station ):
		super(EditStationDialog, self).__init__(parent=parent, title=title, size=(250, 125))

		self.station = station
		
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.stationNameCtrl = wx.TextCtrl( panel)
		self.stationNameCtrl.AppendText( station.name )
		dataSizer = wx.FlexGridSizer( 1, 2 )
		dataSizer.AddMany([
			wx.StaticText( panel, label='Station Name:' ), ( self.stationNameCtrl, 1, wx.EXPAND )
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
		
	def GetStationName( self ):
		return self.stationNameCtrl.GetValue().strip()
		
