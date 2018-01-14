#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from WScanner import *
from Channel import *
from tv_settings import TVSettings
from tv_state import TVState
from edit_station_dialog import EditStationDialog
from ScanStationsDialog import *

#from mixer_pulseaudio import *
#from dummyMixer import * #remove for release

from VLCControl import *
from media_device import MediaDevice


class TV( MediaDevice ):
	'''
	This is the tv program. It uses WScanner which is a wrrapper of the w_scan utility.
	It uses vlc to display the tv picture
	'''
	
	ChannelsFile = 'channelList.tv'
	#'vlc -vvv dvb:// --dvb-frequency={} --dvb-adapter=0 --dvb-bandwidth=8 --program={}'
	VLCTuneCmd = 'dvb-t:// :frequency={0} :adapter=0 :bandwidth=8'
	
	def __init__( self, abstract_device ):
		MediaDevice.__init__( self, abstract_device.name, abstract_device.dev_path, abstract_device.dev_type, abstract_device._mmedia_gui, abstract_device._gui_media_functions, abstract_device._playerLock, abstract_device._error_reporter, abstract_device._message_reporter )
		self.tunedChannel = None
		self.tuneObservers = []
		self.volumeObservers = []
		self.channels = {}
		self.digitalScanner = WScanner()
		#self.mixer = DummyMixer() #used for debugging in windows. For linux use self.mixer = PulseaudioMixer( _PULSEAUDIO_SOURCENAME )
		self.onlyVideoIsDisplayed = False
		
		self.LoadChannels()
				
	def Tune( self, channel ):
		print( 'TV is tuning to channel {0}'.format( channel.name ) )
		self.tunedChannel = channel
		self.state.TunedChannelIs( self.tunedChannel )
		
		#execute a command that will make the vlc plugin used for displaying tv image to tune the tv tuner device
		#to the required station
		media = TV.VLCTuneCmd.format( channel.frequency )
		options = 'program={0}'.format( channel.service_id )
		#media = 'v4l2:///dev/video0'
		#media = 'dvb:// :dvb-frequency=682000000 :dvb-adapter=0 :dvb-bandwidth=8 :program=500'
		#media = 'dvb-t://:frequency=682000000:bandwidth=8:adapter=0'
		self.vlccontrol.PlayMedia( media, options )
		self.UpdateTuneObservers()
		self.DisplayOnlyVideo( self.onlyVideoIsDisplayed )
		self._mmedia_gui.SetTextDisplayMessage( self.tunedChannel.name )
		
	def DisplayOnlyVideo( self, onlyVideoIsDisplayed ):
		self.onlyVideoIsDisplayed = onlyVideoIsDisplayed
		if( self.onlyVideoIsDisplayed ):
			self.vlccontrol.ShowMarquee( False ) #hide marquee			
		else:
			self.vlccontrol.ShowMarquee( True, self.tunedChannel.name ) #show marquee
		
	def GetTunedChannelHash( self ):
		hash = ''
		if( self.tunedChannel is not None ):
			hash = self.tunedChannel.Hash()
		return hash
				
	def AddTuneObserver( self, observer ):
		self.tuneObservers.append( observer )
		
	def UpdateTuneObservers( self ):
		if( self.tunedChannel is None ):
			return
		for i in self.tuneObservers:
			i.TunedChannelIs( self.tunedChannel )
								
	def AddVolumeObserver( self, observer ):
		self.volumeObservers.append( observer )
		
	def UpdateVolumeObservers( self, volume ):
		for i in self.volumeObservers:
			i.VolumeIs( volume )
			
	def TrackHashIsValid( self, track_hash ):
		'''overriden to check if a hash i.e. frequency is valid
		'''
		is_valid = self.channels.has_key( track_hash )
		return is_valid
		
	#All concrete devices should override the following functions
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return TVSettings()

	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return TVState()
		
	def Activate( self ):
		MediaDevice.Activate( self )
		if( not self.vlccontrol.IsPlaying() ):
			if( self.state.channelHash is not None and 
				len( self.state.channelHash ) > 0 and
				self.channels.has_key( self.state.channelHash )
			):
				self.tunedChannel = self.channels[ self.state.channelHash ]
				self.Play()
		self.SetMute( False )
			
	def Deactivate( self ):
		MediaDevice.Deactivate( self )
		self.SetMute( True )
		#self.vlccontrol.Stop()
				
	def _DevPlaylistFunctions( self ):
		'''
		Returns a dictionary. The keys are the playlist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'new': None, 'clear': None, 'save': None, 'add': None, 'edit': self.EditListStation,'delete': self.DelListStation, 'scan': self.ScanListStation }
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'speeddial_previous',
				'speeddial_next',
				'playlist_previous',
				'playlist_next',
			]
		else:
			return [
			]
				
	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return {
			'zap':[ True, None ],
			'play':[ False, None ],
			'rewind':[ False, None ],
			'forward':[ False, None ],
			'previous':[ False, None ],
			'next':[ False, None ],
			'step_back':[ False, None ],
			'step_forward':[ False, None ],
			'speeddial_previous':[ True, None ],
			'speeddial_next':[ True, None ],
			'playlist_previous':[ True, None ],
			'playlist_next':[ True, None ],
			'shuffle':[ False, None ],
			'repeat':[ False, None],
			'eject': [ False, None ] 
		}
												
	def Play( self ):
		self.Tune( self.tunedChannel )
		
	def PlayTrack( self, track_hash ):
		if( track_hash ):
			channel = self.channels[ track_hash ]
			self.Tune( channel )
			MediaDevice.PlayTrack( self, track_hash )
		else:
			raise Exception( 'TV was asked to play unknown track with hash: {}'.format( track_hash ) )				
		
	def GetFilelistItems( self ):
		raise Exception( 'A tv device does not support filelist functionality' )
	
	def GetPlaylistItems( self ):
		return Channel.ToMediaListItems( self.channels )
							
	def GetMute( self ):
		#return self.mixer.GetMute()
		self.vlccontrol.player.audio_get_mute()

	def SetMute( self, on ):
		#self.mixer.SetMute( on )
		self.vlccontrol.player.audio_set_mute( on )

	def SetVolume( self, volume ):
		#self.mixer.SetVolume( volume )
		#vlc volume range is in [0, 200]
		self.vlccontrol.player.audio_set_volume(volume*20)
		self.UpdateVolumeObservers( volume )

	def GetVolume( self ):
		#return self.mixer.GetVolume()
		#vlc volume range is in [0, 200]
		return self.vlccontrol.player.audio_get_volume() / 20

	#end of functions to be overriden by concrete devices
	
	#functions that may be overriden
	
	def InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		MediaDevice.InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback )
		print( 'passing video_panel_click_callback:{} to VLCControl'.format( video_panel_click_callback ) )
		self.vlccontrol = VLCControl( video_panel_parent, control_panel_parent, self.state, playerLock = self._playerLock, videoPanelClickCallback = video_panel_click_callback )
		self._video_panel = self.vlccontrol.videopanel
		self._controls_panel = self.vlccontrol.ctrlpanel
		self._video_panel_parent.GetSizer().Add( self._video_panel, 1, wx.EXPAND )

		return
		
	#def InitUI( self, videoParentPanel, controlsParentPanel, state, stateSaveCallback, videoPanelClickCallback, hideDevice = True ):
		#self.vlccontrol = VLCControl( videoParentPanel, controlsParentPanel, state, stateSaveCallback, videoPanelClickCallback )
		#self._video_panel = self.vlccontrol.videopanel
		#self.controlspanel = self.vlccontrol.ctrlpanel

	def MainFrameInitUIFinished( self ):
		'''
		vlccontrol.Start must be called only after the main frame of the parent 
		application has been displayed with Frame.Show()
		'''
		self.vlccontrol.Start()
		
	#end of functions that may be overriden
			
	#playlist functions
	
	def EditListStation( self, event ):
		button = event.GetEventObject()
		station_hash = button.get_selected_item_hash_callback ()
		if( station_hash == '' or ( not self.channels.has_key( station_hash ) ) ):
			return False

		station = self.channels[ station_hash ]
		result = False
		ad = EditStationDialog( None, title='Edit Station', station=station )
		if( ad.ShowModal() == wx.ID_OK ):
			station.name = ad.GetStationName()
			self.SaveChannels()
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			result = True
		ad.Destroy()
		return result
		
	def DelListStation( self, event ):
		button = event.GetEventObject()
		station_hash = button.get_selected_item_hash_callback ()
		if( station_hash == '' or ( not self.channels.has_key( station_hash ) ) ):
			return False

		station = self.channels[ station_hash ]
		result = False
		dial = wx.MessageDialog(None, 'Are you sure you want to delete ' +
			str( station.name ) +
			#' - ' + self.stationList[ str( selectedListStationButton.frequency ) ]+ 
			' ?', 'Delete station', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if( dial.ShowModal() == wx.ID_YES ):
			del self.tv.channels[ station.GetHash() ]
			self.SaveChannels()
			self.stationList.stations = self.tv.channels
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			result = True
	
	def ScanListStation( self, event ):
		dlg = ScanStationsDialog( None, 'Scan Stations Test', self.channels )
		if( dlg.ShowModal() == wx.ID_OK ):
			self.stationList.stations = dlg.stations
			self.channels = dlg.stations
			self.SaveChannels()
			#button.refresh_list_items_callback( self.GetPlaylistItems() )
			self.UpdatePlaylistObservers()
			result = True
	
	#end of playlist functions
		
	def Callback( progressPercent, status, message ):
		pass
		
	def LoadChannels( self ):
		for c in Channel.LoadList( TV.ChannelsFile ):
			self.channels[c.Hash()] = c
	
	def SaveChannels(self):
		Channel.SaveList( self.channels, TV.ChannelsFile )
		
	def DumpChannels( self ):
		for key, value in self.channels.iteritems():
			value.Dump()
		

if __name__ == '__main__':
	tv = TV()
	tv.channels = tv.digitalScanner.ReadConf( 'channels.conf' )
	tv.SaveChannels()
	tv.LoadChannels()
	#tv.DumpChannels()
