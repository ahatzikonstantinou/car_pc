#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse

from filesystem_device import *
from upnp_provider import *
from upnp_media_item import *
from upnp_mediaserver_device import *
from upnp_mediarenderer_proxy_player import *

from coherence.base import Coherence
from coherence.upnp.devices.media_renderer import MediaRenderer

from gstreamer_renderer import *

'''
TODO: 
	-upnp_hostInfo will change/be updated at every call on SetCurrentTrack, so maybe I will not be able to extend UPnPMediaServerDevice and should extend Filesystem instead
	-Ensure that the metadata passed to SetCurrentTrack are appropriate for UPnPMediaItem constructor
	-The UPnPMediaRendererDevice must be added to the devices of MMedia gui and exists always like TV and Radio
	-Implement a mechanism to show the device in the gui when "Play", and hide it from the gui when "Stop"
	-Look at MediaRendererProxyPlayer.update method and how it is used in gstreamer_player.py in class Player to update the position and duration of current track
	-Maybe I should implement "next" and "previous" buttons, see MediaRendererProxyPlayer.load and in particular the lines about transport_actions
'''
	
import logging
logging.basicConfig( level = logging.DEBUG )

class UPnPMediaRendererDevice( UPnPMediaServerDevice ):
	def __init__( self, abstract_device ):
		#Filesystem.__init__( self, abstract_device, root_dir = '0' )
		UPnPMediaServerDevice.__init__( self, None, None, None, abstract_device )
		self.coherence_thread = None
		
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return UPnPMediaRendererState()
		
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return UPnPMediaRendererSettings()
				
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path )
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'play',
				'rewind',
				'forward',
				'step_back',
				'step_forward',
				'subtitles'
			]
			
		return []

	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return {
			'play': [ True, [ [wx.EVT_BUTTON, self.OnPlay] ] ],
			'rewind':[ True, [ [wx.EVT_BUTTON, self.OnRewind] ] ], 
			'forward':[ True, [ [wx.EVT_BUTTON, self.OnForward] ] ], 
			'step_back':[ True, [ [wx.EVT_BUTTON, self.OnStepBack] ] ],
			'step_forward':[ True, [ [wx.EVT_BUTTON, self.OnStepForward] ] ],
			'subtitles':[ True, None ]
		}

	def SetMute( self, on ):
		Filesystem.SetMute( self, on )
		if( on ):
			rcs_value = 'True'
		else:
			rcs_value = 'False'
		if( self.coherence_thread is not None ):
			self.coherence_thread.SetRCSVariable( 'Mute', rcs_value )
		
	def Mute( self ):
		self.SetMute( True )
		
	def Unmute( self ):
		self.SetMute( False )
		
	def SetVolume( self, volume ):
		Filesystem.SetVolume( self, volume )
		if( self.coherence_thread is not None ):
			self.coherence_thread.SetRCSVariable( 'Volume', volume )
		
	def Pause( self ):
		Filesystem.Pause( self )
		if( self.coherence_thread is not None ):
			logging.debug( 'UPnPMediaRendererDevice sending PAUSED_PLAYBACK to transport server' )
			self.coherence_thread.SetAVTVariable( 'TransportState', 'PAUSED_PLAYBACK' )
		
	def DoPlay( self ):
		if( self.coherence_thread is not None ):
			logging.debug( 'UPnPMediaRendererDevice sending PLAYING to transport server' )
			self.coherence_thread.SetAVTVariable( 'TransportState', 'PLAYING' )
		dev_hash = self.Hash()
		wx.CallAfter( self._mmedia_gui.GU_DeviceShowMe, dev_hash )
		self.media_player.Play( self._current_track_hash )
		wx.CallAfter( MediaDevice.Play, self )
		#return MediaDevice.Play( self ) #will call the UPnPMediaServerDevice.GetCurrentTrackText which calls self.current_media_item.Text()
		return True
			
	def Stop( self, silent = False ):
		Filesystem.Stop( self )
		dev_hash = self.Hash()
		wx.CallAfter( self._mmedia_gui.GU_DeviceHideMe, dev_hash )
		if( silent is True and self.coherence_thread is not None ):
			self.coherence_thread.SetAVTVariable( 'TransportState', 'STOPPED' )
		self.is_active = False

	def SetCurrentTrack( self, uri, metadata ):
		logging.debug( 'UPnPMediaRendererDevice.SetCurrentTrack called with:\n\turi: {}\n\tmetadata: {}'.format( uri, metadata ) )
		self._current_track_hash = uri
		o = urlparse( uri )
		hostname = o.netloc
		logging.debug( 'UPnPMediaRendererDevice.SetCurrentTrack will try to create a UPnPMediaItem with hostname: {}, metadata: {}'.format( hostname, metadata ) )
		self.current_media_item = UPnPMediaItem( hostname, metadata )
		
	def OnEndOfTrack( self ):
		#TODO: hide from the gui
		print( 'TODO: hide from the gui' )
		
	def Seek( self, location ):
		''' 
		location is a positive or negative string representing an integer. It is the time in secs where to set the track time
		'''
		if( self.media_player.IsPlaying() ):
			try:
				self.media_player.SetTime( int( location )*1000 )
			except ValueError:
				print( 'Could not seek to time {}. Maybe this is not a valid string representation of secs.'.format( location ) )

	def RefreshMediaActions( self, actions ):
		''' 
		actions is a set that may contain the following string values: 'PLAY,STOP,PAUSE,SEEK,NEXT,PREVIOUS'
		'''
		if( 'NEXT' in actions ):
			#TODO: enable the next button
			pass
		else:
			#TODO: disable the next button
			pass

		if( 'PREVIOUS' in actions ):
			#TODO: enable the next button
			pass
		else:
			#TODO: disable the next button
			pass
			
	def GetPlayerState( self ):
		state = PlayerState.OTHER
		player_state = self.media_player.GetState()
		if( player_state == vlc.State.Playing ):
			state = PlayerState.PLAYING
		elif( player_state == vlc.State.Paused ):
			state = PlayerState.PAUSED
		return state

	def _ReadDir( self, directory ):
		'''
		This is a hack. The Filesystem device calls _ReadDir at InitUI. There is no dir to read for a media renderer
		so do nothing
		'''
		return
		
	def MainFrameInitUIFinished( self ):
		logging.debug( 'UPnPMediaRendererDevice.MainFrameInitUIFinished hiding...' )
		dev_hash = self.Hash()
		wx.CallAfter( self._mmedia_gui.GU_DeviceHideMe, dev_hash )
		logging.debug( 'UPnPMediaRendererDevice.MainFrameInitUIFinished hid.' )
		self.coherence_thread = CoherenceThread( self )
		logging.debug( 'UPnPMediaRendererDevice.MainFrameInitUIFinished and created CoherenceThread' )
		
	def Shutdown( self ):
		logging.debug( 'UPnPMediaRendererDevice: Shutdown was just called...' )
		if( self.coherence_thread is not None ):
			self.coherence_thread.stop()
		logging.debug( 'UPnPMediaRendererDevice: Shutdown has finished.' )
		
