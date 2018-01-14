#!/usr/bin/python
# -*- coding: utf-8 -*-

from filesystem_device import *
from upnp_provider import *
from upnp_media_item import *
from upnp_media_player import *

class UPnPMediaServerDevice( Filesystem ):
	def __init__( self, upnp_hostInfo, upnp_device_name, upnp_provider, abstract_device, GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectePlaylistItemsCallback = None  ):
		self._upnp_hostInfo = upnp_hostInfo
		self._upnp_device_name = upnp_device_name
		self._upnp_provider = upnp_provider
		self._media_items = []
		Filesystem.__init__( self, 
			abstract_device, 
			root_dir = '0',
			GetSelectedListFilesCallback = GetSelectedListFilesCallback, 
			SetPlaylistLabelTextCallback = SetPlaylistLabelTextCallback, 
			GetSelectePlaylistItemsCallback = GetSelectePlaylistItemsCallback 
		)
		self.current_dir = self.root_dir
		self.current_dir_item = None
		self.current_media_item = None
		
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return UPnPMediaServerState()
		
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return UPnPMediaServerSettings()
		
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path )
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'play',
				'previous',
				'next',
				'playlist_previous',
				'playlist_next'
			]
		else:
			return [
				'rewind',
				'forward',
				'step_back'
				'step_forward',
				'shuffle',
				'repeat'
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
			'shuffle':[ True, [ [wx.EVT_BUTTON, self.OnShuffle] ] ],
			'repeat':[ True, [ [wx.EVT_BUTTON, self.OnRepeat] ] ],
			'eject': [ False, None ] 
		}
		
	def PlayTrack( self, track_hash ):
		'''
		I need to store locally the last played item, because if it is a container
		the ReadDir function will read it and then I will only have its hash and no
		other info
		'''
		self.current_media_item = self.GetMediaItem( track_hash )
		if( self.current_media_item.IsDir() ):
			self.current_dir_item = self.current_media_item
		Filesystem.PlayTrack( self, track_hash )
		
	def GetCurrentTrackText( self ):
		if( self.current_media_item ):
			return self.current_media_item.Text()
			
		return ''
		
	def GetFilelistItems( self ):
		'''
		Returns the contents of the current folder
		'''
		#print( 'GetFilelistItems returns {} items:'.format( len( self.file_items ) ) )		
		return self._media_items
	
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions
	
	def _GetValidParentDir( self, directory ):
		'''
		Will return None if there is no parent dir (i.e. this is the root directory)
		'''
		logging.debug( 'UPnPMediaServerDevice._GetValidParentDir...' )
		didllite_object_id = directory
		if( directory == self.root_dir or directory == 'http://{}/{}'.format( self._upnp_hostInfo['name'], self.root_dir ) ):
			logging.debug( '\treturning {}'.format( directory ) )
			return directory
		
		item = self.GetMediaItem( directory )
		if( not item ):
			logging.error( '_ReadDir: Did not find {} in the media items'.format( directory ) )
			#import traceback ; traceback.print_stack()
			return None
			
		parent_dir = item.ParentDir()
		logging.debug( '\treturning {}'.format( parent_dir ) )
		return ( parent_dir if parent_dir != '-1' else None )
		
	def _ReadDir( self, directory ):
		'''
		The root_dir = '0'. This may be browsed at any time, even at initialisation when
		no previous browsing has been performed
		'''
		logging.debug( '_ReadDir for dir: {}'.format( directory ) )
		didllite_object_id = directory
		if( directory != self.root_dir ):
			try:
				#Check my known items in order to avoid errors regarding leading slashed in the object id
				item = self.GetMediaItem( directory )
				if( item ):
					didllite_object_id = item.didllite_object.id
					logging.debug( '\tthis is a known item with id: {}'.format( didllite_object_id ) )
				else:
					parsed = urlparse( directory )
					didllite_object_id = parsed.path.strip( '/' )
					logging.debug( 'urlparse returns {}'.format( parsed ) )
			except:
				logging.error( '_ReadDir: Did not find {} in the media items'.format( directory ) )
				import traceback ; traceback.print_stack()
				didllite_object_id  = directory
		logging.debug( '_ReadDir will BrowseMediaServer for didllite_object_id: {}'.format( didllite_object_id ) )
		items = BrowseMediaServer( self._upnp_provider._upnp, self._upnp_hostInfo, self._upnp_device_name, didllite_object_id )
		if( items ):
			self._media_items = [ UPnPMediaItem( self._upnp_hostInfo['name'], x ) for x in items ]
			for x in self._media_items:
				logging.debug( 'added UPnPMediaItem: {}'.format( x.DumpStr() ) )
			self.UpdateFilelistObservers()
	
	def _MoveUpFolder( self, event ):
		logging.debug( 'UPnPMediaServerDevice._MoveUpFolder: self.current_dir: {}'.format( self.current_dir_item.DumpStr() ) )
		if( not self.current_dir_item ):
			logging.debug( '\treturning, no current_dir found ...' )
			return
			
		items = GetMetadata( self._upnp_provider._upnp, self._upnp_hostInfo, self._upnp_device_name, self.current_dir_item.didllite_object.parentID )
		if( items ):
			self.current_dir_item = UPnPMediaItem( self._upnp_hostInfo['name'], items[0] )
		else:
			self._ReportError( 'An error occured, cannot move up folder' )
			return
					
		self.current_dir = self.current_dir_item.name
		self.state.SetCurrentDir( self.current_dir )
		#print( 'self.current_dir is now {}'.format( self.current_dir ) )
		items = BrowseMediaServer( self._upnp_provider._upnp, self._upnp_hostInfo, self._upnp_device_name, self.current_dir_item.didllite_object.id )
		if( items ):
			self._media_items = [ UPnPMediaItem( self._upnp_hostInfo['name'], x ) for x in items ]
			for x in self._media_items:
				logging.debug( 'added UPnPMediaItem: {}'.format( x.DumpStr() ) )
			self.UpdateFilelistObservers()
			MediaDevice.PlayTrack( self, self.current_dir )
		
				
	def FileIsPlaylist( self, file_hash ):
		'''
		MediaServer media items are never playlists
		'''
		return False

	def IsDir( self, track_hash ):
		logging.debug( 'UPnPMediaServerDevice. Checking if {} is a dir'.format( track_hash ) )
		item = self.GetMediaItem( track_hash )
		if( not item ):
			logging.error( '\tDid not find {} in the media items'.format( track_hash ) )
			return False
			
		logging.debug( '\t{} is {}a directory'.format( track_hash, ( '' if item.IsDir() else 'NOT ' ) ) )
		return item.IsDir()
		
	def IsPlayableFile( self, file_item ):
		#import traceback;traceback.print_stack()
		logging.debug( 'UPnPMediaServerDevice.IsPlayableFile checking file {}'.format( file_item.name ) )
		is_playable = file_item.is_enabled and not file_item.is_playlist and not file_item.IsDir()
		logging.debug( 'is_enabled: {}, is_playlist: {}, IsDir(): {}, fileItem:[{}]'.format( file_item.is_enabled, file_item.is_playlist, file_item.IsDir(), file_item.DumpStr() ) )
		logging.debug( '\t returning {}'.format( is_playable ) )
		return is_playable
		
	def GetMediaItem( self, track_hash ):
		logging.debug( 'will try to get media item {}'.format( track_hash ) )
		#self.DumpMediaItems()
		logging.debug( 'self.current_media_item: {}'.format( ( self.current_media_item.DumpStr() if self.current_media_item else 'None' ) ) )
		item_list = self._media_items
		if( self.current_media_item ):
			item_list = self._media_items + [ self.current_media_item ]
		#for x in item_list :
			#logging.debug( 'x is a {}'.format( x.__class__ ) )
			#logging.debug( 'Searching x.name:{} for track_hash: {}'.format( x.name, track_hash ) )
			#if( x.name == track_hash ):
				#logging.debug( '\tFound it!' )
		try:
			item = next( ( x for x in item_list if x.name == track_hash ), None )
			if( item ):
				return item
			else:
				parsed = urlparse( track_hash )
				didllite_object_id = parsed.path.strip( '/' )
				items = GetMetadata( self._upnp_provider._upnp, self._upnp_hostInfo, self._upnp_device_name, didllite_object_id )
				if( items ):
					return UPnPMediaItem( self._upnp_hostInfo['name'], items[0] )
			return None
		except:
			import traceback, sys; traceback.print_exc()
			return None
		
	def DumpMediaItems( self ):
		for i in self._media_items:
			i.Dump()
			
	#Not required after all. Just refactored slightly MediaPlayer
	#def _CreateMediaPlayer( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		#return UPnPMediaPlayer( video_panel_parent, self._playerLock, self, video_panel_click_callback )
	
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
		
	# media resolver functions
	def MediaIsVideo( self, media_str ):
		item = self.GetMediaItem( media_str )
		if( item ):
			return item.IsVideo()
			
		logging.error( 'media {} is unknown, cannot determine if it is video'.format( media_str ) )
		return False
			
	def MediaIsAudio( self, media_str ):
		item = self.GetMediaItem( media_str )
		if( item ):
			return item.IsAudio()
			
		logging.error( 'media {} is unknown, cannot determine if it is audio'.format( media_str ) )
		return False
	# end of media resolver functions
	
class UPnPMediaServerSettings( MediaDeviceSettings ):
	def __init__( self ):
		MediaDeviceSettings.__init__( self )
		self._speeddial_rows = 0
		self._speeddial_buttons_per_row = 0
			
class UPnPMediaServerState( FilesystemState ):
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
