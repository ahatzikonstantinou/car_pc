#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import wx
#~ from threading import Timer
from stationList import *
from CarPC_RDSDecoderListener import *
import v4l2radio
import sys
import signal
from mixer_pulseaudio import *
from media_device import MediaDevice, MediaTrack
from media_player_device import MediaPlayerDevice
from add_station_dialog import *
from stationList import StationList
from radio_settings import *
from radio_state import *
#from gstreamer_players.radio_player import *
from radio_media_player import *
from device_behavior_on_activate import *

#_PULSEAUDIO_SOURCENAME = 'alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.iec958-stereo'
_PULSEAUDIO_SOURCENAME = 'pulse://alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo'

class RadioStation:
	def __init__( self, frequency, name ):
		self.frequency = frequency
		self.name = name

class Radio( MediaPlayerDevice ):
	def __init__( self, abstract_device, RDSListener, frequency = 87.5 ):
		MediaPlayerDevice.__init__( self, abstract_device )
		self.rds_listener = RDSListener
		self.frequency = frequency

		self.signalStrength = 0.0
		self.MaxFrequency = 108.0
		self.MinFrequency = 87.5
		self.frequencyObservers = []
		self.signalStrengthObservers = []
		self.stereoMonoObservers = []
		self.stationList = StationList()
		self.stationList.Load()
		
		self.tuner = None
		self._CreateTuner()
		self.scanTimer = wx.Timer( self._mmedia_gui )
		abstract_device._mmedia_gui.Bind(wx.EVT_TIMER, self.Scan, self.scanTimer)
		
		self.signalBarCount = 10
		self.signalBar = []

		self.scanUntilObserver = ScanUntilObserver( self._mmedia_gui, self )
		self.AddSignalStrengthObserver( SignalStrengthPanelObserver( self ) )
		self.AddSignalStrengthObserver( self.scanUntilObserver )
		self.AddFrequencyObserver( FrequencyPanelObserver( self ) )
		self.AddFrequencyObserver( self.state )

		self.Tune( self.state.frequency )
		
		# register signal handler for exiting
		def handler(signum, frame):
			#self.tuner.close()
			self.Deactivate()
			sys.exit(0)
		#
		signal.signal(signal.SIGINT, handler)
		
		#print( '--------Radio-----------\nself._dev_supports_media_function:' )
		#self.DumpDevMediaFunctions( self._dev_supports_media_function )
		#print( '\n\nself._dev_media_functions:' )
		#self.DumpDevMediaFunctions( self._dev_media_functions )
		#print( '--------Radio-----------\n' )
		#import sys ; sys.exit()

	def _CreateMediaPlayer( self ):
		return RadioMediaPlayer( playerLock = self._playerLock, pulseuadio_source = _PULSEAUDIO_SOURCENAME )
		
	def Tune( self, frequency ):
		#Perhaps a radio tuner usb is not present so no tuner object has been created. If so, exit
		if( self.tuner is None ):
			return

		if( frequency > self.MaxFrequency or frequency < self.MinFrequency ):
			raise Exception( 'Cannot tune at {}. Range: [{} - {}]'.format( 
				frequency, self.MinFrequency, self.MaxFrequency )
				)
		self.frequency = frequency
		self._current_track_hash = str( frequency )
		self.tuner.set_frequency( int( frequency * 1000 ) )
		self.state.SetFrequency( frequency )
		wx.CallAfter( self._mmedia_gui.ClearTextDisplayMessage )
		self.Refresh()
		self.UpdateObservers()

	def Refresh( self ):
		#Note that get_signal_strength reads multiple times the radio device
		#and refreshes the internal tuner info. So there is no further need
		#for refresh in order to get the sterero/mono mode
		self.signalStrength = self.tuner.get_signal_strength()
		self._is_stereo = self.tuner.get_stereo()
		#print( 'Stereo:{}'.format( self.isStereo ) )		
		self.UpdateSignalStrengthObservers()
		self.UpdateStereoMonoObservers()
		
	def UpdateObservers( self ):
		self.UpdateFrequencyObservers()
		#print( 'Finished UpdateFrequencyObservers' )
		self.UpdateSignalStrengthObservers()
		#print( 'Finished UpdateSignalStrengthObservers' )
		self.UpdateStereoMonoObservers()
		#print( 'Finished UpdateStereoMonoObservers' )
		pass
		
	def AddFrequencyObserver( self, observer ):
		self.frequencyObservers.append( observer )
		
	def UpdateFrequencyObservers( self ):
		for i in self.frequencyObservers:
			wx.CallAfter( i.FrequencyIs, self.frequency )

	def IncreaseFrequency( self, kHz ):		
		self.frequency += ( kHz / 1000.0 )
		print( 'Increase by {0} to {1}'.format( str( kHz / 1000.0 ), self.frequency ) )
		if self.frequency > self.MaxFrequency:
			self.frequency = self.MinFrequency
		self.Tune( self.frequency )
		
	def DecreaseFrequency( self, kHz ):
		self.frequency -= ( kHz / 1000.0 )
		print( 'Decrease by {0} to {1}'.format( str( kHz / 1000.0 ), self.frequency ) )
		if self.frequency < self.MinFrequency:
			self.frequency = self.MaxFrequency
		self.Tune( self.frequency )
		
	def GetMaxSignalStrength( self ):
		return self.tuner.MAX_SIGNAL_STRENGTH

	def _CreateTuner( self ):
		try:
			self.tuner = FMRadio( dev=self.dev_path )
			low, high = self.tuner.get_frequency_range()
			self.MinFrequency = low/1000.0
			self.MaxFrequency = high/1000.0
			if( self.rds_listener is not None ):
				self.tuner.rds.add_listener( self.rds_listener )
			self.is_active = True
			#self.Tune( self.state.frequency )
			print( 'Radio is active' )
		except FMRadioUnavailableError:
			error_msg = "FM radio device is unavailable"
			print error_msg
			self._ReportError( error_msg )
			self.is_active = False
			import sys, traceback; xc = traceback.format_exception(*sys.exc_info()); print( ''.join(xc) )
			return		
		
	#Overrides
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return RadioSettings()

	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		#print( 'returning RadioState' )
		return RadioState()

	def _GetDeviceBehaviorOnActivate( self ):
		return DeviceBehaviorOnActivate( self, mute_on_deactivate = True, unmute_on_activate = True )
		#return DeviceBehaviorOnActivate( self, pause_on_deactivate = True, play_on_activate = True )

	#def Activate( self ):
		#if( not self.media_player.IsPlaying() ):
			#logging.debug( 'Radio.Activate: my media_player is not playing. Will start now.' )
			#self.media_player.Play( _PULSEAUDIO_SOURCENAME )
		#else:
			#logging.debug( 'Radio.Activate: my media_player is already playing.' )
		#MediaPlayerDevice.Activate( self )
		
	def Deactivate( self ):
		MediaDevice.Deactivate( self )
		
		if( self.scanTimer.IsRunning() ):
			#logging.debug( 'scanTimer stopped!' )
			self.scanTimer.Stop()
		self.scanUntilObserver.Stop()

	def _DevPlaylistFunctions( self ):
		'''
		Returns a dictionary. The keys are the playlist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'new': None, 'clear': None, 'save': None, 'add': self.AddStationDlg, 'edit': self.EditStationDlg,'delete': self.DelStationDlg, 'scan': None }
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'previous',
				'next',
				'step_back',
				'step_forward',
				'playlist_previous',
				'playlist_next'
			]
		else:
			return [
				'speeddial_previous',
				'speeddial_next',
			]

	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return {
			'zap':[ True, None ],
			'rewind':[ False, None ],
			'forward':[ False, None ],
			'previous':[ True, [ [wx.EVT_LEFT_DOWN, self.ScanManualBackStart], [wx.EVT_LEFT_UP, self.ScanManualBackStop], [wx.EVT_BUTTON, self.ScanManualBack] ] ],
			'next':[ True, [ [wx.EVT_LEFT_DOWN, self.ScanManualForwardStart], [wx.EVT_LEFT_UP, self.ScanManualForwardStop], [wx.EVT_BUTTON, self.ScanManualForward] ] ],
			'step_back':[ True, [ [wx.EVT_BUTTON, self.ScanBackward] ] ],
			'step_forward':[ True, [ [wx.EVT_BUTTON, self.ScanForward] ] ],
			'speeddial_previous':[ True, None ],
			'speeddial_next':[ True, None ],
			'playlist_previous':[ True, None ],
			'playlist_next':[ True, None ],
			'shuffle':[ False, None ],
			'repeat':[ False, None],
			'eject': [ False, None ] 
		}

	def TrackHashIsValid( self, track_hash ):
		#for fm_radio this is expected to be a station frequency in MHz
		frequency = float( track_hash )
		return ( frequency >= self.MinFrequency and frequency <= self.MaxFrequency )
	
	def DoPlay( self ):
		self.scanUntilObserver.Stop()
		self.Tune( self.frequency )
		
	def DoPlayTrack( self, track_hash ):
		self.scanUntilObserver.Stop()
		self.Tune( float( track_hash ) )
		MediaDevice.DoPlayTrack( self, track_hash )
		
	def GetCurrentTrackText( self ):
		text = ''
		if( self.frequency and self.stationList.StationAt( self.frequency ) ):
			text = self.stationList.StationAt( self.frequency )
		return text
	
	def GetFilelistItems( self ):
		raise Exception( 'A radio device does not support filelist functionality' )
	
	def GetPlaylistItems( self ):
		return self.stationList.ToMediaListItems()

	def SupportsStereoMono( self ):
		return True

	def SupportsSignalStrength( self ):
		return True
		
	def SignalStrengthIs( self ):
		return self.tuner.get_signal_strength()
	
	def InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		'''For the time being video_panel_click_callback is not used for radio'''
		MediaDevice.InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback )
		#sizer = self._video_panel_parent.GetSizer()
		self._video_panel = wx.Panel( video_panel_parent )
		video_panel_parent.GetSizer().Add( self._video_panel, 1, wx.EXPAND )
		
		video_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self._video_panel.SetSizer( video_sizer )
		
		video_sizer.Add( self._BuildFrequencyDisplay( self._video_panel ), 5, wx.EXPAND|wx.ALL, border=0 )
		
		self.signalStrengthControl = self._BuildSignalControl( self._video_panel )
		video_sizer.Add( self.signalStrengthControl, 2, wx.EXPAND|wx.ALL, border=0 )

		self.media_player = self._CreateMediaPlayer()

	def MainFrameInitUIFinished( self ):
		MediaPlayerDevice.MainFrameInitUIFinished( self )
		#self._behavior_on_activate.SetSystemMute( False )
		#self.media_player.SetMute( True )
		self._behavior_on_activate.SetUserPlay()
		#self.media_player.Play( '' )

	def HasVideoSettings( self ):
		return False

	#end of overrides

	#playlist functions
	def AddStationDlg( self, event ):
		button = event.GetEventObject()

		result = False
		ad = AddStationDialog( None, title='Add Station', defaultFrequency = self.frequency, 
			defaultStationName = 'Station' + str( len( self.stationList.stations ) ),
			MinFrequency = self.MinFrequency, MaxFrequency = self.MaxFrequency )
		if( ad.ShowModal() == wx.ID_OK ):
			print( 'Will add {}, {}'.format( ad.GetFrequency(), ad.GetStationName() ) )
			self.stationList.AddStation( ad.GetFrequency(), ad.GetStationName() )
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			result = True
		ad.Destroy()
		return result

	def EditStationDlg( self, event ):
		button = event.GetEventObject()
		station_hash = button.get_selected_item_hash_callback ()
		if( station_hash == '' or ( not self.stationList.stations.has_key( station_hash ) ) ):
			return False

		station = RadioStation( station_hash, self.stationList.stations[ station_hash ] )
		result = False
		ad = AddStationDialog( None, title='Edit Station', defaultFrequency = station.frequency, 
			defaultStationName = station.name,	MinFrequency = self.MinFrequency, MaxFrequency = self.MaxFrequency )
		if( ad.ShowModal() == wx.ID_OK ):
			print( 'Will edit {}, {}'.format( ad.GetFrequency(), ad.GetStationName() ) )
			self.stationList.EditStation( ad.GetFrequency(), ad.GetStationName() )
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			result = True
		ad.Destroy()
		return result
		
	def DelStationDlg( self, event ):
		button = event.GetEventObject()
		station_hash = button.get_selected_item_hash_callback ()
		if( station_hash == '' or ( not self.stationList.stations.has_key( station_hash ) ) ):
			return False
		
		station = RadioStation( station_hash, self.stationList.stations[ station_hash ] )	
		dial = wx.MessageDialog(None, 'Are you sure you want to delete ' +
			str( station.frequency ) +' Mhz' + ' - ' + station.name + 
			' ?', 'Delete station', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if( dial.ShowModal() == wx.ID_YES ):
			self.stationList.DeleteStation( station_hash )
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			return True
			
		return False
		
	#end of playlist functions
		
	def ScanBackward( self, event ):
		print( 'Scan backwards' )
		self.scanForward = False
		if( self._mmedia_gui ): 
			wx.CallAfter( self._mmedia_gui.ResetSpeedDials )
		self.ScanUntil()
		
	def ScanForward( self, event ):
		print( 'Scan forward' )
		self.scanForward = True
		if( self._mmedia_gui ): 
			wx.CallAfter( self._mmedia_gui.ResetSpeedDials )
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
		if( self._mmedia_gui ): 
			wx.CallAfter( self._mmedia_gui.ResetSpeedDials )
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
		if( self._mmedia_gui ): 
			wx.CallAfter( self._mmedia_gui.ResetSpeedDials )
		self.scanTimer.Start(500)
		event.Skip()
		
	def ScanManualForwardStop( self, event ):
		print( 'Scan manual forward Stop' )
		self.scanTimer.Stop()
		event.Skip()		
	
	def Scan( self, event = None ):		
		if( self.scanForward ):
			print( 'scanning forward...' )
			self.IncreaseFrequency( self.settings.ScanStepKHz )
		else:
			print( 'scanning backward...' )
			self.DecreaseFrequency( self.settings.ScanStepKHz )
		if( self._mmedia_gui ): 
			wx.CallAfter( self._mmedia_gui.ResetSpeedDials )
			
	def _BuildFrequencyDisplay( self, panel ):
		controlPanel = wx.Panel( panel )
		controlPanel.SetBackgroundColour( '#000000' )
		freqSizer = wx.BoxSizer( wx.VERTICAL )
		controlPanel.SetSizer( freqSizer )
		self.stationNameText = wx.StaticText( controlPanel )		
		self.freqText = wx.StaticText( controlPanel )
		freqStationTextFont = self.settings.StationFreqFont.GetFont()
		nameStationTextFont = self.settings.StationNameFont.GetFont()
		self.stationNameText.SetFont( nameStationTextFont )
		self.freqText.SetFont( freqStationTextFont )
		self.stationNameText.SetForegroundColour(self.settings.StationNameFont.Color )
		self.freqText.SetForegroundColour(self.settings.StationFreqFont.Color )
		
		freqSizer.Add( self.freqText, 0, wx.ALIGN_LEFT, border=0 )
		freqSizer.Add( self.stationNameText, 0, wx.ALIGN_LEFT, border=0 )
		
		return controlPanel
		
	def _BuildSignalControl( self, panel ):
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
			color = self.settings.SignalBarBrightColor if ( (i+1)*10 ) <= signalStrength else self.settings.SignalBarDimColor
			self.signalBar[ self.signalBarCount - i - 1 ].SetBackgroundColour( color )
			self.signalBar[ self.signalBarCount - i - 1 ].Refresh()
			
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
		
class ScanUntilObserver:	
	FALLING = 0
	RISING = 1 
	MIN_FREQUENCY_SEPARATION = 0.25
	a = 0
	b = 0
	last = 0.0	
	
	def __init__( self, frame, radio ):
		self.frame = frame
		self.radio = radio
		self.running = False
		self.previousSignalStrength = 0
		self.previousFrequency = 0.0
		
	def Start( self ):
		# print( 'Started :)' )
		self.running = True
		self.previousSignalStrength = self.radio.signalStrength
		self.previousFrequency = self.radio.frequency
		self.mode = ScanUntilObserver.FALLING
		#print( 'ScanUntilObserver will system mute' )
		wx.CallAfter( self.frame.SystemMute )
		ScanUntilObserver.last = self.radio.frequency
		self.radio.Scan()
		
	def Stop( self ):
		# print( 'Stopped :(' )
		self.running = False
		#print( 'ScanUntilObserver will system unmute' )
		wx.CallAfter( self.frame.SystemUnmute )
			
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
			#self.radio.frequency, 
			#self.radio.signalStrength ) )
		
		strength = self.radio.signalStrength			
			
		#print( 'a:{} + b:{} + s:{} = {} ~ max:{}, f:{} - last:{} = {} ~ MIN_FREQUENCY_SEPARATION:{}'.format( ScanUntilObserver.a, ScanUntilObserver.b, strength, ScanUntilObserver.a + ScanUntilObserver.b + strength,
			#self.radio.GetMaxSignalStrength(),
			#self.radio.frequency, ScanUntilObserver.last,			
			#math.fabs( self.radio.frequency - ScanUntilObserver.last ),
			#self.frame.Settings.ScanFrequencySeparationThresholdMHz ) )
		last3Strengths = ScanUntilObserver.a + ScanUntilObserver.b + strength
		if( ( last3Strengths > self.radio.GetMaxSignalStrength() ) and
			last3Strengths > 0.8*self.radio.settings.MinAcceptableStationSignalStrength and
			( math.fabs( self.radio.frequency - ScanUntilObserver.last ) > 
			self.radio.settings.ScanFrequencySeparationThresholdMHz ) 
			):
			#print( 'previous strength:{}%, current strength:{}%'.format( 
			#self.previousSignalStrength, strength ) )
			if( self.previousSignalStrength > strength ):			
				if( self.mode == ScanUntilObserver.RISING ):
					#print( 'found peak' )
					if( self.previousSignalStrength > self.radio.settings.MinAcceptableStationSignalStrength ):
						self.Stop()					
						ScanUntilObserver.a = 0
						ScanUntilObserver.b = 0
						ScanUntilObserver.last = self.radio.frequency
						self.radio.Tune( self.previousFrequency )
						wx.CallAfter( self.frame.ZappStart, self.Start )
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
		self.previousFrequency = self.radio.frequency
		self.radio.scanTimer.Start( self.radio.settings.ScanWaitTimeMSecs, True )
		return	

class FrequencyPanelObserver:
	'''A class that will be notified when the states frequency changes'''
	
	def __init__( self, radio ):
		self.radio = radio
		
	def FrequencyIs( self, frequency ):
		#~ print( 'will update to freq {}'.format( frequency ) )
		self.radio.SetFrequencyText( frequency )
		self.radio.title = frequency
		station = self.radio.stationList.StationAt( frequency )
		if( station is not None ):
			self.radio.SetStationNameText( station )			
		else:
			self.radio.ClearStationNameText()	
		self.radio.GetVideoPanel().Refresh()
		
class SignalStrengthPanelObserver:
	def __init__( self, frame ):
		self.frame = frame
		
	def SignalStrengthIs( self, signalStrength ):
		self.frame.SetSignalStrength( signalStrength )
	
class RandomRadio( Radio ):
	def __init__( self, frequency = 87.5 ):
		Radio.__init__( self, frequency )
		#super( RandomRadio, self ).__init__()
		
	def Tune( self, frequency ):
		self.signalStrength = random.randrange( 0, 100 )
		time.sleep( random.randrange( 5, 10 )/10.0 )
		Radio.Tune( self, frequency )
	
class DemoRadio( Radio ):	
		
	def __init__( self, frequency = 87.5, minAcceptableStationSignalStrength = 30 ):
		#Radio.__init__( self, None, frequency )
		self.MinAcceptableStationSignalStrength = minAcceptableStationSignalStrength
		self.stationList = DemoStationList()	
		
	def Tune( self, frequency ):	
		time.sleep( 0.1 )
		self.TuneStop( frequency )
		#Timer( random.randrange( 5, 10 )/10.0, self.TuneStop, [frequency] ).start()
		#d = DemoTimer( lambda: self.TuneStop( frequency ) )
		#d.Start( 1 ) 
	
	def TuneStop( self, frequency ):
		print( 'Testing {0}Mhz'.format( frequency ) )
		station = self.stationList.StationAt( frequency )
		if( station is not None ):
			# print( '{} at {}Mhz'.format( station, frequency ) )
			self.signalStrength = random.randrange( self.MinAcceptableStationSignalStrength, 100 )
			self.isStereo = ( random.randrange( 0.0, 10.0 ) > 0.1 )
		else:
			# print( 'No station at {}MHz'.format( frequency ) )
			self.signalStrength = random.randrange( 0, self.MinAcceptableStationSignalStrength - 1 )
			self.isStereo = False
		#Radio.Tune( self, frequency )

class DemoTimer( wx.Timer ):
	def __init__( self, notifyMethod ):
		wx.Timer.__init__( self )
		self.notifyMethod = notifyMethod
		
	def Notify( self ):
		print( 'Calling notify' )
		self.notifyMethod()

_DEFAULT_FREQUENCY = 102.5
def main():
    
	try:
		tuner = FMRadio(enable_rds=False)
		#pass
	except FMRadioUnavailableError:
		print "FM radio device is unavailable"
		sys.exit(1)

	# register signal handler for exiting
	def handler(signum, frame):
		tuner.close()
		sys.exit(0)

	signal.signal(signal.SIGINT, handler)

	# tune to a radio service
	frequency = float(sys.argv[1]) if len(sys.argv) is 2 else _DEFAULT_FREQUENCY
	print "Tuning to %0.2f Mhz" % frequency

	tuner.set_frequency(frequency*1000 )
	print( 'Actually tuned to {}'.format( tuner.get_frequency() ) )
	print( 'Signal strength:{}'.format( tuner.get_signal_strength() ) )
	#tuner.rds.add_listener( CarPC_RDSDecoderListener() )

	# keep the app running
	keep_running = True
	while keep_running:
		newFreq = input( 'Enter new frequency to tune at (e.g. 102.5):' )
		if( newFreq == 0 ):
			keep_running = False
			break
		else:
			tuner.set_frequency(newFreq*1000 )
			#print( 'Will check actual frequency' )
			#print( 'Actually tuned to {}'.format( tuner.get_frequency() ) )
			#print( 'Signal strength:{}'.format( tuner.get_signal_strength() ) )
		#time.sleep(1000)

	
if __name__ == "__main__":
	main()
