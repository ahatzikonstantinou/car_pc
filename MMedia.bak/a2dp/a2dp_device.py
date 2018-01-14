#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import logging
import os

from filesystem_device import *
from a2dp_media_player import *

__all__ = [ 'A2DPDevice' ]

class A2DPDevice( Filesystem ):
	DEBUG = True
	def __init__( self, a2dp_source, abstract_device, GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectePlaylistItemsCallback = None ):
		self.a2dp_source = a2dp_source
		Filesystem.__init__( self, abstract_device, root_dir = '000' )
		if( A2DPDevice.DEBUG ):
			logging.debug( 'I am an a2dp device, name: {}'.format( self.name ) )
				
	def Activate( self ):
		Filesystem.Activate( self )
		self.media_player.Play( self.GetMediaStringForPlayer( '' ) )
		MediaDevice.Play( self )
		
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return A2DPDeviceState()
		
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return A2DPSettings()
		
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path.replace( '/ ', '_' ) )
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [ 'eject' ]
			
		return []

	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return { 'eject': [ True, [ [ wx.EVT_BUTTON, self.OnEject ] ] ] }
		
	def OnEject( self, event ):
		if( A2DPDevice.DEBUG ):
			logging.debug( 'Will try to disconnect a2dp device "{}"'.format( self.a2dp_source.address ) )
		dial = wx.MessageDialog(
			None, 
			'Are you sure you want to disconnect ' + self.name + ' ?', 
			'Disconnect', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
			)
		if( dial.ShowModal() == wx.ID_YES ):
			print( '{}: {}'.format( self.a2dp_source.address, type( self.a2dp_source.address[:-1] ) ) )
			try:
				#cmd = 'bluez-test-device disconnect {}'.format( self.a2dp_source.address[:-1] )
				#import shlex
				#args = shlex.split( cmd )
				#cmd = "echo '{}'".format( self.a2dp_source.address[:-1] )
				subprocess.call( ['bluez-test-device',  'disconnect', self.a2dp_source.address[:-1] ] )
				#os.system( cmd )
			except:
				import traceback; traceback.print_exc()
				self._ReportError( 'An error occured. Failed to disconnect {} ({})'.format( self.name, self.a2dp_source.address ) )
				
	def _CreateMediaPlayer( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		return A2DPMediaPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
		
	def GetMediaStringForPlayer( self, item_str ):
		return 'pulse://{}'.format( self.a2dp_source.pulseaudio_name )
			
class A2DPSettings( MediaDeviceSettings ):
	def __init__( self ):
		MediaDeviceSettings.__init__( self )
		self._speeddial_rows = 0
		self._speeddial_buttons_per_row = 0
		
class A2DPDeviceState( FilesystemState ):
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
		
		
