#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import json
import random
import datetime
import logging
#import time
#from threading import Thread
from custom_controls.mmedia_list import *
from media_device import *
from media_player_device import *
from media_player import MediaPlayer
from file_item import *
from subtitles_dlg import *
from device_behavior_on_activate import *
from progress_pulse_dialog import ProgressPulseDlg


class Filesystem( MediaPlayerDevice ):
	ACTIVE_FILELIST = 0
	ACTIVE_PLAYLIST = 1
	
	def __init__( self, abstract_device, root_dir = '/', GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectedPlaylistItemsCallback = None ):
		MediaPlayerDevice.__init__( self, abstract_device, SetPlaylistLabelTextCallback,GetSelectedPlaylistItemsCallback )
		self.media_player = None
		self.root_dir = root_dir
		self._GetSelectedListFilesCallback = GetSelectedListFilesCallback
		self.current_dir = self.state.current_dir
		self.file_items = []
		#I want initially when the app starts to have Filelist displayed for Filesystem devices
		self.state.SetActiveListId( Filesystem.ACTIVE_FILELIST )
	
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
	
	def _GetDeviceBehaviorOnActivate( self ):
		return DeviceBehaviorOnActivate( self, pause_on_deactivate = True, play_on_activate = True )

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
				'speeddial_next',
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
			'eject': [ False, None ],
			'refresh': [ True, [ [wx.EVT_BUTTON, self.OnRefresh] ] ]
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
	
	def OnRefresh( self, event ):
		self.PlayTrack( self.current_dir )

	def DoPlay( self ):
		local_success = False
		if( self._current_track_hash ):
			logging.debug( 'will try to play my _current_track_hash: {}'.format( self._current_track_hash.encode( 'utf-8' ) ) )
			#self.DumpFilelistItems()
			if( self._current_track_hash == self.current_dir ):
				logging.debug( 'This is my current dir, will just show it''s name' )
				#self._ShowMessage( self.GetCurrentTrackText() )
				local_success = False
			elif( not self._current_track_hash ):
				logging.debug( 'not self._current_track_hash, will do nothing' )
				local_success = False
			elif( not any( i.Hash() == self._current_track_hash for i in self.playlist_items ) ):
				logging.debug( 'not in playlist, will do nothing' )
				logging.debug( 'my playlist items are:' )
				for i in self.playlist_items:
					logging.debug( '{}'.format( i.Hash() ) )
				logging.debug( 'I am done here, returning False' )
				local_success = False
			else:
				file_item = next( i for i in self.playlist_items if i.Hash() == self._current_track_hash )
				logging.debug( 'And my file item is: {}'.format( file_item.name.encode( 'utf-8' ) ) ) ; file_item.Dump()
				if( self.IsPlayableFile( file_item ) ):
					logging.debug( 'I am passing it to the media player...' )
					self.media_player.Play( self.GetMediaStringForPlayer( file_item.name ) )
					local_success = True
				else:
					logging.debug( '{} is not a playable file, will do nothing'.format( file_item.name ) )
					local_success = False
				
		return MediaDevice.DoPlay( self ) and local_success

	def IsPlaying( self ):
		'''
		Devices that use media_players should override this function and return True if the media_player is playing
		'''
		if( not self.media_player ):
			return False
			
		return self.media_player.IsPlaying()
	
	#def PlayTrack( self, track_hash ):
		#ProgressPulseDlg( 
			#parent = self._mmedia_gui,
			#message = 'Opening {}'.format( track_hash.encode( 'utf-8' ) ),
			#worker_method = self.DoPlayTrack,
			#worker_method_args = [ track_hash ]
			#)
		#the same thing donw with standard wx.ProgressDialog
		#dlg = wx.ProgressDialog( 
			#title = 'Opening {}'.format( track_hash.encode( 'utf-8' ) ),
			#message = 'Please wait'.format( track_hash.encode( 'utf-8' ) ),
			#parent = self._mmedia_gui,
			#style = wx.PD_AUTO_HIDE|wx.PD_APP_MODAL|wx.PD_SMOOTH			
			#)
		#th_dp = Thread( target = self.DoPlayTrack, args = [ track_hash ], group = None ) #group = None because some wird library assertion runs and complains about it if it is missing
		#th_dp.start()
		#
		#def Pulse( progress_dlg, worker_thread ):
			#while( True ):
				#try:
					#if( not worker_thread.is_alive() ):
						#logging.debug( 'Pulse: the worker thread finished so I am done now' )
						#wx.CallAfter( progress_dlg.Update, 100 )
						#break;
					#wx.CallAfter( dlg.Pulse )
					#time.sleep( 0.05 )
				#except:
					#logging.debug( 'Pulse crashed, most probably the progress dialog closed' )
					#break
			#logging.debug( 'Pulse finished' )
		#
		#th_pulse = Thread( target = Pulse, args = [ dlg, th_dp ], group = None )
		#th_pulse.start()
	
	def DoPlayTrack( self, track_hash ):
		logging.debug( 'was asked to play track_hash {}'.format( track_hash.encode( 'utf-8' ) ) )
		
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
				#Must NOT do MediaDevice.DoPlayTrack because if the device is already playing it will stop and start over again (very annoying)
				return False
			else:
				#parent_dir = self._GetValidParentDir( os.path.abspath( track_hash ) )#, os.path.pardir ) )
				#print( 'parent of {} is {}'.format( track_hash, parent_dir ) )
				#print( 'comparing parent {} to current {}'.format( parent_dir, self.current_dir ) )
				#
				#Cancelled. We don't change dir when playing a file from another dir
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
						text = os.path.splitext( os.path.basename( track_hash ) )[0]
						wx.CallAfter( self._SetPlaylistLabelTextCallback, text )
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
		MediaDevice.DoPlayTrack( self, track_hash )
	
	def SetCurrentTrack( self, track_hash ):
		'''
		This function is overriden by filesystem devices. The current_track_hash will not change if track_hash is a dir
		'''
		if( not self.IsDir( track_hash ) ):
			MediaDevice.SetCurrentTrack( self, track_hash )

	def ShowPlaylistAfterPlayTrack( self ):
		'''
		This function is overriden by filesystem devices to return False if the PlayTrack was used to change directory i.e. the track that was played was a directory
		'''
		if( self._current_track_hash == self.current_dir ):
			return False
		
		return True
	
	def GetCurrentTrackText( self ):
		if( self._current_track_hash ):
			return os.path.basename( self._current_track_hash )
		elif( self.current_dir ):
			return self.current_dir
		
		return ''
	
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
	
	def HasVideoSettings( self ):
		return True

	def UseMediaListsWithImages( self ):
		return True

	#End of functions to be overriden by concrete devices
	
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions

	def InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		MediaPlayerDevice.InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback )
		self._ReadDir( self.current_dir )
	
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path )
	
	def NeedsMedia( self ):
		return False
	
	def SupportsStereoMono( self ):
		return True
	
	#End of functions that may be overriden
	
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
		logging.debug( '_MoveUpFolder: self.current_dir: {}'.format( self.current_dir.encode( 'utf-8' ) ) )
		if( not self.current_dir ):
			logging.debug( '\treturning, no current_dir found ...' )
			return
		parent_dir = self._GetValidParentDir( self.current_dir )
		logging.debug( '\tparent_dir of {} is {}'.format( self.current_dir.encode( 'utf-8' ), parent_dir.encode( 'utf-8' ) ) )
		if( parent_dir ):
			logging.debug( '\twill playtrack {} to move to parent_dir'.format( parent_dir.encode( 'utf-8' ) ) )
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
	
	def CDToDir	( self, event ):
		if( self._GetSelectedPlaylistItemsCallback ):
			items = self._GetSelectedPlaylistItemsCallback()
			if( not items or len( items ) == 0 ):
				return
			cd_dir = os.path.dirname( items[0].Hash() )
			#print( 'will try to cd to {}'.format( cd_dir ) )
			self.current_dir = cd_dir
			self.state.SetCurrentDir( self.current_dir )
			self._ReadDir( self.current_dir )
			self._ShowMessage( self.current_dir )
	
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
			logging.debug( 'Setting subtitle file: {}'.format( subtitle_object ) )
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

