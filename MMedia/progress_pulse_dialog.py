#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import time
import logging
from threading import Thread

class ProgressPulseDlg( wx.Dialog ):
	def __init__( self, parent, message, worker_method, worker_method_args=[], worker_method_kwargs={} ):
		wx.Dialog.__init__(self, id=-1, name='', parent=parent, size = (-1, 150 ), style=wx.DEFAULT_FRAME_STYLE|wx.NO_BORDER, title=message )
		
		self.parent = parent
		#panel = wx.Panel( self )
		vbox = wx.BoxSizer(wx.VERTICAL)
		#panel.SetSizer( vbox )
		
		self.progressCtrl = wx.Gauge( self, style = wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		
		#Cancelled. In python there is no way to kill a thread
		#cancelBtn = wx.Button( self, wx.ID_ANY, label = "Cancel" )
		#cancelBtn.Bind( wx.EVT_BUTTON, self.OnCancel )
		
		vbox.Add( wx.StaticText( self, label=message ), 0, wx.ALIGN_CENTRE_VERTICAL|wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 10 )
		vbox.Add( self.progressCtrl, 0, wx.ALIGN_CENTRE_VERTICAL|wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 10 )
		#vbox.Add( cancelBtn, 0, wx.CENTRE|wx.TOP|wx.BOTTOM, border = 10 )
		self.SetSizer(vbox)
		
		self.worker_thread = Thread( 
			target = worker_method, 
			args = worker_method_args, 
			kwargs = worker_method_kwargs, 
			group = None 
			) #group = None because some wird library assertion runs and complains about it if it is missing
			
	def Start( self ):
		self.worker_thread.start()
		
		th_pulse = Thread( target = self._Pulse, group = None )
		th_pulse.setDaemon( True )
		th_pulse.start()

		if( self.parent ):
			wx.CallAfter( self.parent.Disable )
		#self.SetBackgroundColour( '#886' )
		self.ShowModal()
		
	def Stop( self ):
		if( self.parent ):
			wx.CallAfter( self.parent.Enable )
		wx.CallAfter( self.Close )
		
	#def OnCancel( self, event ):
		#self.Stop()
		
	def _Pulse( self ):
		while( True ):
			try:
				if( not self.worker_thread.is_alive() ):
					#logging.debug( 'Pulse: the worker thread finished so I am done now' )
					#if( self.parent ):
						#wx.CallAfter( self.parent.Enable )
					#wx.CallAfter( self.Close )
					wx.CallAfter( self.Stop )
					break;
				#wx.CallLater( 1000, dlg.Pulse )
				wx.CallAfter( self.progressCtrl.Pulse )
				time.sleep( 0.05 )
			except:
				logging.debug( 'Pulse crashed, most probably the progress dialog closed' )
				break
		logging.debug( 'Pulse finished' )
		
		

if __name__ == '__main__':
	def TestMethod( text, options = '' ):
		for i in range( 0, 10 ):
			print '{} {} options: {}'.format( i, text, options )
			time.sleep( 1 )
			
	app = wx.App()
	frame = ProgressPulseDlg( 
		None, 
		'Test Progress', 
		TestMethod, 
		worker_method_args = [ 'Hello' ], 
		worker_method_kwargs = { 'options': 'a, b, c, d' } 
		)
	app.SetTopWindow(frame)
	frame.Start()
	app.MainLoop()
