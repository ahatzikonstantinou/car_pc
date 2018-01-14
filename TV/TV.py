#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from WScanner import *
from Channel import *

#from mixer_pulseaudio import *
#from dummyMixer import * #remove for release

from VLCControl import *

#_PULSEAUDIO_SOURCENAME = 'alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo'

class TV:
	'''
	This is the tv program. It uses WScanner which is a wrrapper of the w_scan utility.
	It uses vlc to display the tv picture
	'''
	
	ChannelsFile = 'channelList.tv'
	#'vlc -vvv dvb:// --dvb-frequency={} --dvb-adapter=0 --dvb-bandwidth=8 --program={}'
	VLCTuneCmd = 'dvb-t:// :frequency={0} :adapter=0 :bandwidth=8'
	
	def __init__( self ):
		self.tunedChannel = None
		self.tuneObservers = []
		self.volumeObservers = []
		self.channels = {}
		self.digitalScanner = WScanner()
		#self.mixer = DummyMixer() #used for debugging in windows. For linux use self.mixer = PulseaudioMixer( _PULSEAUDIO_SOURCENAME )
		self.videopanel = None
		self.controlspanel = None
		self.onlyVideoIsDisplayed = False
		
	def InitUI( self, videoParentPanel, controlsParentPanel, state, stateSaveCallback, videoPanelClickCallback, hideDevice = True ):
		self.vlccontrol = VLCControl( videoParentPanel, controlsParentPanel, state, stateSaveCallback, videoPanelClickCallback )
		self.videopanel = self.vlccontrol.videopanel
		self.controlspanel = self.vlccontrol.ctrlpanel
		
	def Start( self ):
		'''Must be called only after the main frame of the parent application has been displayed
		   with Frame.Show()
		'''
		self.vlccontrol.Start()
		
	def GetVolume( self ):
		#return self.mixer.GetVolume()
		#vlc volume range is in [0, 200]
		return self.vlccontrol.player.audio_get_volume() / 2
		
	def SetVolume( self, volume ):
		#self.mixer.SetVolume( volume )
		#vlc volume range is in [0, 200]
		self.vlccontrol.player.audio_set_volume(volume*2)
		self.UpdateVolumeObservers( volume )
				
	def GetMute( self ):
		#return self.mixer.GetMute()
		self.vlccontrol.player.audio_get_mute()

	def SetMute( self, on ):
		#self.mixer.SetMute( on )
		self.vlccontrol.player.audio_set_mute( on )
		
	def Tune( self, channel ):
		print( 'TV is tuning to channel {0}'.format( channel.name ) )
		self.tunedChannel = channel
		
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
		#we need to explicitly set the brightness and contrast every time we tune to a channel
		#self.vlccontrol.OnSetBrightness()
		#self.vlccontrol.OnSetContrast()
		
	def DisplayOnlyVideo( self, onlyVideoIsDisplayed ):
		self.onlyVideoIsDisplayed = onlyVideoIsDisplayed
		if( self.onlyVideoIsDisplayed ):
			self.vlccontrol.ShowMarquee( False ) #hide marquee			
		else:
			self.vlccontrol.ShowMarquee( True, self.tunedChannel.name ) #show marquee
		
	def GetTunedChannelHash( self ):
		hash = ''
		if( self.tunedChannel is not None ):
			hash = self.tunedChannel.GetHash()
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
			
	def Callback( progressPercent, status, message ):
		pass
		
	def LoadChannels( self ):
		for c in Channel.LoadList( TV.ChannelsFile ):
			self.channels[c.GetHash()] = c
	
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