class FilesystemSettings( MediaDeviceSettings ):
	def __init__( self ):
		MediaDeviceSettings.__init__( self )
		self._speeddial_rows = 3
		self._speeddial_buttons_per_row = 10
		self.root_folder = '/'

class FilesystemState( MediaPlayerDeviceState ):
	def __init__( self, current_dir = '/' ):
		self.current_dir = current_dir
		print( 'current_dir: {}'.format( current_dir ) )
		self.filename = "state.filesystem"	#the file were the state is saved
		MediaPlayerDeviceState.__init__( self )
	
	def SetCurrentDir( self, directory ):
		self.current_dir = directory
		self.Save()

	def Load( self ):
		if( not os.path.isfile( self.filename ) ):
			return
		statinfo = os.stat( self.filename )
		if( statinfo.st_size == 0 ):
			return
		
		current_dir = self.current_dir #store temporarily
		with open( self.filename, mode='r' ) as f:
			data = json.load( f )
			#self.__dict__ = json.load( f )
			for key in self.__dict__:
				if( key in data.keys() ):
					self.__dict__[key] = data[key]
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
	#for i in glob.glob( '/*' ):
		#print i
	def Pulse( progress_dlg ):
		while( True ):
			#wx.CallLater( 1000, dlg.Pulse )
			wx.CallAfter( dlg.Pulse )
			time.sleep( 0.05 )
		
	app = wx.App()		
	dlg = wx.ProgressDialog( 
		title = 'Opening file',
		message = 'Please wait...',
		style = wx.PD_AUTO_HIDE|wx.PD_APP_MODAL|wx.PD_SMOOTH			
		)
	dlg.Close()
	th = Thread( target = Pulse, args = [ dlg ], group = None )
	th.start()
	app.MainLoop()
