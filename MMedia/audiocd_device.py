#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from filesystem_device import *
import gio	#I need it to keep the mount object so I can eject

__all__ = [ 'AudioCDDevice' ]
class AudioCDDevice( Filesystem ):
	def __init__( self, root_dir, abstract_device, gio_mount, GetSelectedListFilesCallback = None, SetPlaylistLabelTextCallback = None, GetSelectedPlaylistItemsCallback = None ):
		#print( 'root_dir: {}'.format( root_dir ) )
		#print( 'gio_mount.root_dir: {}'.format( gio_mount.get_root().get_path() ) )
		self.root_dir = root_dir	#needs to be here because Filesystem.__init__ first calls MediaDevice.__init__ and then sets self.root_dir
		self._gio_mount = gio_mount
		infos = gio_mount.get_root().enumerate_children('standard::name,standard::type,standard::size')
		self.tracks = [ i for i in infos if i.get_file_type() == gio.FILE_TYPE_REGULAR ]

		Filesystem.__init__( self, abstract_device, self.root_dir, GetSelectedListFilesCallback, SetPlaylistLabelTextCallback, GetSelectedPlaylistItemsCallback )
		
		#set file_items after Filesystem constructor
		self.file_items = [ 
			FileItem( 
				name = os.path.join( self.root_dir, t.get_name() ),
				file_type = FileItem.FILE_TYPE, 
				text = t.get_name(),
				is_enabled = True, 
				is_playlist = False
			) for t in self.tracks
		]

				
	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		settings = self._GetSettings()
		return AudioCDDeviceState( self.root_dir, settings._speeddial_rows, settings._speeddial_buttons_per_row, self.tracks )
		
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return AudioCDDeviceSettings( self.root_dir, self.tracks )
		
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
				'playlist_next',
				'eject'
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
			'speeddial_previous':[ False, None ],
			'speeddial_next':[ False, None ],
			'playlist_previous':[ True, None ],
			'playlist_next':[ True, None ],
			'subtitles':[ False, None ],
			'shuffle':[ True, [ [wx.EVT_BUTTON, self.OnShuffle] ] ],
			'repeat':[ True, [ [wx.EVT_BUTTON, self.OnRepeat] ] ],
			'eject': [ True, [ [wx.EVT_BUTTON, self.OnEject ] ] ] 
		}

	def HasVideoSettings( self ):
		return False

	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions
	
	def OnEject( self, event ):
		dial = wx.MessageDialog(
			None, 
			'Are you sure you want to eject ' + self.name + ' ?', 
			'Eject CD', 
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
			)
		if( dial.ShowModal() == wx.ID_YES ):
			if( self.media_player.IsPlaying() ):
				self.media_player.Stop()
			#subprocess.call( ['sudo', 'eject', 'cdda://sr0/' ] ) #self.dev_path] )
			self._gio_mount.eject( self.OnAfterEject )
			
	def OnAfterEject( self, arg0, arg1 ):
		#TODO: not sure what args 0 and 1 are
		pass
		
	def _ReadDir( self, directory ):
		self.UpdateFilelistObservers()
			
class AudioCDDeviceSettings( MediaDeviceSettings ):
	def __init__( self, root_folder, tracks ):
		MediaDeviceSettings.__init__( self )
						
		#self._speeddial_rows = 3
		self._speeddial_buttons_per_row = 10
		self._speeddial_rows = ( len( tracks ) / 10 ) + ( 1 if len( tracks ) % 10 > 0 else 0 )
		self._speeddial_rows = min( 3, self._speeddial_rows )
		self._track_count = len( tracks )
		self.root_folder = root_folder
		
	def GetSpeedDialButtonTotal( self ):
		return self._track_count
		
class AudioCDDeviceState( FilesystemState ):
	def __init__( self, current_dir, speeddial_rows, speeddial_buttons_per_row, songs ):
		self._songs = songs
		self.audiocd_current_dir = current_dir #in a bug this was changed and wronlgy loaded by FilesystemState.Load
		FilesystemState.__init__( self, current_dir )
		self.filename = 'state.audiocd.filesystem'
		self._SetSpeedDials()

	def _SetSpeedDials( self ):
		self.speed_dials = {}
		for i in range( len( self._songs ) ):
			#print( 'speeddial["{}"] = {}'.format( str(i+1), os.path.join( self.audiocd_current_dir, self._songs[i].get_name() ) ) )
			self.speed_dials[ str( i+1 ) ] = os.path.join( self.audiocd_current_dir, self._songs[i].get_name() )	#speeddial index starts from 1, because it is the displayed label
			
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
		
