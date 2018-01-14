#!/usr/bin/python
# -*- coding: utf-8 -*-

from filesystem_device import *
from upnp_provider import *
from upnp_media_item import *
from upnp_media_player import *
from upnp_mediarenderer_player import *

class UPnPMediaRendererDevice( Filesystem ):
	def __init__( self, abstract_device  ):
		Filesystem.__init__( self, 
			abstract_device, 
			root_dir = '0'
		)
		
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
				'step_forward'
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
			'step_forward':[ True, [ [wx.EVT_BUTTON, self.OnStepForward] ] ]
		}
		
	def GetCurrentTrackText( self ):
		if( self.current_media_item ):
			return self.current_media_item.Text()
			
		return ''
		
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions
				
	def GetMediaStringForPlayer( self, item_str ):
		'''
		For almost any filesystem derived device this is just the item_str
		But for the UPnP MediaServer device this is the mediaservers hostname concat with the object's id
		There is a bug here. Some object id's come prefixed with '/'. If this is concatenated to
		http://hostname/ there will be two '/' after the hostname and this is a "not exists" error
		'''
		media_string = item_str
		item = self.GetMediaItem( item_str )
		if( item ):
			media_string = item.ResGetUrl()
		return media_string
		
	def _CreateMediaPlayer( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		return UPnPMediaRendererPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
	
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
