#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import json
import random
import datetime
import logging

from custom_controls.mmedia_list import *
from media_device import *
from media_player import MediaPlayer
from file_item import *
from subtitles_dlg import *
				
class Filesystem( MediaDevice ):
	ACTIVE_FILELIST = 0
	ACTIVE_PLAYLIST = 1
	
	def __init__( self, abstract_device, root_dir = '/', GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectePlaylistItemsCallback = None ):
		MediaDevice.__init__( self, abstract_device.name, abstract_device.dev_path, abstract_device.dev_type, abstract_device._mmedia_gui, abstract_device._gui_media_functions, abstract_device._playerLock, abstract_device._error_reporter, abstract_device._message_reporter, GetSelectedSystemPlaylistItemsCallback = abstract_device._GetSelectedSystemPlaylistItemsCallback )
		self.player = None
		self.root_dir = root_dir
		self._GetSelectedListFilesCallback = GetSelectedListFilesCallback
		self._SetPlaylistLabelTextCallback = SetPlaylistLabelTextCallback
		self._GetSelectePlaylistItemsCallback = GetSelectePlaylistItemsCallback
		self.current_dir = self.state.current_dir
		self.file_items = []
		self.playlist_items = []
		#self._ReadDir( self.current_dir ) #Cannot call _ReadDir so early. Only after InitUI. Only then I have a player. _ReadDir uses it to determine playable files
		self.active_list = Filesystem.ACTIVE_FILELIST
		