class UPnPMediaRendererSettings( MediaDeviceSettings ):
	def __init__( self ):
		MediaDeviceSettings.__init__( self )
		self._speeddial_rows = 0
		self._speeddial_buttons_per_row = 0
			
class UPnPMediaRendererState( FilesystemState ):
	def __init__( self, current_dir = '0' ):
		FilesystemState.__init__( self, current_dir )
		
	def SetSpeedDial( self, index, track_hash ):
		pass
	
	def DelSpeedDial( self, index ):
		pass
		
	def Load( self ):
		pass
	
	def Save(self):
		pass

class CoherenceThread( Thread ):
	def __init__( self, mmedia_mediarendererdevice ):
		self.mmedia_mediarendererdevice = mmedia_mediarendererdevice
		kwargs = {}
		kwargs['controller'] = self.mmedia_mediarendererdevice
		self.server = MediaRenderer(coherence = Coherence({'unittest':'no','logmode':'error','use_dbus':'yes','controlpoint':'yes'}), backend = MediaRendererProxyPlayer, **kwargs )
		logging.debug( 'UPnPMediaRendererDevice: Finished initialization, just created my MediaRenderer' )

		Thread.__init__( self )
		self.setDaemon( True )
		self.start()
		
	def stop( self ):
		logging.debug( 'Will unregister the coherence media renderer...' )
		self.server.unregister()
		logging.debug( 'Unregistered the coherence media renderer.' )
		#reactor.stop()
		
	def run( self ):
		reactor.run()
		
	def SetAVTVariable( self, variable_name, variable_value ):
		if( self.server is not None and self.server.backend is not None ):
			self.server.backend.SetAVTVariable( variable_name, variable_value )

	def SetRCSVariable( self, variable_name, variable_value ):
		if( self.server is not None and self.server.backend is not None ):
			self.server.backend.SetRCSVariable( variable_name, variable_value )
