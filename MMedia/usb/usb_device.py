#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import logging

from filesystem_device import *

__all__ = [ 'USBDevice' ]
class USBDevice( Filesystem ):
	DEBUG = True
	def __init__( self, gio_mount, uuid, root_dir, abstract_device, GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectedPlaylistItemsCallback = None ):
		self.gio_mount = gio_mount
		self.uuid = uuid	#needs to be here before Filesystem.__init__
		self.root_dir = root_dir	#needs to be here because Filesystem.__init__ first calls MediaDevice.__init__ and then sets self.root_dir
		Filesystem.__init__( self, abstract_device, self.root_dir, GetSelectedListFilesCallback, SetPlaylistLabelTextCallback, GetSelectedPlaylistItemsCallback )
				
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return UsbDeviceState( self.uuid, self.name, self.root_dir )
		
	def Hash( self ):
		return '{0}_{1}_{2}_{3}'.format( self.dev_type, self.name, self.dev_path, self.uuid )
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'play',
				'previous',
				'next',
				'speeddial_previous',
				'speeddial_next',
				'eject'
			]
		else:
			return [
				'rewind',
				'forward',
				'step_back'
				'step_forward',
				'playlist_previous',
				'playlist_next',
				'subtitles',
				'shuffle',
				'repeat',
				'refresh'
			]

	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return {
			'zap':[ True, None ],
			'play': [ True, [ [wx.EVT_BUTTON, self.OnPlay] ] ],
			'rewind':[ True, [ [wx.EVT_BUTTON, self.OnRewind] ] ], 
			'forward':[ True, [ [wx.EVT_BUTTON, self.OnForward] ] ], 
			'previous':[ True, None ],
			'next':[ True, None ],
			'step_back':[ True, [ [wx.EVT_BUTTON, self.OnStepBack] ] ],
			'step_forward':[ True, [ [wx.EVT_BUTTON, self.OnStepForward] ] ],
			'speeddial_previous':[ True, None ],
			'speeddial_next':[ True, None ],
			'playlist_previous':[ True, None ],
			'playlist_next':[ True, None ],
			'subtitles':[ True, None ],
			'shuffle':[ True, [ [wx.EVT_BUTTON, self.OnShuffle] ] ],
			'repeat':[ True, [ [wx.EVT_BUTTON, self.OnRepeat] ] ],
			'eject': [ True, [ [wx.EVT_BUTTON, self.OnEject ] ] ],
			'refresh': [ True, [ [wx.EVT_BUTTON, self.OnRefresh] ] ]
		}
		
	def OnEject( self, event ):
		if( USBDevice.DEBUG ):
			logging.debug( 'Will try to unmount {}'.format( self.dev_path ) )
		dial = wx.MessageDialog(
			None, 
			'Are you sure you want to unmount ' + self.name + ' ?', 
			'Unmount Disk', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
			)
		if( dial.ShowModal() == wx.ID_YES ):
			self.gio_mount.unmount( self._UnmountCallback )
			subprocess.call( ['sudo', 'gvfs-mount', '-u', '"{}"'.format( self.dev_path ) ] )
		
	def _UnmountCallback( self, obj, res ):
		success = obj.unmount_finish( res )
		if( not success ):
			self._ReportError( 'Unmount failed' )
			
class UsbDeviceState( FilesystemState ):
	def __init__( self, device_uuid, device_name, root_dir ):
		FilesystemState.__init__( self, root_dir )
		self.filename = 'state.{}_{}.filesystem'.format( device_name, device_uuid )
