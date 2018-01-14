#!/usr/bin/python
# -*- coding: utf-8 -*-

# toggle_radio_button.py

import wx

class ToggleRadioButton( wx.ToggleButton ):
	'''A toggle button that is unpressed only when a sibling toggle button is pressed. Siblings are found in the same
	   parent panel. associated_widget is a widget that is shown when a ToggleRadioButton is pressed and hidden when 
	   it is unpressed.
	''' 
	def __init__( self, parent, ID=wx.ID_ANY, label='', pos=wx.DefaultPosition, 
		size=wx.DefaultSize, style=0, associated_object=None, associated_widget=None, press_callback=None, 
		pressed_background_colour = None,
		unpressed_background_colour = None,
		pressed_text_colour = None,
		unpressed_text_colour = None
		):
		#print( 'initialising parent:{0}, ID:{1}, pos:{2}, size:{3}, style:{4}'.format( str( parent ), str(ID), str( pos ), str( size ), str( style ) ) )
		wx.ToggleButton.__init__( self, parent, ID, label, pos, size, style )
		self.associated_object = associated_object
		self.associated_widget = associated_widget
		self.press_callback = press_callback
		self.pressed_background_colour = pressed_background_colour
		self.unpressed_background_colour = unpressed_background_colour
		self.pressed_text_colour = pressed_text_colour
		self.unpressed_text_colour = unpressed_text_colour
		self.Bind( wx.EVT_TOGGLEBUTTON, self.SetValue )

	def SetValue( self, on, event=None ):
		'''
		Buttons that are already pushed in will not be unpressed. They will be unpressed only if a
		sibling button is pushed.
		'''
		#Direct unpress is not allowed.
		if( not on ):
			return

		self.Press()
		if( event ):
			event.Skip()

	def Press( self ):
		super( ToggleRadioButton, self ).SetValue( True )
		if( self.associated_object and self.press_callback ):
				self.press_callback( self.associated_object )
				
		if( self.associated_widget ):
			self.associated_widget.Show()
			
			if( isinstance( self.associated_widget.GetParent(), wx.Panel ) and
				self.associated_widget.GetParent().GetSizer() 
				):
				self.associated_widget.GetParent().GetSizer().Layout()
		for b in self.GetParent().GetChildren():
			if( b == self or ( type( b ) != ToggleRadioButton ) ):					
				continue
			b.Unpress()
		if( self.pressed_background_colour ):
			self.SetBackgroundColour( self.pressed_background_colour )
		if( self.pressed_text_colour ):
			self.SetForegroundColour( self.pressed_text_colour )
		self.GetParent().GetSizer().Layout()		

	def Unpress( self ):
		super( ToggleRadioButton, self ).SetValue( False )
		#print( 'unpressed ToggleRadioButton{}'.format( self.GetLabel() ) )
		if( self.unpressed_background_colour ):
			self.SetBackgroundColour( self.unpressed_background_colour )
		elif( self.pressed_background_colour ):
			self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		if( self.unpressed_text_colour ):
			self.SetForegroundColour( self.unpressed_text_colour )
		elif( self.pressed_text_colour ):
			self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
			
		if( self.associated_widget ):
			self.associated_widget.Hide()
			if( isinstance( self.associated_widget.GetParent(), wx.Panel ) and
				self.associated_widget.GetParent().GetSizer() 
				):
				self.associated_widget.GetParent().GetSizer().Layout()
			self.GetParent().GetSizer().Layout()


#test
class TestFrame( wx.Frame ):
	def __init__(self, parent, title):	
		super(TestFrame, self).__init__(parent, title=title)

		panel = wx.Panel( self )
		sizer = wx.BoxSizer( wx.VERTICAL )
		panel.SetSizer( sizer )

		bpanel = wx.Panel( panel )
		bsizer = wx.BoxSizer( wx.HORIZONTAL )
		bpanel.SetSizer( bsizer )

		wpanel = wx.Panel( panel )
		wsizer = wx.BoxSizer( wx.HORIZONTAL )
		wpanel.SetSizer( wsizer )

		w1 = wx.Panel( wpanel )
		w1.SetBackgroundColour( '#00aaff' )
		w2 = wx.Button( wpanel, label='Test button' )
		w3 = wx.ListCtrl( wpanel, style=wx.LC_REPORT )
		w3.SetBackgroundColour( '#555555' )

		b1 = ToggleRadioButton( bpanel, label='Panel', associated_widget=w1 )
		b2 = ToggleRadioButton( bpanel, label='Button', associated_widget=w2 )
		b3 = ToggleRadioButton( bpanel, label='List', associated_widget=w3 )

		bsizer.Add( b1 )
		bsizer.Add( b2 )
		bsizer.Add( b3 )

		wsizer.Add( w1 )
		wsizer.Add( w2 )
		wsizer.Add( w3 )

		sizer.Add( bpanel, 0, wx.EXPAND | wx.ALL, 5 )
		sizer.Add( wpanel, 1, wx.EXPAND | wx.ALL, 5 )

		self.Show()

if __name__ == '__main__':	
	try:
		app = wx.App()
		TestFrame(None, title="ToggleRadioButton Test")
		app.MainLoop()
	except Exception, e:
		#traceback.print_exc()
		#e = sys.exc_info()[0]
		#print( 'Exception %s', e )
		import sys, traceback
		xc = traceback.format_exception(*sys.exc_info())
		wx.MessageBox(''.join(xc))
