#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class PlayProgress:
	DEFAULT_TIME_TEXT = '00:00:00'
	def __init__( self, parent_panel ):
		self.parent_panel = parent_panel
		
		self._panel = wx.Panel( self.parent_panel )
		self._panel.SetBackgroundColour( '#000000' )
		self._panel.SetForegroundColour( '#ffff00' )
		self._sizer = wx.BoxSizer( wx.HORIZONTAL )
		self._panel.SetSizer( self._sizer )
		
		self._duration_Txt = wx.StaticText( self._panel, wx.ID_ANY, label = PlayProgress.DEFAULT_TIME_TEXT )
		self._current_time_Txt = wx.StaticText( self._panel, wx.ID_ANY, label = PlayProgress.DEFAULT_TIME_TEXT )		
		self._progressbar = wx.Gauge( self._panel, size = (-1,4 ), style = wx.GA_SMOOTH )
		self._progressbar.SetRange( 100 )
		self._progressbar.SetBackgroundColour( '#111111' )
		
		self._sizer.Add( self._current_time_Txt, 0, wx.RIGHT, border = 4 )
		self._sizer.Add( self._progressbar, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border = 0 )
		self._sizer.Add( self._duration_Txt, 0, wx.LEFT, border = 4 )
		
	def GetWidget( self ):
		return self._panel
		
	def SetPosition( self, position ):
		#print( 'PlayProgress will SetPosition to {}'.format( position ) )
		self._progressbar.SetValue( position )
		
	def SetTime( self, time ):
		#print( 'PlayProgress will SetTime to {}'.format( time ) )
		self._current_time_Txt.SetLabel( time )
		
	def SetDuration( self, duration ):
		#print( 'PlayProgress will SetDuration to {}'.format( duration ) )
		self._duration_Txt.SetLabel( duration )
		
	def Show( self ):
		#print( 'PlayProgress will show' )
		self._panel.Show()
		
	def Hide( self ):
		#print( 'PlayProgress will hide' )
		self._panel.Hide()
		
	def Reset( self ):
		self._duration_Txt.SetLabel( PlayProgress.DEFAULT_TIME_TEXT )
		self._current_time_Txt.SetLabel( PlayProgress.DEFAULT_TIME_TEXT )
		self._progressbar.SetValue( 0 )
		
