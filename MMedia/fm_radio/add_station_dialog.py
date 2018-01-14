#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class AddStationDialog( wx.Dialog ):
	def __init__( self, parent, title, defaultFrequency, defaultStationName, MinFrequency, MaxFrequency ):
		super(AddStationDialog, self).__init__(parent=parent, title=title, size=(250, 125))

		self.MinFrequency = MinFrequency
		self.MaxFrequency = MaxFrequency
		
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.frequencyCtrl = wx.TextCtrl( panel )
		self.frequencyCtrl.AppendText( str( defaultFrequency ) )
		self.stationNameCtrl = wx.TextCtrl( panel)
		self.stationNameCtrl.AppendText( defaultStationName )
		dataSizer = wx.FlexGridSizer( 2, 2 )
		dataSizer.AddMany([
			wx.StaticText( panel, label='MHz:' ), ( self.frequencyCtrl, 1, wx.EXPAND ),
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
		error = False
		try:
			# print( self.frequencyCtrl.GetValue() )
			frequency = float( self.frequencyCtrl.GetValue().strip() )
			# print( 'frequency:'+ str(frequency) )
			if( frequency < self.MinFrequency or frequency > self.MaxFrequency ):
				# print( 'Invalid frequency' )
				error = True
			else:
				self.EndModal(e.GetId())
		except Exception, e:
			# traceback.print_exc()
			# e = sys.exc_info()[0]
			# print( 'Exception %s', e )
			error = True
			
		if( error ):
			errorDlg = wx.MessageDialog(None, 
				'The number you entered is not a valid station frequency. Valid frequency range [{} - {}]'.format(
					self.MinFrequency, self.MaxFrequency ),
				'Error', wx.OK | wx.ICON_ERROR )
			errorDlg.ShowModal()
			
	def OnClose(self, e):
		self.Destroy()
		
	def GetFrequency( self ):
		return self.frequencyCtrl.GetValue().strip()
		
	def GetStationName( self ):
		return self.stationNameCtrl.GetValue().strip()