#All concrete devices should override the following functions
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return FilesystemSettings()

	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return FilesystemState()
		
	def Activate( self ):
		MediaDevice.Activate( self )
					
	def Deactivate( self ):
		MediaDevice.Deactivate( self )
		if( self.media_player and self.media_player.IsPlaying() ):
			self.media_player.Pause()
				
	def _DevPlaylistFunctions( self ):
		'''
		Returns a dictionary. The keys are the playlist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'new': self.NewPlaylist, 'clear': self.ClearPlaylist, 'save': self.SavePlaylist, 'add': None, 'edit': None,'delete': self.RemovePlaylistItem, 'scan': None, 'cd_to_dir': self.CDToDir }
		
	def _DevFilelistFunctions( self ):
		'''
		Returns a dictionary. The keys are the filelist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'move_up_folder': self._MoveUpFolder, 'play_all': self._MovePlayableFilesToPlaylist, 'play_selected': self._MoveSelectedFilesToPlaylist, 'refresh': self._ReReadDir }
		
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'play',
				'previous',
				'next',
				'speeddial_previous',
				'speeddial_next'
				'rewind',
				'forward',
			]
		else:
			return [			
				'step_back'
				'step_forward',
				'playlist_previous',
				'playlist_next',
				'subtitles',
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
			'subtitles':[ True, None ],
			'shuffle':[ True, [ [wx.EVT_BUTTON, self.OnShuffle] ] ],
			'repeat':[ True, [ [wx.EVT_BUTTON, self.OnRepeat] ] ],
			'eject': [ False, None ] 
		}
		
	def MediaButtonIsPressed( self, media_button_function_name ):
		'''
		This function is used to determine the state of the media button e.g.
		when the user selects a device, and the device is activated.
		For example, if a device should start with media_button "Repeat" 
		(i.e. loop a playlist) the device should return True
		'''
		#print( 'Filesystem.MediaButtonIsPressed was called for {}'.format( media_button_function_name ) )
		is_pressed = False #default for all media button functions
		
		if( media_button_function_name == 'repeat' ):
			is_pressed = self.state.repeat
		elif( media_button_function_name == 'shuffle' ):
			is_pressed = self.state.shuffle
			
		#print( '\treturning {}'.format( is_pressed ) )
		return is_pressed
		
	def MediaButtonIsEnabled( self, media_button_function_name ):
		if( media_button_function_name == 'subtitles' ):
			return self.SubtitlesAreAvailable()
			
		#all other media buttons
		return True
		
	def Play( self ):
		print( 'will try to play my _current_track_hash: {}'.format( self._current_track_hash ) )
		#self.DumpFilelistItems()
		if( not self._current_track_hash ):
			logging.debug( 'not self._current_track_hash, will do nothing' )
			return
		if( not any( i.Hash() == self._current_track_hash for i in self.playlist_items ) ):
			logging.debug( 'not in playlist, will do nothing' )
			logging.debug( 'my playlist items are:\n' )
			for i in self.playlist_items:
				logging.debug( '{}'.format( i.Hash() ) )
			return
		file_item = next( i for i in self.playlist_items if i.Hash() == self._current_track_hash )
		logging.debug( 'And my file item is: {}'.format( file_item.name ) ) ; file_item.Dump()
		if( not	self.IsPlayableFile( file_item ) ):
			logging.debug( '{} is not a playable file, will do nothing'.format( file_item.name ) )
			return
			
		logging.debug( 'I am passing it to the media player...' )
		self.media_player.Play( self.GetMediaStringForPlayer( file_item.name ) )
		MediaDevice.Play( self )
		
	def PlayTrack( self, track_hash ):
		print( 'was asked to play track_hash {}'.format( track_hash ) )
		
		#if( not any( i.Hash() == track_hash for i in self.file_items ) ):
			#raise Exception( 'Unknown file item with hash {}'.format( track_hash ) )
			
		#file_item = next( i for i in self.file_items if i.Hash() == track_hash )
		#if( file_item.file_type == FileItem.FOLDER_TYPE ):
		if( all( i.Hash() != track_hash for i in self.playlist_items ) ):	#not already loaded in playlist			
			if( self.IsDir( track_hash ) ):
				self.current_dir = track_hash
				self.state.SetCurrentDir( self.current_dir )
				#print( 'self.current_dir is now {}'.format( self.current_dir ) )
				self._ReadDir( self.current_dir )
			else:
				parent_dir = self._GetValidParentDir( os.path.abspath( track_hash ) )#, os.path.pardir ) )
				#print( 'parent of {} is {}'.format( track_hash, parent_dir ) )
				#print( 'comparing parent {} to current {}'.format( parent_dir, self.current_dir ) )
				#
				#Cancelled. We don't chande dir when playing a file from another dir
				#if( self.current_dir != parent_dir ):
					#self.current_dir = os.path.abspath(os.path.join( track_hash, os.path.pardir) )#parent dir of file
					#self.state.SetCurrentDir( self.current_dir )
					#self._ReadDir( self.current_dir )
				#
				#
				#self.playlist_items = []
				#self._current_playlist_hash = None
				if( self.FileIsPlaylist( track_hash ) ):
					self.playlist_items = []
					playlist_files = self.ReadM3UPlaylist( track_hash )
					if( self._SetPlaylistLabelTextCallback ):
						self._SetPlaylistLabelTextCallback( os.path.splitext( os.path.basename( track_hash ) )[0] )
					for f in playlist_files:
						full_file_path = os.path.abspath( f )
						self.playlist_items.append( self.GetMediaItem( full_file_path )
							#FileItem( 
								#full_file_path, 
								#FileItem.FILE_TYPE, 
								#is_enabled = self.MediaIsValid( full_file_path ),
								#is_playlist = self.FileIsPlaylist( full_file_path )
								#) 
							)
					#print( self.playlist_items )
					self._current_playlist_hash = track_hash
					track_hash = self.playlist_items[0].Hash()
				else:
					full_file_path = track_hash #os.path.abspath( track_hash )
					self.playlist_items.append( self.GetMediaItem( full_file_path )
						#FileItem( 
							#full_file_path, 
							#FileItem.FILE_TYPE, 
							#is_enabled = self.MediaIsValid( full_file_path ),
							#is_playlist = self.FileIsPlaylist( full_file_path )
							#) 
					)					
				self.UpdatePlaylistObservers()

		#This line will execute Play among other things so call it after eveything else is ready
		MediaDevice.PlayTrack( self, track_hash )
		
	def GetCurrentTrackText( self ):
		return os.path.basename( self._current_track_hash )
		
	def GetFilelistItems( self ):
		'''
		Returns the contents of the current folder
		'''
		#print( 'GetFilelistItems returns {} items:'.format( len( self.file_items ) ) )		
		return self.file_items
			
	def GetPlaylistItems( self ):
		return self.playlist_items
		
	def GetCurrentDirectoryHash( self ):
		return self.current_dir
		
	def TrackHashIsValid( self, track_hash ):
		'''This should be overriden only by fm_radio
		'''
		return True
			
	def GetMute( self ):
		return self.media_player.GetMute()

	def SetMute( self, on ):
		self.media_player.SetMute( on )
		
	def SetVolume( self, volume ):
		self.media_player.SetVolume( volume )

	def GetVolume( self ):
		return self.media_player.GetVolume()

	def MediaIsValid( self, media_hash ):
		'''
		media_hash is expected to be a file path
		'''
		return self.media_player.MediaIsValid( media_hash )
		
	#End of functions to be overriden by concrete devices
	
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions

	def InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		MediaDevice.InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback )
		#self.media_player = MediaPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
		self.media_player = self._CreateMediaPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
		self.media_player.AddStereoMonoObserver( self )
		self.media_player.AddEndOfTrackObserver( self )
		self.media_player.AddPosChangeObserver( self )
		self.media_player.AddPlayingObserver( self )
		self.media_player.AddPausedObserver( self )
		self._video_panel = self.media_player.video_panel
		#self._controls_panel = self.player.ctrlpanel
		self._video_panel_parent.GetSizer().Add( self._video_panel, 1, wx.EXPAND )
		self._ReadDir( self.current_dir )
			
	def MainFrameInitUIFinished( self ):
		'''
		For any device that requires to initialize stuff after the parent is Shown
		e.g. vlc based tv tunr
		'''
		pass
		
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path )
				
	def NeedsMedia( self ):
		return False
		
	def SupportsStereoMono( self ):
		return True
		
	def Stop( self ):
		self.media_player.Stop()
		MediaDevice.Stop( self )
				
	#End of functions that may be overriden
	
	def OnStepBack( self, event ):
		self.media_player.MoveTrackTime( -30000 )
	
	def OnStepForward( self, event ):
		self.media_player.MoveTrackTime( 30000 )
			
	def OnRewind( self, event = None ):
		self.media_player.MoveTrackTime( -10000 )
		
	def OnForward( self, event = None ):
		self.media_player.MoveTrackTime( 10000 )
			
	def OnEndOfTrack( self ):
		print( 'I am an observer of OnEndOfTrack and will run OnEndOfTrack...' )
		#try:
		if( self.state.repeat ):
			items = []
			#if( self.active_list == Filesystem.ACTIVE_FILELIST ):
				#items = [ i for i in self.GetFilelistItems() if os.path.isfile( i.name ) ]
			#else:
			items = self.GetPlaylistItems()
				
			#current_track = next( i for i in items if i.Hash() == self._current_track_hash )
			current_track = None
			for i in items:
				print( 'will compare {} ({}) against {} ({})'.format( i.Hash(), i.Hash().__class__, self._current_track_hash, self._current_track_hash.__class__ ) )
				if( i.Hash() == self._current_track_hash ):
					current_track = i
					break
			next_track_index = 0
			if( current_track ):
				if( self.state.shuffle and len( items ) > 1 ):
					print( 'I am shuffling...' )
					next_track_index = random.randrange( 0, len( items ) - 1 )
					print( 'next_track_index: {}'.format( next_track_index ) )
					if( next_track_index == items.index( current_track ) ):
						next_track_index = ( next_track_index + 1 ) % len( items )
						print( 'but this is what I am already playing so next_track_index:{}'.format( next_track_index ) )
				else:
					next_track_index = ( items.index( current_track ) + 1 ) % len( items )
					print( 'I am NOT shuffling so next_track_index:{}'.format( next_track_index ) )
			
			self.PlayTrack( items[ next_track_index ].Hash() )
		#except:
			#import sys; print('Error: %s' % sys.exc_info()[1])
			#pass
		
		print( 'I am an observer of OnEndOfTrack and OnEndOfTrack finished.' )
		
	def OnPosChange( self, pos ):
		'''
		pos is a tuple containing ( player.get_time(), player.get_media().get_duration(), player.get_position() )
		player.get_position() is [0.0 .. 1.0]
		'''
		( player_time, media_duration, player_position ) = pos
		#print( 'I am an observer of OnPosChange and received OnPosChange with player_time: {}, duration: {}, player_position: {}'.format( datetime.timedelta( milliseconds = player_time ), datetime.timedelta( milliseconds = media_duration ), str( player_position ) ) )
		duration_delta = datetime.timedelta( milliseconds = media_duration )
		s = duration_delta.seconds
		hours, remainder = divmod(s, 3600)
		minutes, seconds = divmod(remainder, 60)
		self._mmedia_gui.SetPlayProgressDuration( '{:02d}:{:02d}:{:02d}'.format( hours, minutes, seconds ) )
		
		time_delta = datetime.timedelta( milliseconds = player_time )
		s = time_delta.seconds
		hours, remainder = divmod(s, 3600)
		minutes, seconds = divmod(remainder, 60)		
		position = round( player_position * 100, 0 )
		self._mmedia_gui.SetPlayProgressPosition( position, '{:02d}:{:02d}:{:02d}'.format( hours, minutes, seconds ) )
		
	def OnShuffle( self, event ):
		button = event.GetEventObject()
		media_button = self._mmedia_gui.GetMediaButtonByFunctionName( button.function_name )
		print( 'filesystem OnShuffle function: {}, media_button: {}, is_pressed: {}'.format( button.function_name, media_button, media_button.is_pressed ) )
		self.state.SetShuffle( media_button.is_pressed )
		event.Skip()
		
	def OnRepeat( self, event ):
		button = event.GetEventObject()
		media_button = self._mmedia_gui.GetMediaButtonByFunctionName( button.function_name )
		self.state.SetRepeat( media_button.is_pressed )
		event.Skip()
		
	def OnPlay( self, event ):
		if( not self.is_active ):
			print( 'I {} am not active, cannot respond to event play'.format( self.name ) )
			return
			
		button = event.GetEventObject()
		media_button = self._mmedia_gui.GetMediaButtonByFunctionName( button.function_name )
		if( media_button.is_pressed ):
			if( self._current_track_hash is not None and len( self._current_track_hash ) > 0 ):
				self.Play()
			else:
				self._mmedia_gui.RefreshMediaButton( media_button )
		else:
			self.Pause() #self.Stop()
		event.Skip()
		
	def Pause( self ):
		self.media_player.Pause()
			
	def _GetValidParentDir( self, directory ):
		'''
		Will return None if there is no parent dir (i.e. this is the root directory)
		'''
		parent_dir = os.path.abspath(os.path.join( directory, os.path.pardir) )
		#print( 'parent of {} is {}, root_dir is {}'.format( directory, parent_dir, self.root_dir ) )
		if( parent_dir != directory and directory != self.root_dir ):
			#print( 'adding {} as ".." to the list of files'.format( parent_dir ) )
			#self.file_items.append( FileItem( parent_dir, FileItem.FOLDER_TYPE, '..' ) )
			return parent_dir
			
		return None
		
	def _ReadDir( self, directory ):
		del self.file_items[:]
		self.file_items = MediaDevice.ReadDirectory( self, directory )
		self.UpdateFilelistObservers()
		
	def _ReReadDir( self, event ):
		if( self.current_dir ):
			self._ReadDir( self.current_dir )
			
	def _MoveUpFolder( self, event ):
		logging.debug( '_MoveUpFolder: self.current_dir: {}'.format( self.current_dir ) )
		if( not self.current_dir ):
			logging.debug( '\treturning, no current_dir found ...' )
			return
		parent_dir = self._GetValidParentDir( self.current_dir )
		logging.debug( '\tparent_dir of {} is {}'.format( self.current_dir, parent_dir ) )
		if( parent_dir ):
			logging.debug( '\twill playtrack {} to move to parent_dir'.format( parent_dir ) )
			self.PlayTrack( parent_dir )
	
	def IsDir( self, track_hash ):
		return os.path.isdir( track_hash )
		
	def IsPlayableFile( self, file_item ):
		return file_item.is_enabled and not file_item.is_playlist and not os.path.isdir( file_item.name )
		
	def GetMediaItem( self, track_hash ):
		return FileItem( 
				track_hash, 
				( FileItem.FOLDER_TYPE if self.IsDir( track_hash ) else FileItem.FILE_TYPE ), 
				is_enabled = self.MediaIsValid( track_hash ),
				is_playlist = self.FileIsPlaylist( track_hash )
			) 
			
	def FilterUnplayableFileItems( self, file_items ):
		return [ i for i in file_items if self.IsPlayableFile( i ) ]
		
	def _MovePlayableFilesToPlaylist( self, event ):
		self.playlist_items = self.FilterUnplayableFileItems( self.file_items )
		#print( self.playlist_items )
		self.UpdatePlaylistObservers()
					
	def _MoveSelectedFilesToPlaylist( self, event ):
		print( '_MoveSelectedFilesToPlaylist' )
		if( self._GetSelectedListFilesCallback ):
			print( 'have self._GetSelectedListFilesCallback' )
			self.playlist_items = self.FilterUnplayableFileItems( self._GetSelectedListFilesCallback() )
			print( 'got {} playlist_items'.format( len( self.playlist_items ) ) )
			self.UpdatePlaylistObservers()
		
	def ClearPlaylist( self, event = None ):
		self.playlist_items = []
		self._current_track_hash = None
		self._current_playlist_hash = None
		self.Stop()
		self.UpdatePlaylistObservers()
		
	def NewPlaylist( self, event ):
		if( self._SetPlaylistLabelTextCallback ):
			self._SetPlaylistLabelTextCallback( 'New' )
		self._current_playlist_hash = None
		self.ClearPlaylist()
		
	def RemovePlaylistItem( self, event ):
		if( self._GetSelectePlaylistItemsCallback ):
			items = self._GetSelectePlaylistItemsCallback()
			self.playlist_items = [ i for i in self.playlist_items if i not in items ]
			self.UpdatePlaylistObservers()
			
	def CDToDir	( self, event ):
		if( self._GetSelectePlaylistItemsCallback ):
			items = self._GetSelectePlaylistItemsCallback()
			if( not items or len( items ) == 0 ):
				return
			cd_dir = os.path.dirname( items[0].Hash() )
			#print( 'will try to cd to {}'.format( cd_dir ) )
			self.current_dir = cd_dir
			self.state.SetCurrentDir( self.current_dir )
			self._ReadDir( self.current_dir )
		
	def _CreateMediaPlayer( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		return MediaPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
		
	def GetMediaStringForPlayer( self, item_str ):
		'''
		For almost any filesystem derived device this is just the item_str
		But for the UPnP MediaServer device this is the mediaservers hostname concat with the object's id
		There is a bug here. Some object id's come prefixed with '/'. If this is concatenated to
		http://hostname/ there will be two '/' after the hostname and this is a "not exists" error
		'''
		return item_str
	
	def GetSubtitlesDialog( self, dialog_parent, SelectedSubtitlesCallback ):
		return FileSubtitlesDlg( dialog_parent, SelectedSubtitlesCallback, self.root_dir, self.current_dir, self.GetCurrentSubtitle() )
	
	def GetCurrentSubtitle( self ):
		subtitle = ''
		if( self.media_player ):
			subtitle = self.media_player.GetCurrentSubtitle()
		return subtitle
			
	def SetSubtitle( self, show_subtitles, subtitle_object ):
		if( not show_subtitles ):			
			return self.StopSubtitles()
			
		if( subtitle_object is None ):
			logging.debug( 'None subtitle object in FilesystemDevice.SetSubtitle' )
			return False
			
		if( self.media_player ):
			if( not self.media_player.SetSubtitleFile( subtitle_object ) ):
				self._ReportError( 'Could not set subtitle file {}'.format( subtitle_object ) )
		else:
			self._ReportError( 'No media player in device.Weird!' )
			
	def StopSubtitles( self ):
		logging.debug( 'StopSubtitles:' )
		if( self.media_player ):
			success = self.media_player.SetSubtitleByIndex( 0 )
			logging.debug( '\tI have a player and returned {}'.format( success ) )
			return success
			
		logging.debug( '\tI have no player, returning False' )
		return False
			
	def SubtitlesAreAvailable( self ):
		return self.media_player.MediaIsVideo()
		
	def MediaPlayerIsPlaying( self ):
		self._mmedia_gui.GU_IsPlaying()
		
	def MediaPlayerPaused( self ):
		self._mmedia_gui.GU_IsPaused()
		
class FilesystemSettings( MediaDeviceSettings ):
	def __init__( self ):
		MediaDeviceSettings.__init__( self )
		self._speeddial_rows = 3
		self._speeddial_buttons_per_row = 10
		self.root_folder = '/'
						
class FilesystemState( MediaDeviceState ):
	def __init__( self, current_dir = '/' ):
		self.current_dir = current_dir
		print( 'current_dir: {}'.format( current_dir ) )
		self.shuffle = False
		self.repeat = False
		self.filename = "state.filesystem"	#the file were the state is saved
		MediaDeviceState.__init__( self )
	
	def SetCurrentDir( self, directory ):
		self.current_dir = directory
		self.Save()
		
	def SetShuffle( self, shuffle ):
		self.shuffle = shuffle
		self.Save()
		
	def SetRepeat( self, repeat ):
		self.repeat = repeat 
		self.Save()
		
	def Load( self ):
		if( not os.path.isfile( self.filename ) ):
			return
		statinfo = os.stat( self.filename )
		if( statinfo.st_size == 0 ):
			return
		
		current_dir = self.current_dir #store temporarily
		with open( self.filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
		try:			
			if( not os.path.isdir( self.current_dir ) ):
				self.current_dir = current_dir
		except AttributeError:	#guard against the case that the saved state does not include a current_dir attribute
			self.current_dir = current_dir
		
	
	def Save(self):
		import pprint; pprint.pprint( self.__dict__ )
		with open( self.filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )		

if __name__ == '__main__':
	for i in glob.glob( '/*' ):
		print i
