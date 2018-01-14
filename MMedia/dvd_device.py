#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from filesystem_device import *
import gio	#I need it to keep the mount object so I can eject
from tv import vlc

__all__ = [ 'DVDDevice' ]

class DVDItem( MMediaListItem ):
	#_DVDTag = 'dvd'
	_DVDTag = 'dvdsimple'	#no dvd menus in libvlc
	def __init__( self, root_dir, gio_mount ):
		MMediaListItem.__init__( self, hash = '{}:// {}'.format( DVDItem._DVDTag, root_dir ), text = gio_mount.get_name(), is_enabled = True, is_playlist = False )
		self.root_dir = root_dir
		self.gio_mount = gio_mount
		
class DVDDevice( Filesystem ):
	def __init__( self, root_dir, abstract_device, gio_mount, GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectedPlaylistItemsCallback = None ):
		print( 'initing DVDDevice...' )
		self.root_dir = root_dir	#needs to be here because Filesystem.__init__ first calls MediaDevice.__init__ and then sets self.root_dir
		self._gio_mount = gio_mount
		#self.chapters = self._GetChapters()

		Filesystem.__init__( self, abstract_device, self.root_dir, GetSelectedListFilesCallback, SetPlaylistLabelTextCallback, GetSelectedPlaylistItemsCallback )
				
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		settings = self._GetSettings()
		return DVDDeviceState( self.root_dir )
		
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return DVDDeviceSettings( self.root_dir )
		
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
				'subtitles',
				'eject'
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
			'zap':[ False, None ],
			'play': [ True, [ [wx.EVT_BUTTON, self.OnPlay] ] ],
			'rewind':[ True, [ [wx.EVT_BUTTON, self.OnRewind] ] ], 
			'forward':[ True, [ [wx.EVT_BUTTON, self.OnForward] ] ], 
			'previous':[ False, None ],
			'next':[ False, None ],
			'step_back':[ True, [ [wx.EVT_BUTTON, self.OnStepBack] ] ],
			'step_forward':[ True, [ [wx.EVT_BUTTON, self.OnStepForward] ] ],
			'speeddial_previous':[ False, None ],
			'speeddial_next':[ False, None ],
			'playlist_previous':[ False, None ],
			'playlist_next':[ False, None ],
			'subtitles':[ True, None ],
			'shuffle':[ False, None ],
			'repeat':[ False, None ],
			'eject': [ True, [ [wx.EVT_BUTTON, self.OnEject ] ] ] 
		}
		
	def GetFilelistItems( self ):
		'''
		Returns the contents of the current folder
		'''
		return [ DVDItem( self.root_dir, self._gio_mount ) ]
		
	def GetPlaylistItems( self ):
		return [ DVDItem( self.root_dir, self._gio_mount ) ]
		
	def DoPlay( self ):
		#print( 'will try to play my _current_track_hash: {}'.format( self._current_track_hash ) )
		#self.DumpFilelistItems()
		#if( not self._current_track_hash ):
			#return
		#if( not any( i.Hash() == self._current_track_hash for i in self.playlist_items ) ):
			#return
		#file_item = next( i for i in self.playlist_items if i.Hash() == self._current_track_hash )
		#
		#if( not	os.path.isfile( file_item.name ) ):
			#return
			
		self.media_player.Play( self._current_track_hash )
		MediaDevice.DoPlay( self )
		
	def DoPlayTrack( self, track_hash ):
		print( 'was asked to play dvd {}'.format( track_hash ) )
		MediaDevice.DoPlayTrack( self, track_hash )
		
	#End of functions to be overriden by concrete devices
	
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions

	def OnEject( self, event ):
		dial = wx.MessageDialog(
			None, 
			'Are you sure you want to eject ' + self.name + ' ?', 
			'Eject DVD', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
			)
		if( dial.ShowModal() == wx.ID_YES ):
			if( self.media_player.IsPlaying() ):
				self.media_player.Stop()
			#subprocess.call( ['sudo', 'eject', self.dev_path] )
			self._gio_mount.eject( self.OnAfterEject )
			
	def OnAfterEject( self, arg0, arg1 ):
		#TODO: not sure what args 0 and 1 are
		pass
		
	def _GetChapters( self ):
		print( '_GetChapters' )
		instance = vlc.Instance()
		player = instance.media_player_new()
		m = instance.media_new( 'dvd://' )
		player.set_media( m )
		chapter_count = player.get_chapter_count()
		print( 'chapter_count: {}'.format( str( chapter_count ) ) )
		import pprint;
		pprint.pprint( player.get_chapter_description( 0 ) )
		
	def GetSubtitlesDialog( self, dialog_parent, SelectedSubtitlesCallback ):
		return DVDSubtitlesDlg( dialog_parent, SelectedSubtitlesCallback, self.media_player.GetSubtitlesList(), self.GetCurrentSubtitle() )
		
	def SetSubtitle( self, show_subtitles, subtitle_object ):
		if( not show_subtitles ):			
			return self.StopSubtitles()
			
		if( subtitle_object is None ):
			logging.debug( 'None subtitle object in DVDDevice.SetSubtitle' )
			return False
			
		if( self.media_player ):
			if( not self.media_player.SetSubtitleByIndex( subtitle_object ) ):
				self._ReportError( 'Could not set subtitle index {}'.format( subtitle_object ) )
		else:
			self._ReportError( 'No media player in device.Weird!' )
			
class DVDDeviceSettings( MediaDeviceSettings ):
	def __init__( self, root_folder ):
		MediaDeviceSettings.__init__( self )
						
		self._speeddial_rows = 0
		self._speeddial_buttons_per_row = 0
		#self._speeddial_rows = ( len( chapters ) / 10 ) + ( 1 if len( chapters ) % 10 > 0 else 0 )
		#self._speeddial_rows = min( 3, self._speeddial_rows )
		self.root_folder = root_folder
		
class DVDDeviceState( FilesystemState ):
	def __init__( self, current_dir ):
		self.dvd_current_dir = current_dir #in a bug this was changed and wronlgy loaded by FilesystemState.Load
		FilesystemState.__init__( self, current_dir )
		self.filename = 'state.audiocd.filesystem'
		self.speed_dials = {}		
		
	def SetSpeedDial( self, index, track_hash ):
		'''
		We don't set speed dials in audio cds. They are auto assigned to tracks
		'''
		pass
	
	def DelSpeedDial( self, index ):
		'''
		We don't set speed dials in audio cds. They are auto assigned to tracks
		'''
		pass
	
	def Load( self ):
		pass
	
	def Save( self ):
		pass
		
if __name__ == "__main__":
	instance = vlc.Instance()
	player = instance.media_player_new()
	m = instance.media_new( 'dvd:// /media/DANCING_WITH_WOLVES_DISC_2' )
	m.parse()
	print( 'mrl: {}'.format( m.get_mrl() ) )
	print( 'tracks info: {}'.format( m.get_tracks_info() ) )
	player.set_media( m )
	player.play()
	while True:
		pass
	chapter_count = player.get_chapter_count()
	print( 'chapter_count: {}'.format( str( chapter_count ) ) )
	print('Track: {}/{}'.format( player.video_get_track(), player.video_get_track_count() ) )
	#import pprint;
	#pprint.pprint( player.get_chapter_description( 0 ) )
