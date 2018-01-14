#!/usr/bin/python
# -*- coding: utf-8 -*-

# fmradio_gui.py

import wx
import sys
import os
import time
import pprint
import wx.lib.platebtn as platebtn
import wx.lib.buttons as libButtons
from state import *
from settings import *
from radio import *
from sounds import *
from CarPC_RDSDecoderListener import *
from wx.lib.pubsub import Publisher

#import traceback

class FMRadioGui(wx.Frame):

	def __init__(self, parent, title):	
		super(FMRadioGui, self).__init__(parent, title=title, size=(750, 420))

		self.numPadKeys = {}
		self.signalBarCount = 10
		self.signalBar = []
		self.stationSizers = []
		self.State = State()
		self.State.Load()
		self.Settings = Settings()
		self.Settings.Load()
		self.SpeedDialButtons = []
		self.stationList = StationList()
		self.stationList.Load()
		self.stationListButtons = []
		self.stationListButtonsBackgroundColour = wx.Colour(0,0,0)
		self.stationListButtonsForegroundColour = wx.Colour(0,0,0)

		#radio initialization must be executed before InitUI because the UI will use
		#radio properties for its own initialization
		self.radio = Radio( self.Settings.radioDevice, CarPC_RDSDecoderListener( self ), self.State.frequency )
		#self.radio = DemoRadio( self.State.frequency, self.Settings.MinAcceptableStationSignalStrength )

		self.zappIsOn = False
		self.ZappTimer = wx.Timer( self )
		self.zappCallback = None
				
		self.userSetMuteOn = self.radio.GetMute()
		
		self.InitUI()
		self.Centre()
		self.Show()
		
		self.__sounds = Sounds()
		
		self.scanUntilObserver = ScanUntilObserver( self )
		
		#the stations dictionary should be loaded from a file. For now get the hardcoded demo stations
		self.radio.AddFrequencyObserver( FrequencyPanelObserver( self ) )
		self.radio.AddFrequencyObserver( self.State )
		self.radio.AddSignalStrengthObserver( SignalStrengthPanelObserver( self ) )
		self.radio.AddSignalStrengthObserver( self.scanUntilObserver )
		self.radio.AddStereoMonoObserver( StereoMonoPanelObserver( self ) )		
		
		self.scanTimer = wx.Timer( self )
		self.Bind(wx.EVT_TIMER, self.Scan, self.scanTimer)
		
		self.setSpeedDialTimer = wx.Timer( self )
		self.Bind( wx.EVT_TIMER, self.SetSpeedDialTimerFinished, self.setSpeedDialTimer )
		# self.unsetSpeedDialTimer = wx.Timer( self )
		# self.Bind( wx.EVT_TIMER, self.ResetUnsetSpeedDialTimer, self.unsetSpeedDialTimer )
		self.cancelSpeedDialTimer = wx.Timer( self )
		self.Bind( wx.EVT_TIMER, self.CancelSpeedDialTimerFinished, self.cancelSpeedDialTimer )

		self.ScanTimer = wx.Timer( self )
		self.Bind( wx.EVT_TIMER, self.Scan, self.ScanTimer )		
		
		#self.RefreshDisplayTimer = wx.Timer( self )
		#self.Bind( wx.EVT_TIMER, self.RefreshDisplay, self.RefreshDisplayTimer )		
		#self.RefreshDisplayTimer.Start( self.Settings.RefreshDisplayMillisecs, True )
		
		Publisher().subscribe(self.UpdateRDSDisplay, "update_rds")
		
		self.Tune( self.State.frequency )		
				
	def InitUI(self):

		panel = wx.Panel(self)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		panel.SetSizer( sizer )

		lbox = wx.BoxSizer( wx.VERTICAL )
		sizer.Add( lbox, 5, wx.EXPAND, 2 )

		#sizer.Add(  wx.StaticLine( panel, style=wx.LI_VERTICAL ), 1, wx.EXPAND|wx.ALL, 0 )
		self.rbox = wx.BoxSizer(wx.VERTICAL)
		sizer.Add( self.rbox, 2, wx.EXPAND, 2 )

		self.numListButton = wx.Button( panel, id=1, label='Numeric/Stations' )
		self.Bind( wx.EVT_BUTTON, self.ToggleNumericStationList, id=1)
		#settingsButton = wx.BitmapButton( panel, bitmap=GetImage("gears.png", size='24x24') )
		buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
		buttonSizer.Add( self.numListButton, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10 )
		#buttonSizer.Add( settingsButton, 0, wx.ALL, 5 )
		self.rbox.Add( buttonSizer, 0, wx.EXPAND )

		self.numPanel = wx.Panel( panel )
		self.numSizer = wx.BoxSizer( wx.VERTICAL )
		self.numPanel.SetSizer( self.numSizer )
		self.rbox.Add( self.numPanel, 1, wx.EXPAND )

		numTextPanel = wx.Panel( self.numPanel )
		numTextPanel.SetBackgroundColour( self.Settings.NumericFreqFontBackgroundColor )
		numTextPanelS = wx.BoxSizer( wx.VERTICAL )
		numTextInnerSizer = wx.BoxSizer( wx.HORIZONTAL )
		numTextPanel.SetSizer( numTextPanelS )

		self.numText = wx.StaticText( numTextPanel, label = '555.55' )# str( self.State.frequency ) )
		self.numText.SetFont( self.Settings.NumericFreqFont.GetFont() )
		self.numText.SetForegroundColour(self.Settings.NumericFreqFont.Color)
		numTextPanelS.Add( numTextInnerSizer, 1, wx.EXPAND|wx.CENTRE, border = 5 )

		self.numTextWarningImage = wx.StaticBitmap( numTextPanel, wx.ID_ANY, GetImage( 'warning.png', '32x32' ) )
		numTextInnerSizer.Add( self.numTextWarningImage, 0, wx.ALL, border = 2 )
		self.numTextWarningImage.Hide()
		numTextInnerSizer.Add( (0,0),1,wx.EXPAND)
		numTextInnerSizer.Add( self.numText, 0, wx.ALIGN_RIGHT|wx.RIGHT, border = 10 )		

		row1s = wx.BoxSizer( wx.HORIZONTAL )
		row1s.Add( self.CreateNumPadKey( str( '7' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row1s.Add( self.CreateNumPadKey( str( '8' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row1s.Add( self.CreateNumPadKey( str( '9' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s = wx.BoxSizer( wx.HORIZONTAL )
		row2s.Add( self.CreateNumPadKey( str( '4' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s.Add( self.CreateNumPadKey( str( '5' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s.Add( self.CreateNumPadKey( str( '6' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s = wx.BoxSizer( wx.HORIZONTAL )
		row3s.Add( self.CreateNumPadKey( str( '1' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s.Add( self.CreateNumPadKey( str( '2' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s.Add( self.CreateNumPadKey( str( '3' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row4s = wx.BoxSizer( wx.HORIZONTAL )
		row4s.Add( self.CreateNumPadKey( str( '0' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row4s.Add( self.CreateNumPadKey( str( '.' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row4s.Add( self.CreateNumPadKey( str( 'Del' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row5s = wx.BoxSizer( wx.HORIZONTAL )
		row5s.Add( self.CreateNumPadKey( str( 'Enter' ) ), 2, wx.EXPAND|wx.ALL, 5 )		
		row5s.Add( self.CreateNumPadKey( str( 'Clear' ) ), 1, wx.EXPAND|wx.ALL, 5 )		

		self.numSizer.Add( numTextPanel, 1, wx.EXPAND|wx.ALL, 10 )
		self.numSizer.Add( row1s, 1, wx.EXPAND )
		self.numSizer.Add( row2s, 1, wx.EXPAND )
		self.numSizer.Add( row3s, 1, wx.EXPAND )
		self.numSizer.Add( row4s, 1, wx.EXPAND )
		self.numSizer.Add( row5s, 1, wx.EXPAND )

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
		stationListPreviousButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("nav_up_blue.png") )
		stationListPreviousButton.Bind( wx.EVT_LEFT_UP, self.TunePreviousListStation )
		stationListNextButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("nav_down_blue.png") )
		stationListNextButton.Bind( wx.EVT_LEFT_UP, self.TuneNextListStation )
		stationListNavSizer = wx.BoxSizer( wx.HORIZONTAL )
		stationListAddButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("add_blue.png") )
		stationListAddButton.Bind( wx.EVT_LEFT_UP, self.AddListStation )
		stationListDelButton = wx.StaticBitmap( self.stationPanel, bitmap=GetImage("delete_blue.png") )
		stationListDelButton.Bind( wx.EVT_LEFT_UP, self.DelListStation )
		stationListNavSizer = wx.BoxSizer( wx.HORIZONTAL )
		stationListNavSizer.Add( stationListPreviousButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListNextButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListAddButton, 0, wx.ALIGN_CENTRE, 5 )
		stationListNavSizer.Add( stationListDelButton, 0, wx.ALIGN_CENTRE, 5 )
		self.stationSizer.Add( stationListNavSizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
		if self.State.selector == State.STATIONSELECTOR:
			self.numPanel.Hide() 
		else: 
			self.stationPanel.Hide()

		speedDialSizer = wx.BoxSizer( wx.VERTICAL )
		#scanSizer = wx.GridBagSizer( 1, 10 )
		scanSizer = wx.BoxSizer( wx.HORIZONTAL )
		displayPanel = wx.Panel( panel )
		displayPanel.SetBackgroundColour( '#000000' )
		displaySizer = wx.BoxSizer( wx.HORIZONTAL )
		displayPanel.SetSizer( displaySizer )
		#lbox.Add( displaySizer, 7, wx.EXPAND, 10 )
		lbox.Add( displayPanel, 7, wx.EXPAND, 10 )
		#lbox.Add( wx.StaticLine( panel ), 1, wx.EXPAND )
		lbox.Add( scanSizer, 3, wx.EXPAND|wx.ALL, 5 )
		#lbox.Add( wx.StaticLine( panel ), 1, wx.EXPAND )
		lbox.Add( speedDialSizer, 5, wx.EXPAND, 5 )

		stationIndex = 1
		speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
		speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
				
		for i in range( 0, self.Settings.SpeedDialRows ):
			stationSizer = wx.BoxSizer( wx.HORIZONTAL )
			for k in range( 0, self.Settings.StationsPerSpeedDialRow ):
				stationButton = wx.ToggleButton( panel, label=str( stationIndex ) )
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
				 
		spaceX = 10
		spaceY = 1
		#self.MuteButton = wx.BitmapButton( panel, id=2, 
			#bitmap=GetImage("mute.png") if self.radio.GetMute() else GetImage("unmute.png") )
		#self.Bind( wx.EVT_BUTTON, self.ToggleMute, id=2)
		#scanSizer.Add( self.MuteButton, wx.EXPAND|wx.ALL, 5)
		zappButton = wx.BitmapButton( panel, bitmap=( GetImage( "media_play.png" ) if self.zappIsOn else GetImage( "media_stop.png" ) ) )
		zappButton.Bind( wx.EVT_BUTTON, self.ToggleZapp )
		scanSizer.Add( zappButton, wx.EXPAND|wx.ALL, 5)
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		scanBackButton = wx.BitmapButton( panel, id=111, bitmap=GetImage("media_beginning.png") )
		scanBackButton.Bind( wx.EVT_BUTTON, self.ScanBackward )
		scanSizer.Add( scanBackButton, wx.EXPAND|wx.ALL, 5 )
		scanForwardButton = wx.BitmapButton( panel, bitmap=GetImage("media_end.png") )
		scanForwardButton.Bind( wx.EVT_BUTTON, self.ScanForward )
		scanSizer.Add( scanForwardButton, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		scanManualBackwardButton = wx.BitmapButton( panel, bitmap=GetImage("media_rewind.png") )
		scanManualBackwardButton.Bind( wx.EVT_LEFT_DOWN, self.ScanManualBackStart )
		scanManualBackwardButton.Bind( wx.EVT_LEFT_UP, self.ScanManualBackStop )
		scanManualBackwardButton.Bind( wx.EVT_BUTTON, self.ScanManualBack )
		scanManualForwardButton = wx.BitmapButton( panel, bitmap=GetImage("media_fast_forward.png") )		
		scanManualForwardButton.Bind( wx.EVT_LEFT_DOWN, self.ScanManualForwardStart )
		scanManualForwardButton.Bind( wx.EVT_LEFT_UP, self.ScanManualForwardStop )
		scanManualForwardButton.Bind( wx.EVT_BUTTON, self.ScanManualForward )
		scanSizer.Add( scanManualBackwardButton, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( scanManualForwardButton, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( (spaceX, spaceY), 0, 0, 0 )
		speedDialBack = wx.BitmapButton( panel, bitmap=GetImage("media_step_back.png") ) 
		speedDialBack.Bind( wx.EVT_BUTTON, self.SpeedDialBack )
		speedDialForward = wx.BitmapButton( panel, bitmap=GetImage("media_step_forward.png") )
		speedDialForward.Bind( wx.EVT_BUTTON, self.SpeedDialForward )
		scanSizer.Add( speedDialBack, wx.EXPAND|wx.ALL, 5 )
		scanSizer.Add( speedDialForward, wx.EXPAND|wx.ALL, 5 )		
		   
		radioSizer = wx.BoxSizer( wx.HORIZONTAL )
		radioPanel = wx.Panel( panel )
		radioPanel.SetBackgroundColour( '#000000' )
		radioPanel.SetForegroundColour( '#ffff00' )
		radioPanel.SetSizer( radioSizer )

		self.volumeControl = VolumeControl( panel, self.Settings, self.radio )
		self.volumeControl.SetVolume( int( self.radio.GetVolume()/10 ) )
		displaySizer.Add( self.volumeControl.GetControlPanel(), 1, wx.EXPAND, border=5 )
		
		displaySizer.Add( self.BuildStereoMonoControl( panel ), 1, wx.EXPAND|wx.ALL, border=0 )
		
		rightDisplaySizer = wx.BoxSizer( wx.VERTICAL )
		displaySizer.Add( rightDisplaySizer, 3, wx.EXPAND, border=5 )
				
		rightDisplaySizer.Add( radioPanel, 5, wx.EXPAND )
		rightDisplaySizer.Add( self.BuildRDSDisplay( panel ), 2, wx.EXPAND | wx.RIGHT, border = 10 )
		
		radioSizer.Add( self.BuildFrequencyDisplay( radioPanel ), 1, wx.EXPAND|wx.ALL, border=10 )
		
		displaySizer.Add( self.BuildSignalControl( panel ), 1, wx.EXPAND|wx.ALL, border=10 )
		#radioSizer.Add( self.BuildSignalControl( radioPanel ), 1, wx.EXPAND| wx.RIGHT | wx.LEFT, border=10 )
		
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
		rdsSizer = wx.BoxSizer( wx.HORIZONTAL )
		rdsPanel = wx.Panel( panel )
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
		return rdsSizer
		
	def BuildSignalControl( self, panel ):
		controlPanel = wx.Panel( panel )
		controlPanel.SetBackgroundColour( '#000000' )
		controlPanel.SetForegroundColour( '#FFFF00' )
		
		signalSizer = wx.BoxSizer( wx.VERTICAL )
		controlPanel.SetSizer( signalSizer )
				
		self.signalText = wx.StaticText( controlPanel, label='0%' )
		signalGraphSizer = wx.BoxSizer( wx.VERTICAL )
		signalSizer.Add( signalGraphSizer, 1, wx.EXPAND|wx.ALL, 1 )
		for i in range( 0, self.signalBarCount ):
			self.signalBar.append( wx.Button( controlPanel )  )#, style=wx.NO_BORDER ) )
			signalGraphSizer.Add( self.signalBar[i], 1, wx.EXPAND|wx.ALL, 2 )
		signalGraphSizer.Add( self.signalText, 0, wx.ALIGN_CENTRE|wx.ALL, 0  )
		return controlPanel 
		
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
			bitmap=GetImage("mute.png") if self.radio.GetMute() else GetImage("unmute.png") )
		muteButton.Bind( wx.EVT_LEFT_UP, self.ToggleMute )
		self.audioSizer.Add( muteButton, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE, border=5 )
		return controlPanel
		
	def BuildStationListGUI( self ):
		del self.stationListButtons[:]
		self.stationListStationContainerSizer.Clear( True )
		keys = sorted( self.stationList.stations.keys(), key = float )
		# #print repr( keys ) #repr( keys )
		stationListButtonsIndex = 0
		for key in keys:
			wind = platebtn.PlateButton(self.scrollingStationListWindow, 
				label=key+' Mhz - ' + self.stationList.stations[key],
				style = platebtn.PB_STYLE_GRADIENT | platebtn.PB_STYLE_SQUARE )
			wind.SetFont( self.Settings.StationListFont.GetFont() )
			wind.SetPressColor(	wx.Color(
				self.Settings.StationListPressColor[0],
				self.Settings.StationListPressColor[1], 
				self.Settings.StationListPressColor[2]) )
			wind.frequency = float( key )
			wind.index = stationListButtonsIndex
			wind.selected = False
			stationListButtonsIndex += 1
			wind.Bind( wx.EVT_BUTTON, self.TuneListStation )
			self.stationListButtons.append( wind )
			self.stationListButtonsBackgroundColour = wind.GetBackgroundColour()
			self.stationListButtonsForegroundColour = wind.GetForegroundColour()
			self.stationListStationContainerSizer.Add(wind, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=2)
		self.stationListStationContainerSizer.Layout()
	
	def AddListStation( self, event ):
		ad = AddStationDialog( None, title='Add Station', defaultFrequency = self.radio.frequency, 
			defaultStationName = 'Station' + str( len( self.stationList.stations ) ),
			MinFrequency = self.radio.MinFrequency, MaxFrequency = self.radio.MaxFrequency )
		if( ad.ShowModal() == wx.ID_OK ):
			print( 'Will add {}, {}'.format( ad.GetFrequency(), ad.GetStationName() ) )
			self.stationList.AddStation( ad.GetFrequency(), ad.GetStationName() )
			self.BuildStationListGUI()
		
		ad.Destroy() 
		
	def DelListStation( self, event ):
		selectedListStationButton = self.StationListFindSelected()
		if( selectedListStationButton is None ):
			self.__sounds.PlayCancel()
			return
			
		dial = wx.MessageDialog(None, 'Are you sure you want to delete ' +
			str( selectedListStationButton.frequency ) +'Mhz' +
			#' - ' + self.stationList[ str( selectedListStationButton.frequency ) ]+ 
			' ?', 'Delete station', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if( dial.ShowModal() == wx.ID_YES ):
			self.stationList.DeleteStation( selectedListStationButton.frequency )
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
		 		
	def ResetStationListButtons( self ):
		for i in self.stationListButtons:
			i.SetBackgroundColour( self.stationListButtonsBackgroundColour )
			i.SetForegroundColour( self.stationListButtonsForegroundColour )
			i.selected = False
			i.Refresh()
					
	def TuneListStation( self, event ):
		button = event.GetEventObject()
		self.StationListSelect( button )
		
	def StationListSelect( self, button ):
		self.ResetStationListButtons()
		button.SetBackgroundColour( self.Settings.StationListSelectedBackgroundColour )
		button.SetForegroundColour( self.Settings.StationListSelectedForegroundColour )
		button.selected = True
		button.Refresh()
		self.StationListScrollIntoView( button )
		self.scanUntilObserver.Stop() #stop any automatic scanning
		self.ResetSpeedDials()
		self.Tune( button.frequency )
		#print( 'Station List tune to {}MHz'.format( event.GetEventObject().frequency ) )
		
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
		self.scanUntilObserver.Stop() #stop any automatic scanning
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
		self.ZappStart( self.TunePreviousListStation )
		self.StationListSelectNext( False )
		
	def TuneNextListStation( self, event=None ):
		self.ZappStart( self.TuneNextListStation )
		self.StationListSelectNext( True )
		
	def CreateNumPadKey( self, label ):
		button = wx.Button( self.numPanel, label=label )
		button.Bind( wx.EVT_BUTTON, self.NumPadKeyPress )
		self.numPadKeys[ label ] =  button
		return button
		
	def NumPadKeyPress( self, event ):
		button = event.GetEventObject()
		buttonLabel = button.GetLabel()
		numText = self.numText.GetLabel()
		if( buttonLabel == 'Enter' ):
			frequency = float( numText )
			try:
				self.Tune( frequency )
				self.scanUntilObserver.Stop() #stop any automatic scanning
				self.ResetSpeedDials()
				self.numTextWarningImage.Hide()
			except:
				self.numTextWarningImage.Show()
				self.__sounds.PlayError()
				return
		elif( buttonLabel == 'Clear' ):
			numText = ''
		elif( buttonLabel == 'Del' ):
			if( len( numText ) > 0 ):
				numText = numText[:-1]
		else:
			decimalPointIndex = numText.find( '.' )
			decimalPointExists = ( decimalPointIndex > -1 )
			#only one decimal point allowed
			if( decimalPointExists and buttonLabel == '.' ):
				self.__sounds.PlayError()
				return
				
			#only up to 3 digits before, and 2 digits after decimal point are allowed
			# print( 'len( numText[decimalPointIndex:] ) => len( {}[{}:] ) => len({})={}'.format( 
				# numText, decimalPointIndex, numText[decimalPointIndex:], len( numText[decimalPointIndex:] ) ) )
			if( ( not decimalPointExists and len( numText ) == 3 and buttonLabel in '0123456789' ) or
				( decimalPointExists and len( numText[decimalPointIndex:] ) == 3 and buttonLabel in '0123456789' )
				):
				self.__sounds.PlayError()
				return
				
			numText += buttonLabel
						
		if( len( numText ) == 0 ):
			self.numTextWarningImage.Hide()
		else:
			# print( '{} <> {}MHz - {}MHz'.format( float( numText ), self.radio.MinFrequency, self.radio.MaxFrequency) )
			if( float( numText ) < self.radio.MinFrequency or float( numText ) > self.radio.MaxFrequency ):
				self.numTextWarningImage.Show()
			else:
				self.numTextWarningImage.Hide()

		self.numText.SetLabel( numText )
				
	def ToggleNumericStationList( self, event ):
		if self.State.selector == State.STATIONSELECTOR: #self.numListButton.GetValue():
			self.State.SetStationSelector( State.NUMERICSELECTOR )
			self.numPanel.Show()
			self.stationPanel.Hide()
		else:
			self.State.SetStationSelector( State.STATIONSELECTOR )
			self.numPanel.Hide()
			self.stationPanel.Show()
		self.rbox.Layout()

	def ToggleMute( self, event ):
		button = event.GetEventObject()
		if self.radio.GetMute():
			self.radio.SetMute( False )
			self.userSetMuteOn = False
			#self.State.SetMute( False )			
			#self.MuteButton.SetBitmapLabel( GetImage( "unmute.png" ) )
			button.SetBitmap( GetImage( "unmute.png" ) )
		else:
			self.radio.SetMute( True )
			self.userSetMuteOn = True
			#self.State.SetMute( True )
			#self.MuteButton.SetBitmapLabel( GetImage( "mute.png" ) )
			button.SetBitmap( GetImage( "mute.png" ) )

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
		
	def SetSignalStrength( self, signalStrength ):
		self.signalText.SetLabel( str( signalStrength ) + '%' )
		for i in range( 0, self.signalBarCount ):
			color = self.Settings.SignalBarBrightColor if ( (i+1)*10 ) <= signalStrength else self.Settings.SignalBarDimColor
			self.signalBar[ self.signalBarCount - i - 1 ].SetBackgroundColour( color )
			self.signalBar[ self.signalBarCount - i - 1 ].Refresh()
			
	def ResetSpeedDials( self, exceptButton = None ):
		for i in self.SpeedDialButtons:
			if  exceptButton is not None and i == exceptButton:
				continue
			i.SetValue( False )
		
	def ToggleSpeedDial( self, event ):
		#print( 'ToggleSpeedDial...' )
		button = event.GetEventObject()
		index = button.GetLabel()
		if( self.State.speedDials.has_key( index ) ):
			self.radio.Tune( self.State.speedDials[ index ] )
			self.ResetSpeedDials( button )
			self.scanUntilObserver.Stop() #stop any automatic scanning
		else:
			button.SetValue( False )
				
	def ScanBackward( self, event ):
		print( 'Scan backwards' )
		self.scanForward = False
		self.ResetSpeedDials()
		self.ScanUntil()
		
	def ScanForward( self, event ):
		print( 'Scan forward' )
		self.scanForward = True
		self.ResetSpeedDials()
		self.ScanUntil()
			
	def ScanUntil( self ):
		self.scanUntilObserver.Start()		
		
	def ScanManualBack( self, event ):
		print( 'Scan Manual Back' )
		self.scanForward = False
		self.scanUntilObserver.Stop() #stop any automatic scanning
		self.Scan()
		
	def ScanManualBackStart( self, event ):
		print( 'Scan Manual Back Start' )
		self.scanForward = False
		self.scanUntilObserver.Stop() #stop any automatic scanning
		self.ResetSpeedDials()
		self.scanTimer.Start(500)
		event.Skip()
		
	def ScanManualBackStop( self, event ):
		print( 'Scan Manual Back Stop' )
		self.scanTimer.Stop()
		event.Skip()
		
	def ScanManualForward( self, event ):
		print( 'Scan Manual Forward' )
		self.scanForward = True
		self.scanUntilObserver.Stop() #stop any automatic scanning
		self.Scan()
		
	def ScanManualForwardStart( self, event ):
		print( 'Scan manual forward Start' )
		self.scanForward = True
		self.scanUntilObserver.Stop() #stop any automatic scanning
		self.ResetSpeedDials()
		self.scanTimer.Start(500)
		event.Skip()
		
	def ScanManualForwardStop( self, event ):
		print( 'Scan manual forward Stop' )
		self.scanTimer.Stop()
		event.Skip()		
	
	def Scan( self, event = None ):		
		if( self.scanForward ):
			print( 'scanning forward...' )
			self.radio.IncreaseFrequency( self.Settings.ScanStepKHz )
		else:
			print( 'scanning backward...' )
			self.radio.DecreaseFrequency( self.Settings.ScanStepKHz )
		self.ResetSpeedDials()

	#def RefreshDisplay( self, event = None ):
		#if( not self.RefreshDisplayTimer.Start( self.Settings.RefreshDisplayMillisecs, True ) ):
			#print( 'Error! Could not start RefreshDisplayTimer' )
		#else:
			#print( 'Restarted RefreshDisplayTimer!' )
		#if( not self.userSetMuteOn ):
			#self.radio.SetMute( True )
		#self.radio.Refresh()
		#if( not self.userSetMuteOn ):
			#self.radio.SetMute( False )
		
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
									
		if( not self.setSpeedDialTimer.IsRunning() and self.cancelSpeedDialTimer.IsRunning() ):
			button = event.GetEventObject()
			index = button.GetLabel()
			
			speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
			speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
			button.SetFont( speedDialAssignedFont )
			button.Refresh()

			self.State.SetSpeedDial( index, self.radio.frequency )
			print( 'Setting speed dial {} : {}'.format( index, self.radio.frequency ) )
			
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

	# def ResetUnsetSpeedDialTimer( self, event = None ):
		# if( self.unsetSpeedDialTimer.IsRunning() ):
			# print( 'unsetSpeedDialTimer stopped!' )
			# self.unsetSpeedDialTimer.Stop()
			
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
		
	def Tune( self, frequency ):
		self.radio.Tune( frequency )
			
	def SetNumPadFrequency( self, frequency ):
		self.numText = frequency
		
	def EnableNumPadKeys( self, keys ):
		for k in keys:
			self.numPadKeys[k[0]].Enable( k[1] )

	def UpdateRDSDisplay( self, msg ):
		rdsText = msg.data
		#print( 'received rdsText:{}'.format( rdsText ) )
		try:
			self.rdsText.SetLabel( unicode( rdsText ) )
		except:
			#errors here involve non ascii character interpretation, no harm done, so pass
			pass
	
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
			self.radio.SetMute( True )
		
	def SystemUnmute( self ):
		if( not self.userSetMuteOn ):
			self.radio.SetMute( False )
		
class VolumeControl:
	def __init__( self, parentPanel, settings, radio ):
		self.settings = settings
		self.maxVolume = 10
		self.volume =  radio.GetVolume()
		self.step = 1
		self.parentPanel = wx.Panel( parentPanel )
		self.parentPanel.SetBackgroundColour( '#000000' )
		self.radio = radio
		
		#put them in a vertical sizer
		self.vsizer = wx.BoxSizer( wx.VERTICAL )
		self.volumeBar = []
		for i in range( 0, self.maxVolume ):
			self.volumeBar.append( wx.Button( self.parentPanel, size=(15,-1) )  )#, style=wx.NO_BORDER ) )
			self.vsizer.Add( self.volumeBar[i], 1, wx.ALL, 1 )

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
		
		self.controlSizer = wx.BoxSizer( wx.VERTICAL )
		volUpBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_up.png' ) )
		volUpBitmap.Bind( wx.EVT_LEFT_UP, self.IncreaseVolume )
		self.controlSizer.Add( volUpBitmap, 0, wx.ALIGN_CENTRE|wx.TOP, 10 )
		self.controlSizer.Add( hsizer, 1, wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL, 0 )
		volDownBitmap = wx.StaticBitmap( self.parentPanel, -1, GetImage( 'volume_down.png' ) )
		volDownBitmap.Bind( wx.EVT_LEFT_UP, self.DecreaseVolume )
		self.controlSizer.Add( volDownBitmap, 0, wx.ALIGN_CENTRE|wx.BOTTOM, 10 )
		self.parentPanel.SetSizer( self.controlSizer )
		
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
		self.radio.SetVolume( volume*10 )
		
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

class FrequencyPanelObserver:
	'''A class that will be notified when the states frequency changes'''
	
	def __init__( self, frame ):
		self.frame = frame
		
	def FrequencyIs( self, frequency ):
		#~ print( 'will update to freq {}'.format( frequency ) )
		self.frame.SetFrequencyText( frequency )
		self.frame.title = frequency
		station = self.frame.stationList.StationAt( frequency )
		if( station is not None ):
			self.frame.SetStationNameText( station )			
		else:
			self.frame.ClearStationNameText()	
		self.frame.Refresh()
		
class SignalStrengthPanelObserver:
	def __init__( self, frame ):
		self.frame = frame
		
	def SignalStrengthIs( self, signalStrength ):
		self.frame.SetSignalStrength( signalStrength )
		
class StereoMonoPanelObserver:
	def __init__( self, frame ):
		self.frame = frame
		
	def IsStereo( self, isStereo ):
		self.frame.SetStereoMono( isStereo )
		
class ScanUntilObserver:	
	FALLING = 0
	RISING = 1 
	MIN_FREQUENCY_SEPARATION = 0.25
	a = 0
	b = 0
	last = 0.0	
	
	def __init__( self, frame ):
		self.frame = frame
		self.running = False
		self.previousSignalStrength = 0
		self.previousFrequency = 0.0
		
	def Start( self ):
		# print( 'Started :)' )
		self.running = True
		self.previousSignalStrength = self.frame.radio.signalStrength
		self.previousFrequency = self.frame.radio.frequency
		self.mode = ScanUntilObserver.FALLING
		self.frame.SystemMute()
		ScanUntilObserver.last = self.frame.radio.frequency
		self.frame.Scan()
		
	def Stop( self ):
		# print( 'Stopped :(' )
		self.running = False
		self.frame.SystemUnmute()
			
	def SignalStrengthIs( self, signalStrength ):
		"""
		A station is recognized on the peak of signal strength
		(RISING -> FALLING) when the signal
		strength is high enough.
		"""
		if( not self.running ):
			return
		#print('')
		#print( '--------------------------' )
		#print( '{}: at {}MHz signal strength is {}%'.format( 
			#( 'Running...' if self.running else 'Not running!' ),
			#self.frame.radio.frequency, 
			#self.frame.radio.signalStrength ) )
		
		strength = self.frame.radio.signalStrength			
			
		#print( 'a:{} + b:{} + s:{} = {} ~ max:{}, f:{} - last:{} = {} ~ MIN_FREQUENCY_SEPARATION:{}'.format( ScanUntilObserver.a, ScanUntilObserver.b, strength, ScanUntilObserver.a + ScanUntilObserver.b + strength,
			#self.frame.radio.GetMaxSignalStrength(),
			#self.frame.radio.frequency, ScanUntilObserver.last,			
			#math.fabs( self.frame.radio.frequency - ScanUntilObserver.last ),
			#self.frame.Settings.ScanFrequencySeparationThresholdMHz ) )
		last3Strengths = ScanUntilObserver.a + ScanUntilObserver.b + strength
		if( ( last3Strengths > self.frame.radio.GetMaxSignalStrength() ) and
			last3Strengths > 0.8*self.frame.Settings.MinAcceptableStationSignalStrength and
			( math.fabs( self.frame.radio.frequency - ScanUntilObserver.last ) > 
			self.frame.Settings.ScanFrequencySeparationThresholdMHz ) 
			):
			#print( 'previous strength:{}%, current strength:{}%'.format( 
			#self.previousSignalStrength, strength ) )
			if( self.previousSignalStrength > strength ):			
				if( self.mode == ScanUntilObserver.RISING ):
					#print( 'found peak' )
					if( self.previousSignalStrength > self.frame.Settings.MinAcceptableStationSignalStrength ):
						self.Stop()					
						ScanUntilObserver.a = 0
						ScanUntilObserver.b = 0
						ScanUntilObserver.last = self.frame.radio.frequency
						self.frame.radio.Tune( self.previousFrequency )
						self.frame.ZappStart( self.Start )
						return				 
				else:
					#print( 'mode = FALLING' )
					self.mode = ScanUntilObserver.FALLING
			else:
				#print( 'mode = RISING' )
				self.mode = ScanUntilObserver.RISING
			
		ScanUntilObserver.a = ScanUntilObserver.b
		ScanUntilObserver.b = strength
		self.previousSignalStrength = strength
		self.previousFrequency = self.frame.radio.frequency
		self.frame.ScanTimer.Start( self.frame.Settings.ScanWaitTimeMSecs, True )
		return	
		
			
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
	
if __name__ == '__main__':
  
	app = wx.App()
	FMRadioGui(None, title="FM Radio")
	app.MainLoop()
