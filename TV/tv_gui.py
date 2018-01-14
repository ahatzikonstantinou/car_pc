#!/usr/bin/python
# -*- coding: utf-8 -*-

# tv_gui.py

import wx
import sys
import os
import time
import pprint
import wx.lib.platebtn as platebtn
import wx.lib.buttons as libButtons
from state import *
from settings import *
from stationList import *
from TV import *
from sounds import *
from ScanStationsDialog import *

import traceback

class TVGui(wx.Frame):

	def __init__(self, parent, title):
		try:
			super(TVGui, self).__init__(parent, title=title, size=(750, 420))
			
			self.stationSizers = []
			self.State = State()
			self.State.Load()
			self.Settings = Settings()
			self.Settings.Load()
			self.SpeedDialButtons = []
			self.device = TV()
			self.device.LoadChannels()
			self.tv = self.device #in some places in the code it makes more sense to refer to it as tv rather than device e.g. EditListStation where we call tv.SaveChannels()
			self.stationList = StationList()
			#self.stationList.Load()
			self.stationList.stations = self.device.channels
			self.stationListButtons = []
			self.stationListButtonsBackgroundColour = wx.Colour(0,0,0)
			self.stationListButtonsForegroundColour = wx.Colour(0,0,0)

			#device initialization must be executed before InitUI because the UI will use
			#device properties for its own initialization
			#self.device = Radio( self.Settings.radioDevice, CarPC_RDSDecoderListener( self ), self.State.frequency )
			#self.device = DemoRadio( self.State.frequency, self.Settings.MinAcceptableStationSignalStrength )			

			self.zappIsOn = False
			self.ZappTimer = wx.Timer( self )
			self.zappCallback = None
					
			self.imageSettingsIsOn = False

			self.VideoOnly = False
			
			self.InitUI()
			self.Centre()
			self.Show()
			
			self.tv.Start() #must be called after the show of the parent frame
						
			self.__sounds = Sounds()
					
			self.setSpeedDialTimer = wx.Timer( self )
			self.Bind( wx.EVT_TIMER, self.SetSpeedDialTimerFinished, self.setSpeedDialTimer )
			# self.unsetSpeedDialTimer = wx.Timer( self )
			# self.Bind( wx.EVT_TIMER, self.ResetUnsetSpeedDialTimer, self.unsetSpeedDialTimer )
			self.cancelSpeedDialTimer = wx.Timer( self )
			self.Bind( wx.EVT_TIMER, self.CancelSpeedDialTimerFinished, self.cancelSpeedDialTimer )

			#self.RefreshDisplayTimer = wx.Timer( self )
			#self.Bind( wx.EVT_TIMER, self.RefreshDisplay, self.RefreshDisplayTimer )		
			#self.RefreshDisplayTimer.Start( self.Settings.RefreshDisplayMillisecs, True )
			
			self.device.AddTuneObserver( self.State )
						
			if( self.tv.channels is not None and len( self.tv.channels ) > 0 ):
				channel = None
				if( self.State.channelHash in self.tv.channels ):
					channel = self.tv.channels[ self.State.channelHash ]
				else:
					channel = self.tv.channels.itervalues().next() #first channel in dictionary
				self.Tune( channel )
				self.StationListSetSelected( self.StationListFindButton( channel ) )
				
		except Exception, err:
			print traceback.format_exc()
				
	def InitUI(self):

		panel = wx.Panel(self)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		panel.SetSizer( self.sizer )

		lbox = wx.BoxSizer( wx.VERTICAL )
		self.sizer.Add( lbox, 5, wx.EXPAND, 2 )

		#sizer.Add(  wx.StaticLine( panel, style=wx.LI_VERTICAL ), 1, wx.EXPAND|wx.ALL, 0 )
		self.rbox = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add( self.rbox, 2, wx.EXPAND, 2 )

		self.stationPanel = wx.Panel( panel )
		self.stationSizer = wx.BoxSizer( wx.VERTICAL )
		self.stationPanel.SetSizer( self.stationSizer )
		self.rbox.Add( self.stationPanel, 1, wx.EXPAND )
		# self.stationListCtrl = wx.ListCtrl( self.stationPanel, -1, style=wx.LC_REPORT|wx.BORDER_SUNKEN )
		# self.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.StationListCtrlSelect, self.stationListCtrl )
		# self.stationListCtrl.InsertColumn(1, 'Station')
		# self.stationListCtrl.InsertColumn(0, 'MHz')

		# keys = sorted( self.stationList.stations.keys(), key = float )
		# #print repr( keys ) #repr( keys )
		# for key in keys:
			# freq = str( key )
			# stationName = self.stationList.stations[ freq ]
			# index = self.stationListCtrl.InsertStringItem( sys.maxint, freq )
			# self.stationListCtrl.SetStringItem(index, 1, stationName )
			
		# self.stationListCtrl.SetColumnWidth( 0, wx.LIST_AUTOSIZE )
		# self.stationListCtrl.SetColumnWidth( 1, wx.LIST_AUTOSIZE )

		# self.stationSizer.Add( self.stationListCtrl, 1, wx.EXPAND|wx.ALL, 5 )
		
		self.scrollingStationListWindow = wx.ScrolledWindow( self.stationPanel )
		self.scrollingStationListWindow.SetScrollRate(20,20)
		self.scrollingStationListWindow.EnableScrolling(True,True)
		sizer_container = wx.BoxSizer( wx.VERTICAL )
		self.stationListStationContainerSizer = wx.BoxSizer( wx.VERTICAL )
		sizer_container.Add(self.stationListStationContainerSizer,0,wx.ALL, border=0)
		self.BuildStationListGUI()
		self.scrollingStationListWindow.SetSizer(sizer_container)
		self.scrollingStationListWindow.SetBackgroundColour( self.Settings.StationListBackgroundColour )
		self.stationSizer.Add( self.scrollingStationListWindow, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 15 )
		
		#stationListPreviousButton = wx.BitmapButton( self.stationPanel, bitmap=GetImage("nav_up_blue.png") )
		#stationListPreviousButton.Bind( wx.EVT_BUTTON, self.TunePreviousListStation )
		#stationListPreviousButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("nav_up_blue.png") )
		#stationListPreviousButton.Bind( wx.EVT_LEFT_UP, self.TunePreviousListStation )
		#stationListNextButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("nav_down_blue.png") )
		#stationListNextButton.Bind( wx.EVT_LEFT_UP, self.TuneNextListStation )
		stationListNavSizer = wx.BoxSizer( wx.HORIZONTAL )
		stationListAddButton = wx.BitmapButton( self.stationPanel, bitmap=GetImage("edit.png") )
		stationListAddButton.Bind( wx.EVT_BUTTON, self.EditListStation )
		stationListDelButton = wx.BitmapButton( self.stationPanel, bitmap=GetImage("delete2.png") )
		stationListDelButton.Bind( wx.EVT_BUTTON, self.DelListStation )
		stationListScanButton = wx.BitmapButton( self.stationPanel, bitmap=GetImage("find.png") )
		stationListScanButton.Bind( wx.EVT_BUTTON, self.ScanListStation )
		stationListNavSizer = wx.BoxSizer( wx.HORIZONTAL )		
		#stationListNavSizer.Add( stationListPreviousButton, 0, wx.ALIGN_CENTRE, 5 )
		#stationListNavSizer.Add( stationListNextButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListAddButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListDelButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListScanButton, 0, wx.ALIGN_CENTRE, 5 )
		self.stationSizer.Add( stationListNavSizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		#sd_is_Sizer will include speedDialPanel and imageSettingsPanel. Only one of the two panels is visible
		self.speedDialPanel = wx.Panel( panel )
		#self.imageSettingsPanel = wx.Panel( panel )
		self.sd_is_Sizer = wx.BoxSizer( wx.VERTICAL )
		self.sd_is_Sizer.Add( self.speedDialPanel, 1, wx.EXPAND )
		#self.sd_is_Sizer.Add( self.imageSettingsPanel, 1, wx.EXPAND )
		#self.imageSettingsPanel.Hide()

		speedDialSizer = wx.BoxSizer( wx.VERTICAL )
		#scanSizer = wx.GridBagSizer( 1, 10 )
		self.scanPanel = wx.Panel( panel )
		scanSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.scanPanel.SetSizer( scanSizer )
		displayPanel = wx.Panel( panel )
		displayPanel.SetBackgroundColour( '#000000' )
		displaySizer = wx.BoxSizer( wx.HORIZONTAL )
		displayPanel.SetSizer( displaySizer )
		#lbox.Add( displaySizer, 7, wx.EXPAND, 10 )
		lbox.Add( displayPanel, 7, wx.EXPAND, 10 )
		#lbox.Add( wx.StaticLine( panel ), 1, wx.EXPAND )
		#lbox.Add( scanSizer, 3, wx.EXPAND|wx.ALL, 5 )
		lbox.Add( self.scanPanel, 3, wx.EXPAND|wx.ALL, 5 )
		#lbox.Add( wx.StaticLine( panel ), 1, wx.EXPAND )
		#lbox.Add( speedDialSizer, 5, wx.EXPAND, 5 )

		stationIndex = 1
		speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
		speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
				
		for i in range( 0, self.Settings.SpeedDialRows ):
			stationSizer = wx.BoxSizer( wx.HORIZONTAL )
			for k in range( 0, self.Settings.StationsPerSpeedDialRow ):
				stationButton = wx.ToggleButton( self.speedDialPanel, label=str( stationIndex ) )
				stationButton.SetFont( ( speedDialAssignedFont if self.State.speedDials.has_key( str( stationIndex ) )
					else speedDialUnassignedFont ) )
				stationButton.SetForegroundColour( self.Settings.SpeedDialAssignedFont.Color )
				stationButton.Bind( wx.EVT_TOGGLEBUTTON, self.ToggleSpeedDial )
				stationButton.Bind( wx.EVT_LEFT_DOWN, self.SetSpeedDialStart )
				stationButton.Bind( wx.EVT_LEFT_UP, self.SetSpeedDialStop )
				stationSizer.Add( stationButton, 1, wx.EXPAND|wx.ALL, 5 )
				self.SpeedDialButtons.append( stationButton )
				stationIndex += 1
			speedDialSizer.Add( stationSizer, 1, wx.EXPAND )
		
		self.speedDialPanel.SetSizer( speedDialSizer )		
		lbox.Add( self.sd_is_Sizer, 4, wx.EXPAND, 5 )

		spaceX = 10
		spaceY = 1
		muteButton = wx.BitmapButton( self.scanPanel, bitmap=GetImage("unmute.png") )
		muteButton.Bind( wx.EVT_BUTTON, self.ToggleMute )
		zappButton = wx.BitmapButton( self.scanPanel, bitmap=( GetImage( "media_play.png" ) if self.zappIsOn else GetImage( "media_stop.png" ) ) )
		zappButton.Bind( wx.EVT_BUTTON, self.ToggleZapp )
		speedDialBack = wx.BitmapButton( self.scanPanel, bitmap=GetImage("media_step_back.png") ) 
		speedDialBack.Bind( wx.EVT_BUTTON, self.SpeedDialBack )
		speedDialForward = wx.BitmapButton( self.scanPanel, bitmap=GetImage("media_step_forward.png") )
		speedDialForward.Bind( wx.EVT_BUTTON, self.SpeedDialForward )
		stationListPreviousButton = wx.BitmapButton( self.scanPanel, bitmap=GetImage("media_beginning.png") )
		stationListPreviousButton.Bind( wx.EVT_BUTTON, self.TunePreviousListStation )
		stationListNextButton = wx.BitmapButton( self.scanPanel, bitmap=GetImage("media_end.png") )
		stationListNextButton.Bind( wx.EVT_BUTTON, self.TuneNextListStation )		

		self.imageSettingsButton = wx.BitmapButton( self.scanPanel, bitmap=( GetImage( "gears.png" ) if self.imageSettingsIsOn else GetImage( "keyboard.png" ) ) )
		self.imageSettingsButton.Bind( wx.EVT_BUTTON, self.ToggleImageSettings )

		scanSizer.Add( muteButton, wx.EXPAND|wx.ALL, 5)
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )		
		scanSizer.Add( zappButton, wx.EXPAND|wx.ALL, 5)
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		scanSizer.Add( speedDialBack, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( speedDialForward, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		scanSizer.Add( stationListPreviousButton, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( stationListNextButton, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		scanSizer.Add( self.imageSettingsButton, wx.EXPAND|wx.ALL, 5 )		
		   
		radioSizer = wx.BoxSizer( wx.HORIZONTAL )
		radioPanel = wx.Panel( panel )
		radioPanel.SetBackgroundColour( '#000000' )
		radioPanel.SetForegroundColour( '#ffff00' )
		radioPanel.SetSizer( radioSizer )

		self.volumeControl = VolumeControl( panel, self.Settings, self.device )
		displaySizer.Add( self.volumeControl.GetControlPanel(), 1, wx.EXPAND, border=5 )
		
		#displaySizer.Add( self.BuildStereoMonoControl( panel ), 1, wx.EXPAND|wx.ALL, border=0 )
		
		rightDisplaySizer = wx.BoxSizer( wx.VERTICAL )
		displaySizer.Add( rightDisplaySizer, 3, wx.EXPAND, border=5 )
				
		rightDisplaySizer.Add( radioPanel, 5, wx.EXPAND )
		#rightDisplaySizer.Add( self.BuildRDSDisplay( panel ), 2, wx.EXPAND | wx.RIGHT, border = 10 )
		
		#radioSizer.Add( self.BuildFrequencyDisplay( radioPanel ), 1, wx.EXPAND|wx.ALL, border=10 )
		self.tv.InitUI( radioPanel, panel, self.State, self.State.Save, self.VideoPanelClick )		
		radioSizer.Add( self.tv.videopanel, 1, wx.EXPAND|wx.ALL, border=10 )
		self.sd_is_Sizer.Add( self.tv.controlspanel, 1, wx.EXPAND )
		self.sd_is_Sizer.Layout()
		self.tv.controlspanel.Hide()

		#code referring to tv.GetMute() must be called after self.tv.InitUI for a vlccontrol to exist
		self.device.SetMute( self.State.mute ) 
		if( self.State.mute ):
			muteButton.SetBitmapLabel( GetImage("mute.png") )
		self.volumeControl.SetVolume( self.State.volume/10 )
		self.device.AddVolumeObserver( self.State )		
		
	def VideoPanelClick( self ):
		'''Toggle show/hide all controls to leave only video full screen'''
		self.VideoOnly = not self.VideoOnly
		if( self.VideoOnly ):
			self.stationPanel.Hide()
			self.tv.controlspanel.Hide()
			self.tv.DisplayOnlyVideo( True )
			self.speedDialPanel.Hide()
			self.scanPanel.Hide()
			self.volumeControl.GetControlPanel().Hide()
			#self.rdsRootPanel.Hide()
		else:
			self.tv.DisplayOnlyVideo( False )
			self.stationPanel.Show()
			self.ShowSpeedDialPanel() #special purpose function here to handle iamge settings too
			self.scanPanel.Show()
			self.volumeControl.GetControlPanel().Show()
			#self.rdsRootPanel.Show()
		self.sizer.Layout()
				
	def BuildFrequencyDisplay( self, panel ):
		controlPanel = wx.Panel( panel )
		controlPanel.SetBackgroundColour( '#000000' )
		freqSizer = wx.BoxSizer( wx.VERTICAL )
		controlPanel.SetSizer( freqSizer )
		self.stationNameText = wx.StaticText( controlPanel )		
		self.freqText = wx.StaticText( controlPanel )
		freqStationTextFont = self.Settings.StationFreqFont.GetFont()
		nameStationTextFont = self.Settings.StationNameFont.GetFont()
		self.stationNameText.SetFont( nameStationTextFont )
		self.freqText.SetFont( freqStationTextFont )
		self.stationNameText.SetForegroundColour(self.Settings.StationNameFont.Color )
		self.freqText.SetForegroundColour(self.Settings.StationFreqFont.Color )
		
		freqSizer.Add( self.freqText, 0, wx.ALIGN_LEFT, border=0 )
		freqSizer.Add( self.stationNameText, 0, wx.ALIGN_LEFT, border=0 )
		
		return controlPanel
		
	def BuildRDSDisplay( self, panel ):
		self.rdsRootPanel = wx.Panel( panel )		
		rdsSizer = wx.BoxSizer( wx.HORIZONTAL )
		rdsPanel = wx.Panel( self.rdsRootPanel )
		rdsPanel.SetBackgroundColour( '#111111' )
		rdsPanelSV = wx.BoxSizer( wx.HORIZONTAL )
		rdsPanelS = wx.BoxSizer( wx.VERTICAL )
		rdsPanelSV.Add( rdsPanelS, 1, wx.ALIGN_CENTER )
		rdsPanel.SetSizer( rdsPanelSV )
		#rdsLabel = wx.StaticText( rdsPanel, label='RDS:' )
		#rdsLabel.SetFont( wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL) )
		#rdsLabel.SetForegroundColour(self.Settings.RDSFontColor)
		self.rdsText = wx.StaticText( rdsPanel, label='bla bla bla bla bla bla bla bla' )
		self.rdsText.SetFont( self.Settings.RDSFont.GetFont() )
		self.rdsText.SetForegroundColour(self.Settings.RDSFont.Color)
		#rdsPanelS.Add( rdsLabel, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 10 )
		rdsPanelS.Add( self.rdsText, 1, wx.ALIGN_LEFT|wx.ALL, 10 )
		rdsSizer.Add( rdsPanel, 1, wx.EXPAND )
		#rdsSizer.Add( wx.StaticText( panel, label='RDS:' ), 1, wx.EXPAND, 5 )
		#rdsSizer.Add( wx.StaticText( panel, label='bla bla bla bla bla bla bla bla'), 1, wx.EXPAND, 5 )
		self.rdsRootPanel.SetSizer( rdsSizer )
		return self.rdsRootPanel	
		
	def BuildStereoMonoControl( self, panel ):
		controlPanel = wx.Panel( panel )
		controlPanel.SetBackgroundColour( '#000000' )
		
		self.audioSizer = wx.BoxSizer( wx.VERTICAL )
		controlPanel.SetSizer( self.audioSizer )
		self.stereoPanel = wx.Panel( controlPanel )
		self.stereoPanel.SetBackgroundColour( '#000000' )
		stereoSizer = wx.BoxSizer( wx.VERTICAL )
		self.stereoPanel.SetSizer( stereoSizer )

		#a white text inside a black panel that has a border and is inside a white panel
		#results in a white text with white border over a black background
		self.whiteBorderPanel = wx.Panel( self.stereoPanel )
		self.whiteBorderPanel.SetBackgroundColour( self.Settings.StereoMonoBrightColor )
		whiteBorderSizer = wx.BoxSizer( wx.VERTICAL )
		self.whiteBorderPanel.SetSizer( whiteBorderSizer )
		whiteBorderBlackPanel = wx.Panel( self.whiteBorderPanel )
		whiteBorderSizer.Add( whiteBorderBlackPanel, 0, wx.ALIGN_CENTRE | wx.ALL, 1 )
		whiteBorderBlackPanel.SetBackgroundColour( '#000000' )
		wbbps = wx.BoxSizer( wx.VERTICAL )
		whiteBorderBlackPanel.SetSizer( wbbps )
		self.stereoText = wx.StaticText( whiteBorderBlackPanel, label='STEREO' )
		wbbps.Add( self.stereoText, 0, wx.ALL|wx.ALIGN_CENTRE, 2 )
		self.stereoText.SetForegroundColour( self.Settings.StereoMonoBrightColor )
		stereoSizer.Add( self.whiteBorderPanel, 0, wx.ALIGN_CENTRE )
		
		self.monoPanel = wx.Panel( controlPanel )
		self.monoPanel.SetBackgroundColour( '#000000' )
		monoSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.monoPanel.SetSizer( monoSizer )
		self.monoText = wx.StaticText( self.monoPanel, label='MONO' )
		self.monoText.SetForegroundColour( self.Settings.StereoMonoBrightColor )
		monoSizer.Add( self.monoText, 0, wx.ALIGN_CENTRE )
		self.audioSizer.Add( self.stereoPanel, 0, wx.TOP|wx.ALIGN_CENTRE, border=35 )
		self.audioSizer.Add( (0,0),1,wx.EXPAND ) #add spacer
		self.audioSizer.Add( self.monoPanel, 0, wx.BOTTOM|wx.ALIGN_CENTRE, border=35 )
		
		self.audioSizer.Add( (0,0),2,wx.EXPAND ) #add spacer
		muteButton = wx.StaticBitmap( controlPanel, -1,
			bitmap=GetImage("mute.png") if self.device.GetMute() else GetImage("unmute.png") )
		muteButton.Bind( wx.EVT_LEFT_UP, self.ToggleMute )
		self.audioSizer.Add( muteButton, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE, border=5 )
		return controlPanel
		
	def BuildStationListGUI( self ):
		del self.stationListButtons[:]
		self.stationListStationContainerSizer.Clear( True )
		keys = sorted( self.stationList.stations.keys() )
		# #print repr( keys ) #repr( keys )
		stationListButtonsIndex = 0
		for key in keys:
			station = self.stationList.stations[key]
			wind = platebtn.PlateButton(self.scrollingStationListWindow, 
				label=station.name,
				style = platebtn.PB_STYLE_GRADIENT | platebtn.PB_STYLE_SQUARE )
			wind.SetFont( self.Settings.StationListFont.GetFont() )
			wind.SetPressColor(	wx.Color(
				self.Settings.StationListPressColor[0],
				self.Settings.StationListPressColor[1], 
				self.Settings.StationListPressColor[2]) )
			wind.station = station
			wind.index = stationListButtonsIndex
			wind.selected = False
			stationListButtonsIndex += 1
			wind.Bind( wx.EVT_LEFT_UP, self.TuneListStation )
			self.stationListButtons.append( wind )
			self.stationListButtonsBackgroundColour = wind.GetBackgroundColour()
			self.stationListButtonsForegroundColour = wind.GetForegroundColour()
			self.stationListStationContainerSizer.Add(wind, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=2)
		self.stationListStationContainerSizer.Layout()
	
	def EditListStation( self, event ):
		selectedButton = self.StationListFindSelected()
		if( selectedButton is None ):
			return
		station = selectedButton.station
		ad = EditStationDialog( None, title='Edit Station', station=station )
		if( ad.ShowModal() == wx.ID_OK ):
			station.name = ad.GetStationName()
			self.tv.SaveChannels()
			self.BuildStationListGUI()
		
		ad.Destroy() 
		
	def DelListStation( self, event ):
		selectedListStationButton = self.StationListFindSelected()
		if( selectedListStationButton is None ):
			self.__sounds.PlayCancel()
			return
			
		station = selectedListStationButton.station
		dial = wx.MessageDialog(None, 'Are you sure you want to delete ' +
			str( station.name ) +
			#' - ' + self.stationList[ str( selectedListStationButton.frequency ) ]+ 
			' ?', 'Delete station', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if( dial.ShowModal() == wx.ID_YES ):
			del self.tv.channels[ station.GetHash() ]
			self.tv.SaveChannels()
			self.stationList.stations = self.tv.channels
			self.BuildStationListGUI()
	
	def ScanListStation( self, event ):
		dlg = ScanStationsDialog( None, 'Scan Stations Test', self.tv.channels )
		if( dlg.ShowModal() == wx.ID_OK ):
			self.stationList.stations = dlg.stations
			self.tv.channels = dlg.stations
			self.tv.SaveChannels()
			self.BuildStationListGUI()
	
	def GetSpeedDialButton( self, index ):
		for i in self.SpeedDialButtons:
			if( i.GetLabel() == index ):
				return i
		
		return None
	
	def GetPushedSpeedDialButton( self ):
		for i in self.SpeedDialButtons:
			if( i.GetValue() ):
				return i
		
		return None
		
	def FireSpeedDialButtonClick( self, button ):
		# print( 'Firing for button{} (id:{})'.format( button.GetLabel(), button.GetId() ) )
		cmd = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED)
		cmd.SetEventObject(button)
		cmd.SetId(button.GetId())
		button.SetValue( True )
		self.ToggleSpeedDial( cmd )
		
	def FindNextKey( self, sortedKeys, key, forward ):
		pos = sortedKeys.index( key )
		if( forward ):
			pos += 1
			if( pos >= len( sortedKeys ) ):
				pos = 0
		else:
			pos -= 1 
			if( pos < 0 ):
				pos = len( sortedKeys ) - 1
		
		return sortedKeys[pos]
					
	def PushNextSpeedDialButton( self, forward ):
		if( len( self.State.speedDials ) == 0 ):
			# print( 'No speed dials' )
			return
			
		keys = sorted( self.State.speedDials.keys(), key = int )
		if( len( self.State.speedDials ) == 1 ):
			# print( '1 speed dial' )
			button = self.GetSpeedDialButton( keys[0] )
			if( button is not None and ( not button.GetValue() ) ):
				# print( 'Pushing speed dial button {}'.format( button.GetLabel() ) )
				self.FireSpeedDialButtonClick( button )
				return
			
		#more than 1 speeddials exist
		activeButton = self.GetPushedSpeedDialButton()
		
		# print( '{} speed dials'.format( len( self.State.speedDials ) ) )
		#no active button
		if( activeButton is None ):
			activateKey = ( keys[0] if forward else keys[len(keys)-1] )
			# print( 'No speed dial pushed. Pushing speed dial button {}'.format( activateKey ) )
			self.FireSpeedDialButtonClick( self.GetSpeedDialButton( activateKey ) )
			return
			
		nextKey = self.FindNextKey( keys,  activeButton.GetLabel(), forward )
		nextButton = self.GetSpeedDialButton( nextKey )
		# print( 'Current button:{}, next button:{}. Pushing next button'.format( 
			# activeButton.GetLabel(), nextButton.GetLabel() 
			# )
		# )
		self.FireSpeedDialButtonClick( nextButton )
		
	def SpeedDialBack( self, event=None ):
		self.ZappStart( self.SpeedDialBack )
		self.PushNextSpeedDialButton( False )
		
	def SpeedDialForward( self, event=None):
		self.ZappStart( self.SpeedDialForward )
		self.PushNextSpeedDialButton( True )

	def ToggleImageSettings( self, event ):
		self.imageSettingsIsOn = not self.imageSettingsIsOn
		self.ShowSpeedDialPanel()

	def ShowSpeedDialPanel( self ):
		button = self.imageSettingsButton
		if( self.imageSettingsIsOn ):
			button.SetBitmapLabel( GetImage( 'gears.png' ) )
			self.tv.controlspanel.Show()
			self.speedDialPanel.Hide()
		else:
			button.SetBitmapLabel( GetImage( 'keyboard.png' ) )		
			self.tv.controlspanel.Hide()
			self.speedDialPanel.Show()
		self.sd_is_Sizer.Layout()

	def ResetStationListButtons( self ):
		for i in self.stationListButtons:
			i.SetBackgroundColour( self.stationListButtonsBackgroundColour )
			i.SetForegroundColour( self.stationListButtonsForegroundColour )
			i.selected = False
			i.Refresh()
					
	def TuneListStation( self, event ):
		button = event.GetEventObject()
		#print( 'TuneListStation to station {0}'.format( button.station.name ) )
		self.StationListSelect( button )
		
	def StationListSelect( self, button ):
		self.StationListSetSelected( button )
		self.Tune( button.station )

	def StationListSetSelected( self, button = None  ):
		if( button is None ):
			return
		self.ResetStationListButtons()
		button.SetBackgroundColour( self.Settings.StationListSelectedBackgroundColour )
		button.SetForegroundColour( self.Settings.StationListSelectedForegroundColour )
		button.selected = True
		button.Refresh()
		self.StationListScrollIntoView( button )
		self.ResetSpeedDials()

	def StationListFindButton( self, channel ):
		button = None
		for b in self.stationListButtons:
			if( b.station == channel ):
				button = b
				break
		return button

	def StationListFindSelected( self ):
		selectedButtons = [ i for i in self.stationListButtons if i.selected ]
		if( len( selectedButtons ) > 0 ):
			return selectedButtons[0]
		#~ for i in self.stationListButtons:
			#~ if( i.GetBackgroundColour() == self.stationListButtonsBackgroundColour() ):
				#~ return i
		return None
		
	def StationListSelectNext( self, forward ):
		if( len( self.stationList.stations ) == 0 ):
			return

		nextItemIndex = 0
		itemIndex = -1
		item = self.StationListFindSelected()
		if( item is not None ):
			itemIndex = item.index
		#print( 'List selectedItem index:{}'.format( itemIndex ) )
		if( itemIndex != -1 ):
			if( forward ):
				nextItemIndex = ( itemIndex + 1 ) if ( itemIndex + 1 ) < len( self.stationList.stations ) else 0
			else:
				nextItemIndex = ( itemIndex - 1 ) if ( itemIndex - 1 ) >= 0 else ( len( self.stationList.stations ) - 1 )

		#print( 'Next {} itemIndex:{}'.format( 'next' if forward else 'previous', nextItemIndex ) )
		self.StationListSelect( [i for i in self.stationListButtons if i.index == nextItemIndex][0] )
		#~ self.Tune( float( self.stationListCtrl.GetItemText( nextItemIndex ) ) )
		self.ResetSpeedDials()
		
	def StationListScrollIntoView( self, button ):
		parentPosX, parentPosY = button.GetPosition()
		hx, hy = button.GetSizeTuple()
		overallPosY = ( button.index )* ( hy + 4 ) + 2
		clientSizeX, clientSizeY = self.scrollingStationListWindow.GetClientSize()

		rx, ry = self.scrollingStationListWindow.GetScrollPixelsPerUnit()
		unit = ry
		sx, sy = self.scrollingStationListWindow.GetViewStart()
		#~ magicNumber = 20		# Where did this value come from ?!
		sx = sx * rx #magicNumber
		sy = sy * ry #magicNumber

		#~ print( 'overallPosY:{}, parentPosY:{}, hy:{}, sy:{}, clientSizeY:{} '.format( 
			#~ overallPosY, parentPosY , hy, sy, clientSizeY ) )
		scrollPosY = overallPosY #parentPosY
		
		if( overallPosY + hy < clientSizeY ):
			#~ print( 'will scroll to the top' )
			self.scrollingStationListWindow.Scroll( 0, 0 )
		else:	
			if (parentPosY < 0 ): #sy ) :
				if( overallPosY + hy > clientSizeY ):
					#~ print( 'overallPosY + hy > clientSizeY' )
					scrollPosY = overallPosY - clientSizeY + 1.5*hy
				#~ print( 'parentPosY < sy Scroll( {}, {} )'.format( 0, scrollPosY/unit ) )
				self.scrollingStationListWindow.Scroll( 0, scrollPosY/unit )

		if ( parentPosX < sx ) :
			#~ print( 'parentPosX < sx Scroll( {}, {} )'.format( 0, -1 ) )
			self.scrollingStationListWindow.Scroll( 0, -1 )

		if (parentPosX + sx) > clientSizeX  :
			#~ print( '(parentPosX + sx) > clientSizeX Scroll( {}, {} )'.format( 0, -1 ) )
			self.scrollingStationListWindow.Scroll( 0, -1 )

		if (parentPosY + hy ) > clientSizeY : # - sy) > clientSizeY :
			#~ print( '(parentPosY + hy - sy) > clientSizeY Scroll( {}, {} )'.format( 0, scrollPosY/unit ) )
			self.scrollingStationListWindow.Scroll( 0, scrollPosY/unit )
		
	def TunePreviousListStation( self, event=None):
		print( 'Tuning to previous listed station' )
		self.ZappStart( self.TunePreviousListStation )
		self.StationListSelectNext( False )
		
	def TuneNextListStation( self, event=None ):
		print( 'Tuning to next listed station' )
		self.ZappStart( self.TuneNextListStation )
		self.StationListSelectNext( True )

	def ToggleMute( self, event ):
		button = event.GetEventObject()
		if self.State.mute:
			self.device.SetMute( False )
			self.State.SetMute( False )			
			button.SetBitmapLabel( GetImage( "unmute.png" ) )
			#button.SetBitmap( GetImage( "unmute.png" ) )
		else:
			self.device.SetMute( True )
			self.State.SetMute( True )
			#button.SetBitmap( GetImage( "mute.png" ) )
			button.SetBitmapLabel( GetImage( "mute.png" ) )			

	def SetStereoMono( self, isStereo ):
		#~ print( 'Updating isStereo:{}'.format( isStereo ) )
		if isStereo:
			self.stereoText.SetForegroundColour( self.Settings.StereoMonoBrightColor )
			self.whiteBorderPanel.SetBackgroundColour( self.Settings.StereoMonoBrightColor )
			self.monoText.SetForegroundColour( self.Settings.StereoMonoDimColor )
		else:
			self.stereoText.SetForegroundColour( self.Settings.StereoMonoDimColor )
			self.whiteBorderPanel.SetBackgroundColour( self.Settings.StereoMonoDimColor )
			self.monoText.SetForegroundColour( self.Settings.StereoMonoBrightColor )
		
		self.stereoText.Refresh()
		self.whiteBorderPanel.Refresh()
		self.monoText.Refresh()
				
	def SetFrequencyText( self, frequency ):
		self.freqText.SetLabel( str( frequency ) )
		
	def SetStationNameText( self, station ):
		text = station.decode( 'utf-8' )[:16] + '...' if len( station.decode( 'utf-8' ) ) > 18 else station
		self.stationNameText.SetLabel( text )
		
	def ClearStationNameText( self ):
		self.stationNameText.SetLabel( ' ' )
					
	def ResetSpeedDials( self, exceptButton = None ):
		for i in self.SpeedDialButtons:
			if  exceptButton is not None and i == exceptButton:
				continue
			i.SetValue( False )
		
	def ToggleSpeedDial( self, event ):
		#print( 'ToggleSpeedDial...' )
		button = event.GetEventObject()
		index = button.GetLabel()
		if( self.State.speedDials.has_key( index ) and self.stationList.stations.has_key( self.State.speedDials[ index ] ) ):
			channel = self.stationList.stations[ self.State.speedDials[ index ] ]
			self.Tune( channel )
			self.StationListSetSelected( self.StationListFindButton( channel ) )
			self.ResetSpeedDials( button )
		else:
			button.SetValue( False )							
		
	def SetSpeedDialStart( self, event ):
		print( 'SetSpeedDialStart...' )
		self.StartSpeedDialTimers()
		event.Skip()
			
	def SetSpeedDialStop( self, event ):
		print( 'SetSpeedDialStop! IsRunning cancel:{}, set:{}'.format( 
			self.cancelSpeedDialTimer.IsRunning(),
			# self.unsetSpeedDialTimer.IsRunning(),
			self.setSpeedDialTimer.IsRunning()
			) 
		)		
									
		if( not self.setSpeedDialTimer.IsRunning() and self.cancelSpeedDialTimer.IsRunning() and
			self.device.tunedChannel is not None ):
			button = event.GetEventObject()
			index = button.GetLabel()
			
			speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
			speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
			button.SetFont( speedDialAssignedFont )
			button.Refresh()

			self.State.SetSpeedDial( index )
			print( 'Setting speed dial {} : {}'.format( index, self.State.channelHash ) )
			
		self.ResetSpeedDialTimers()
		event.Skip()
		
	def StartSpeedDialTimers( self ):
		self.ResetSpeedDialTimers()
		if( not self.setSpeedDialTimer.Start( self.Settings.SetSpeedDialPressTimeSecs*1000, True ) ):
			print( 'Error! Could not start setSpeedDialTimer' )
		# if( not self.unsetSpeedDialTimer.Start( self.Settings.UnSetSpeedDialPressTimeSecs*1000, True ) ):
			# print( 'Error! Could not start unsetSpeedDialTimer' )
		if( not self.cancelSpeedDialTimer.Start( self.Settings.CancelSpeedDialPressTimeSecs*1000, True ) ):
			print( 'Error! Could not start cancelSpeedDialTimer' )
		print( 'Started timers to {} {} seconds respectively'.format( 
			self.Settings.SetSpeedDialPressTimeSecs,
			# self.Settings.UnSetSpeedDialPressTimeSecs,
			self.Settings.CancelSpeedDialPressTimeSecs )
			)
		
	def ResetSpeedDialTimers( self, event = None ):
		self.ResetSetSpeedDialTimer()
		# self.ResetUnsetSpeedDialTimer()
		self.ResetCancelSpeedDialTimer()
	
	def ResetSetSpeedDialTimer( self, event = None ):
		if( self.setSpeedDialTimer.IsRunning() ):
			print( 'setSpeedDialTimer stopped!' )
			self.setSpeedDialTimer.Stop()

	def ResetCancelSpeedDialTimer( self, event = None ):
		if( self.cancelSpeedDialTimer.IsRunning() ):
			print( 'cancelSpeedDialTimer stopped!' )
			self.cancelSpeedDialTimer.Stop()
			
	def CancelSpeedDialTimerFinished( self, event ):
		#self.RequestUserAttention( flags = wx.USER_ATTENTION_ERROR )
		# soundFile = os.getcwd() + '/sounds/' + 'CancelSpeedDial.wav'
		# sound = wx.Sound( soundFile )
		# if sound.IsOk():
			# sound.Play(wx.SOUND_ASYNC)
		# else:
			# wx.Bell()
		self.__sounds.PlayCancel()
		
	def SetSpeedDialTimerFinished( self, event ):
		#self.RequestUserAttention( flags = wx.USER_ATTENTION_INFO )
		# soundFile = os.getcwd() + '/sounds/' + 'SetSpeedDial.wav'
		# sound = wx.Sound( soundFile )
		# if sound.IsOk():
			# sound.Play(wx.SOUND_ASYNC)
		# else:
			# wx.Bell()
		self.__sounds.PlayComplete()
		
	def Tune( self, station ):
		self.device.Tune( station )
		#self.rdsText.SetLabel( unicode( station.name ) )
		self.SetTitle( 'TV - {0}'.format( station.name ) )
	
	def ToggleZapp( self, event ):
		self.zappIsOn = not self.zappIsOn
		button = event.GetEventObject()
		if( self.zappIsOn ):
			button.SetBitmapLabel( GetImage( 'media_play.png' ) )
		else:
			button.SetBitmapLabel( GetImage( 'media_stop.png' ) )
			
	def ZappStart( self, callback ):		
		if( self.zappIsOn ):
			self.zappCallback = callback
			self.Bind( wx.EVT_TIMER, self.ZappCoordinate, self.ZappTimer )
			self.ZappTimer.Start( self.Settings.zappTimerMSecs, True )
		
	def ZappCoordinate( self, event ):
		if( self.zappCallback is not None and self.zappIsOn ):
			self.zappCallback()
		
	def SystemMute( self ):
		if( not self.userSetMuteOn ):
			self.device.SetMute( True )
		
	def SystemUnmute( self ):
		if( not self.userSetMuteOn ):
			self.device.SetMute( False )
		
class VolumeControl:
	def __init__( self, parentPanel, settings, device ):
		self.settings = settings
		self.maxVolume = 10
		self.volume = 0		
		self.step = 1
		self.parentPanel = wx.Panel( parentPanel )
		self.parentPanel.SetBackgroundColour( '#000000' )
		self.device = device
		
		#put them in a vertical sizer
		self.vsizer = wx.BoxSizer( wx.VERTICAL )

		#add the volume up button
		volUpBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_up.png' ) )
		volUpBitmap.Bind( wx.EVT_LEFT_UP, self.IncreaseVolume )
		self.vsizer.Add( volUpBitmap, 0, wx.ALIGN_CENTRE|wx.TOP, 10 )

		#add the indicator bars
		self.volumeBar = []
		for i in range( 0, self.maxVolume ):
			self.volumeBar.append( wx.Button( self.parentPanel, size=(15,-1) )  )#, style=wx.NO_BORDER ) )
			self.vsizer.Add( self.volumeBar[i], 1, wx.ALL, 1 )

		#add the volume down button
		volDownBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_down.png' ) )
		volDownBitmap.Bind( wx.EVT_LEFT_UP, self.DecreaseVolume )
		self.vsizer.Add( volDownBitmap, 0, wx.ALIGN_CENTRE|wx.BOTTOM, 10 )

		#put the vertical sizer inside a horizontal sizer along with 
		#a left and right spacers
		hsizer = wx.BoxSizer( wx.HORIZONTAL )
		padding = 2
		hsizer.Add( (1,1), padding, wx.EXPAND, 0 )
		hsizer.Add( self.vsizer, 1, wx.EXPAND, 0 )
		self.Text = wx.StaticText( self.parentPanel, label=str(self.volume*10) + '%' )
		textSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.Text.SetForegroundColour( self.settings.onVolumeBackgroundColour )
		textSizer.Add( self.Text, 0, wx.ALIGN_CENTRE )
		hsizer.Add( textSizer, padding, wx.EXPAND )
		
		self.parentPanel.SetSizer( hsizer )

		#instead of the following volume buttons were placed in the same vertical sizer as the volume bars
		#self.controlSizer = wx.BoxSizer( wx.VERTICAL )
		#volUpBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_up.png' ) )
		#volUpBitmap.Bind( wx.EVT_LEFT_UP, self.IncreaseVolume )
		#self.controlSizer.Add( volUpBitmap, 0, wx.ALIGN_CENTRE|wx.TOP, 10 )
		#self.controlSizer.Add( hsizer, 1, wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL, 0 )
		#volDownBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_down.png' ) )
		#volDownBitmap.Bind( wx.EVT_LEFT_UP, self.DecreaseVolume )
		#self.controlSizer.Add( volDownBitmap, 0, wx.ALIGN_CENTRE|wx.BOTTOM, 10 )
		#self.parentPanel.SetSizer( self.controlSizer )
		
		#self.SetVolume( self.volume )
		
	def GetControlPanel( self ):
		return self.parentPanel
	
	def IncreaseVolume( self, event ):
		self.ChangeVolume( self.step )
		
	def DecreaseVolume( self, event ):
		self.ChangeVolume( -self.step )
		
	def SetVolume( self, volume ):
		self.volume = volume
		if( self.volume > self.maxVolume ):
			self.volume = self.maxVolume
		elif( self.volume < 0 ):
			self.volume = 0
			
		#print( 'volume:{}, self.volume:{}'.format( volume, self.volume ) )
		self.device.SetVolume( volume*10 )		
		
		for i in range( 0, self.maxVolume ):
			color = self.settings.onVolumeBackgroundColour if i <= self.volume-1 else self.settings.offVolumeBackgroundColour
			self.volumeBar[ self.maxVolume - i - 1 ].SetBackgroundColour( color )
			self.volumeBar[ self.maxVolume - i - 1 ].Refresh()
		self.Text.SetLabel( str( self.volume*10 ) + '%' )
		
	def ChangeVolume( self, step ):
		volume = step + self.volume
		if( volume > self.maxVolume ):
			volume = self.maxVolume
		elif( volume < 0 ):
			volume = 0
			
		self.SetVolume( volume )		

					
def GetImage( imageFile, size ='48x48' ):
	imageDir = os.getcwd() + '/images/' + size + '/'
	imageFile = imageDir + imageFile
	image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	
	return image
			
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
		
if __name__ == '__main__':
  
	app = wx.App()
	TVGui(None, title="TV")
	app.MainLoop()
