#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import random #for testing only
import json
import logging
logging.basicConfig( level = logging.DEBUG )

from chardet import detect

from custom_controls import MMediaListItem
from media_track import *
from file_item import *
from save_playlist_dialog import *

__all__ = [ 'MediaDevice', 'MediaTrack', 'MediaDeviceSettings', 'MediaDeviceState' ]

class MediaDeviceSettings:
	def __init__( self ):
		self._speeddial_rows = random.randint( 1, 3 )
		self._speeddial_buttons_per_row = random.randint( 6, 10 )
		
	#NOTE: devices such a dvd player should override this in the case for example
	#of an audio cd, where each speed dial should correspond to a track
	def GetSpeedDialRows( self ):
		return self._speeddial_rows
		
	def GetSpeedDialButtonsPerRow( self ):
		return self._speeddial_buttons_per_row
		
	def GetSpeedDialButtonTotal( self ):
		return self._speeddial_rows * self._speeddial_buttons_per_row
		
	def Load( self ):
		pass
		
	def Save( self ):
		pass
		
class MediaDeviceState:
	Filename = "state.device"	#the file were the state is saved
	def __init__( self ):
		self.speed_dials = {}
		
	def SetSpeedDial( self, index, track_hash ):
		self.speed_dials[index] = track_hash
		self.Save()
	
	def DelSpeedDial( self, index ):
		del self.speed_dials[index]
		self.Save()
		
	def Load( self ):
		if( not os.path.isfile( MediaDeviceState.Filename ) ):
			return
		with codecs.open( MediaDeviceState.Filename, mode='r', encoding='utf-8' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
	
	def Save(self):
		with codecs.open( MediaDeviceState.Filename, mode='w', encoding='utf-8' ) as f:
			json.dump( self.__dict__, f, indent=2 )			

class MediaDevice:
	TYPE_TV_TUNER = 0
	TYPE_FM_RADIO = 1
	TYPE_USB = 2
	TYPE_INTERNAL_HARD_DISK = 3
	TYPE_EXTERNAL_HARD_DISK = 4
	TYPE_DVD = 5
	TYPE_AUDIOCD = 6
	TYPE_UPNP_MEDIASERVER = 7
	TYPE_UPNP_MEDIARENDERER = 8
	TYPE_SAMBA_SHARE = 9
	TYPE_A2DP_BLUETOOTH_SOURCE = 10

	_dev_str_to_types = {
			'0': TYPE_TV_TUNER,
			'1': TYPE_FM_RADIO,
			'2': TYPE_USB,
			'3': TYPE_INTERNAL_HARD_DISK,
			'4': TYPE_EXTERNAL_HARD_DISK,
			'5': TYPE_DVD,
			'6': TYPE_AUDIOCD,
			'7': TYPE_UPNP_MEDIASERVER,
			'8': TYPE_UPNP_MEDIARENDERER,
			'9': TYPE_SAMBA_SHARE,
			'10': TYPE_A2DP_BLUETOOTH_SOURCE
		}
		
	_dev_capability = {
			TYPE_TV_TUNER: { 'numpad': False, 'numpad_decimal': False, 'filesystem': False, 'playlist': True, 'playlist_reordering': False, 'system_playlist': False, 'play_progress': False, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_FM_RADIO: { 'numpad': True, 'numpad_decimal': True, 'filesystem': False, 'playlist': True, 'playlist_reordering': False, 'system_playlist': False, 'play_progress': False, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_USB: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_INTERNAL_HARD_DISK: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_EXTERNAL_HARD_DISK: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_DVD: { 'numpad': False, 'numpad_decimal': False, 'filesystem': False, 'playlist': True, 'playlist_reordering': True, 'system_playlist': False, 'play_progress': True, 'clear_speeddial_button': False, 'speeddial': True },
			TYPE_AUDIOCD: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': False, 'speeddial': True },
			TYPE_UPNP_MEDIASERVER: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': False, 'speeddial': False },
			TYPE_UPNP_MEDIARENDERER: { 'numpad': False, 'numpad_decimal': False, 'filesystem': False, 'playlist': False, 'playlist_reordering': False, 'system_playlist': False, 'play_progress': True, 'clear_speeddial_button': False, 'speeddial': False },
			TYPE_SAMBA_SHARE: { 'numpad': False, 'numpad_decimal': False, 'filesystem': True, 'playlist': True, 'playlist_reordering': True, 'system_playlist': True, 'play_progress': True, 'clear_speeddial_button': True, 'speeddial': True },
			TYPE_A2DP_BLUETOOTH_SOURCE: { 'numpad': False, 'numpad_decimal': False, 'filesystem': False, 'playlist': False, 'playlist_reordering': False, 'system_playlist': False, 'play_progress': False, 'clear_speeddial_button': False, 'speeddial': False }
		}
	
	_dev_needs_media = {
			TYPE_TV_TUNER: False,
			TYPE_FM_RADIO: False,
			TYPE_USB: True,
			TYPE_INTERNAL_HARD_DISK: False,
			TYPE_EXTERNAL_HARD_DISK: False,
			TYPE_DVD: True,
			TYPE_AUDIOCD: True,
			TYPE_UPNP_MEDIASERVER: False,
			TYPE_UPNP_MEDIARENDERER: False,
			TYPE_SAMBA_SHARE: False,
			TYPE_A2DP_BLUETOOTH_SOURCE: False
		}
	
	def __init__( self, name = '', dev_path = '', dev_type = None, mmedia_gui = None, gui_media_functions = {}, playerLock = None,
					error_reporter = None, message_reporter = None, GetSelectedSystemPlaylistItemsCallback = None ):#, playlist_select_callback = None, numpad_trackhash_observer = None ):
		'''
		Note: Concrete devices should change dev_media_functions according to their specifics.
		dev_media_functions contains callback functions offered by MMediaGui such as zap etc.
		If any of these should not be available, the corresponding value in dev_media_functions
		should be set to None
		'''
		self._dev_supports_media_function = self._DevSupportsMediaFunction()
		self._gui_media_functions = gui_media_functions
				
		self.name = name
		self.dev_path = dev_path
		self.dev_type = dev_type
		self._mmedia_gui = mmedia_gui
		#self._playlist_select_callback = playlist_select_callback
		#import pprint; pprint.pprint( self._playlist_select_callback )
			
		self._dev_media_functions = self._MergeDevMediaFunctions( self._gui_media_functions )
		#print( '--------Media Device-----------\nself._dev_supports_media_function:' )
		#self.DumpDevMediaFunctions( self._dev_supports_media_function )
		#print( '\n\ngui_media_functions:' )
		#self.DumpDevMediaFunctions( gui_media_functions )
		#print( '\n\nself._dev_media_functions:' )
		#self.DumpDevMediaFunctions( self._dev_media_functions )
		#print( '--------Media Device-----------\n' )
		#import sys ; sys.exit()
		
		self._GetSelectedSystemPlaylistItemsCallback = GetSelectedSystemPlaylistItemsCallback
		
		self._playerLock = playerLock
		
		self._error_reporter = error_reporter
		self._message_reporter = message_reporter
		
		self.settings = self._GetSettings()
		self.settings.Load()
		self.state = self._GetState()
		self.state.Load()
		self.trackHashObservers = []
		self.signalStrengthObservers = [] #only used by the devices supporting signal strength
		self.stereoMonoObservers = [] #only used by the devices supporting stereo/mono
		
		self.filelistObservers = [] #will have their SetItems( items ) method called with the new filelist items
		self.playlistObservers = [] #will have their SetItems( items ) method called with the new playlist items
		self.systemplaylistsObservers = [] #will have their SetItems( items ) method called with the new playlist items
		self._current_track_hash = None
		self._current_playlist_hash = None

		self._is_stereo = False #testing only
		self.mute = False #testing only
		
		self._video_panel_parent = None
		self._video_panel = None
		
		self._controls_panel_parent = None
		self._controls_panel = None
		
	def GetVideoPanel( self ):
		return self._video_panel
		
	def GetControlsPanel( self ):
		return self._controls_panel
		
	def DumpDevMediaFunctions( self, media_functions_dict ):
		for function, value in media_functions_dict.iteritems():
			supported = value[0]
			binding = value[1]
			print( '{}:[{}, {}]'.format( function, supported, binding ) )
			
	def DumpFilelistItems( self ):
		items = self.GetFilelistItems()
		print( 'Dumping {} filelist items'.format( len( items ) ) )
		for i in items:
			i.Dump()
			
	@staticmethod
	def _RaiseNoConcreteImplementationException( method_name ):
		raise Exception( 'You should have implemented function {} in a concrete subclass of MediaDevice'.format( method_name ) )
		
	def _ReportError( self, error_msg ):
		if( self._error_reporter ):
			self._error_reporter.ReportError( error_msg )		
			
	def _ShowMessage( self, msg ):
		#print( '_ShowMessage called with msg "{}" and self._message_reporter:{}'.format( msg, self._message_reporter ) )
		if( self._message_reporter ):
			#print( 'media_device reporting message "{}"'.format( msg ) )
			self._message_reporter.ReportMessage( msg )		
		
	#def CanBeEjected( self ):
		#return MediaDevice._dev_ejectable_types[ self.dev_type ]
		
	def SupportsPlaylistFunction( self, function ):
		return self._SupportsMediaListFunction( function, self._DevPlaylistFunctions() )
		
	def SupportsFilelistFunction( self, function ):
		return self._SupportsMediaListFunction( function, self._DevFilelistFunctions() )
		
	def _SupportsMediaListFunction( self, function, list_functions ):
		supported = True
		if( not list_functions.has_key( function ) ):
			supported = False
		else:
			supported = list_functions[ function ] is not None
		#print( 'Medialist function "{}" is {} supported'.format( function, ( '' if supported else 'not' ) ) )
		return supported
		
	def ExecutePlaylistFunction( self, function ):
		if( self.SupportsPlaylistFunction( function ) ):
			playlist_functions = self._DevPlaylistFunctions()
			playlist_functions[function]()
			print( 'Executing playlist {}'.format( function ) )
			
	def GetPlaylistActionCallbacks( self ):
		#Debug only
		#return { 'new': self.DummyPlaylistCallback, 'clear': self.DummyPlaylistCallback, 'save': self.DummyPlaylistCallback, 'add': self.DummyPlaylistCallback, 'edit': self.DummyPlaylistCallback,'delete': self.DummyPlaylistCallback, 'scan': self.DummyPlaylistCallback }
		return self._DevPlaylistFunctions()
			
	def DummyPlaylistCallback( self, event ):
		button = event.GetEventObject()
		print( 'Dummy callback of {}'.format( button.action ) )
		
	def GetFilelistActionCallbacks( self ):
		return self._DevFilelistFunctions()
		
	def SupportsMediaFunction( self, media_function ):
		#import inspect; print ( 'called from {}'.format( inspect.stack()[1][3] ) )
		if( not self._dev_media_functions.has_key( media_function ) ):
			logging.debug( '{} not supported'.format( media_function ) )
			return False		
			
		#print( '{} supported:({})'.format( media_function, str( self._dev_media_functions[media_function][0] ) ) )
		return self._dev_media_functions[media_function][0]
		
	def BindMediaButton( self, wxbutton ):
		media_function = wxbutton.function_name
		if( not self.SupportsMediaFunction( media_function ) ):
			logging.debug( 'media function {} not supported by {}'.format( media_function, self.name ) )
			return
		
		#import pprint; pprint.pprint( self._dev_media_functions[media_function] )
		for binding in 	self._dev_media_functions[media_function][1]:
			#logging.debug( 'Type of binding is {}'.format( type( binding ) ) )
			if( binding is None ): #or type( binding ) != List ):
				logging.debug( '{} has no binding for {}'.format( self.name, media_function ) )
				continue
			logging.debug( '{} supports {}'.format( self.name, media_function ) )
			event = binding[0]
			callback_function = binding[1]
			wxbutton.Bind( event, callback_function )
				
	def ExecuteMediaFunction( self, media_function ):
		if( not self.SupportsMediaFunction( media_function ) ):
			raise Exception( 'Media function "{}" is not supported'.format( media_function ) )
			
		print( 'Executing media function "{}"'.format( media_function ) )
		self._dev_media_functions[media_function][1]()
		
	def SupportsCapability( self, capability ):
		supported = True
		if( not self._dev_capability[ self.dev_type ].has_key( capability ) ):
			supported = False
		else:
			supported = self._dev_capability[ self.dev_type ][ capability ]
		#print( 'Capability "{}" in device {} is {} supported'.format( capability, str( self.dev_type ), ( '' if supported else 'not' ) ) )
		return supported
				
	def CurrentTrackHash( self ):
		if( self._current_track_hash ):
			return self._current_track_hash
			
		return None
		
	def _MergeDevMediaFunctions( self, source_media_functions ):
		dev_media_functions = {}
		for function, bindings in source_media_functions.iteritems():
			#import pprint ; pprint.pprint( bindings )
			#print( 'merging {}'.format( function ) )
			#media functions missing form the local support are ignored
			if( not self._dev_supports_media_function.has_key(function) ):
				#print( '\t{} missing from the device support'.format( function ) )
				continue
							
			#use MMediaGui offered media functions
			#print( '\tdevice supports {}'.format( str( self._dev_supports_media_function[function][0] ) ) )
			if( self._dev_supports_media_function[function][0] ):
				#print( '\tdevice supports {}'.format( function ) )
				if( self._dev_supports_media_function[function][1] is None ):
					#print( 'device supports {} but bindings is none so accepts mmedia bindings:{}'.format( function, bindings[1] ) )
					dev_media_functions[function] = [True, bindings[1]]
				else:
					dev_bindings = self._dev_supports_media_function[function][1]
					if( bindings[1] is not None ):
						dev_bindings + bindings[1]
					dev_media_functions[function] =	[True, dev_bindings]
					#print( 'device supports {} and along with its own {}, will also add mmedia bindings:{}'.format( function, dev_bindings[1], bindings[1] ) )
				#import pprint ; pprint.pprint( dev_media_functions[function] )
					
		return dev_media_functions

	#All concrete devices should override the following functions
	def _GetSettings( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceSettings
		'''
		return MediaDeviceSettings()

	def _GetState( self ):
		'''
		Concrete devices must override this function to return its own settings class which
		should inherit MediaDeviceState
		'''
		return MediaDeviceState()
		
	def Activate( self ):
		logging.debug( 'activating {}'.format( self.name ) )
		if( self._video_panel ):
			logging.debug( '\tshowing the video_panel' )
			self._video_panel.Show()
		else:
			logging.debug( '\tno video_panel to show' )
		
		self.state.Load()
		self.is_active = True
		
		if( self.SupportsCapability( 'system_playlist' ) ):
			self.UpdateSystemPlaylistsObservers()
			
	def Deactivate( self ):
		logging.debug( 'deactivating {}'.format( self.name ) )
		if( self._video_panel ):
			logging.debug( '\thiding the video_panel' )
			self._video_panel.Hide()
		else:
			logging.debug( '\tno video_panel to hide' )
			
		self.state.Save()
		self.is_active = False
				
	def _DevPlaylistFunctions( self ):
		'''
		Returns a dictionary. The keys are the playlist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'new': None, 'clear': None, 'save': None, 'add': None, 'edit': None,'delete': None, 'scan': None }

	def _DevFilelistFunctions( self ):
		'''
		Returns a dictionary. The keys are the filelist functions. The values are the callback of each function or
		None if the function is not supported. May also return an empty dictionary. Missing functions are not supported.
		Overriden by concrete devices.
		'''
		return { 'move_up_folder': None, 'play_all': None, 'play_selected': None, 'refresh': None }
	
	def GetMediaButtonsForGroup( self, media_button_group ):
		if( media_button_group == 0 ):
			return [
				'zap',
				'play',
				'rewind',
				'forward',
				'previous',
				'next',
				'step_back'
			]
		else:
			return [
				'step_forward',
				'speeddial_previous',
				'speeddial_next',
				'playlist_previous',
				'playlist_next',
				'subtitles',
				'shuffle',
				'repeat',
				'eject'
			]
				
	def _DevSupportsMediaFunction( self ):
		'''
		Concrete devices must override this function to return a dictionary with what they support.
		False means	media function is not supported. True and None means use the MMediaGui callback.
		True and a local function means the media function is supported by a local callback
		'''
		return {
			'zap':[ True, None ],
			'rewind':[ False, None ],
			'forward':[ False, None ],
			'previous':[ False, None ],
			'next':[ False, None ],
			'step_back':[ False, None ],
			'step_forward':[ False, None ],
			'speeddial_previous':[ True, None ],
			'speeddial_next':[ True, None ],
			'playlist_previous':[ True, None ],
			'playlist_next':[ True, None ],
			'subtitles':[ False, None ],
			'shuffle':[ False, None ],
			'repeat':[ False, None ],
			'eject': [ False, None ] 
		}
		
	def MediaButtonIsPressed( self, media_button_function_name ):
		'''
		This function is used to determine the state of the media button e.g.
		when the user selects a device, and the device is activated.
		For example, if a device should start with media_button "Repeat" 
		(i.e. loop a playlist) the device should return True
		'''
		return False
		
	def MediaButtonIsEnabled( self, media_button_function_name ):
		'''
		This function shoud be overriden by devices that should be asked if a particular
		media button should be displayed disabled or enabled. Such an example is the 
		'select subtitles' media button which should only be enabled while a media player
		(of a device that has one) is playing a video item
		'''
		return True
		
	def Play( self ):
		if( not self.is_active ):
			print( 'I {} am not active, cannot playtrack'.format( self.name ) )
			return
			
		#replaced by a callback called on mediaplyer's IsPlaying event
		#media_button = self._mmedia_gui.GetMediaButtonByFunctionName( 'play' )
		#media_button.is_pressed = True
		#self._mmedia_gui.RefreshMediaButton( media_button )
		
		self.UpdateTrackHashObservers()
		self._ShowMessage( self.GetCurrentTrackText() )
		
	def PlayTrack( self, track_hash ):
		if( not self.is_active ):
			print( 'I {} am not active, cannot playtrack'.format( self.name ) )
			return
			
		self._current_track_hash = track_hash
		self.Play()
		
		#print( 'playing track {}, callback:{}'.format( track_hash, self._playlist_select_callback ) )
		#if( self._playlist_select_callback ):
			#print( 'Calling {}'.format( self._playlist_select_callback.__name__ ) )
			#self._playlist_select_callback( track_hash )
			
	def GetCurrentTrackText( self ):
		pass
		
	def GetFilelistItems( self ):
		#print( 'Returning test filelist items' )
		return [
			MMediaListItem( 0, 'File item 0' ),
			MMediaListItem( 1, 'File item 1', False ),
			MMediaListItem( 2, 'File item 2' ),
			MMediaListItem( 3, 'File item 3 (playlist)', is_playlist=True ),
			MMediaListItem( 4, 'File item 4' ),
			MMediaListItem( 5, 'File item 5', False ),
			MMediaListItem( 6, 'File item 6', False ),
			MMediaListItem( 7, 'File item 7 (playlist)', is_playlist=True ),
			MMediaListItem( 8, 'File item 8' ),
			MMediaListItem( 9, 'File item 9' ),
			MMediaListItem( 10, 'File item 10 (playlist)', is_playlist=True ),
			MMediaListItem( 11, 'File item 11' ),
			MMediaListItem( 12, 'File item 12', False ),
			MMediaListItem( 13, 'File item 13' ),
			MMediaListItem( 14, 'File item 14', False ),
			MMediaListItem( 15, 'File item 15' ),
			MMediaListItem( 16, 'File item 16', False ),
			MMediaListItem( 17, 'File item 17' ),
			MMediaListItem( 18, 'File item 18' ),
			MMediaListItem( 19, 'File item 19' )
			]
			
		MediaDevice._RaiseNoConcreteImplementationException( 'GetFilelistItems' )
	
	def GetPlaylistItems( self ):
		#print( 'Returning test playlist items' )
		return [
			MMediaListItem( 0, 'Playlist item 0' ),
			MMediaListItem( 1, 'Playlist item 1' ),
			MMediaListItem( 2, 'Playlist item 2' ),
			MMediaListItem( 3, 'Playlist item 3' ),
			MMediaListItem( 4, 'Playlist item 4' ),
			MMediaListItem( 5, 'Playlist item 5' ),
			MMediaListItem( 6, 'Playlist item 6' ),
			MMediaListItem( 7, 'Playlist item 7' ),
			MMediaListItem( 8, 'Playlist item 8' ),
			MMediaListItem( 9, 'Playlist item 9' )
			#10: 'Playlist item 10',
			#11: 'Playlist item 11',
			#12: 'Playlist item 12',
			#13: 'Playlist item 13',
			#14: 'Playlist item 14',
			#15: 'Playlist item 15',
			#16: 'Playlist item 16',
			#17: 'Playlist item 17',
			#18: 'Playlist item 18',
			#19: 'Playlist item 19'
			]
			
		MediaDevice._RaiseNoConcreteImplementationException( 'GetPlaylistItems' )
		
	def TrackHashIsValid( self, track_hash ):
		'''This should be overriden only by fm_radio
		'''
		return True
			
	def GetMute( self ):
		return self.mute
		MediaDevice._RaiseNoConcreteImplementationException( 'GetMute' )

	def SetMute( self, on ):
		self.mute = on
		return
		
	def SetVolume( self, volume ):
		MediaDevice._RaiseNoConcreteImplementationException( 'SetVolume' )

	def GetVolume( self ):
		MediaDevice._RaiseNoConcreteImplementationException( 'GetVolume' )

	def GetSystemPlaylistsSaveDir( self ):
		device_sp_dir = self.Hash().replace( os.sep, '_' )
		full_path_dir = os.path.abspath( os.path.join( 'playlists', device_sp_dir ) )
		#logging.debug( 'GetSystemPlaylistsSaveDir: {}'.format( full_path_dir ) )
		return full_path_dir
		
	def GetSystemPlaylists( self ):
		return self.ReadDirectory( self.GetSystemPlaylistsSaveDir() )
		
	def GetSystemPlaylistActionCallbacks( self ):
		#import traceback; traceback.print_stack()
		return { 'delete' : self.DeleteSystemPlaylist }
		
	def SavePlaylist( self, event ):
		'''
		Will save the playlist items in m3u format
		'''
		dlg = SavePlaylistDialog( None, 'Save playlist' )
		if( dlg.ShowModal() == wx.ID_OK ):
			print( 'Will save {}'.format( dlg.GetPlaylistName() ) )
			
			#get the playlist dir for this device and create if not exists
			device_playlist_dir = self.GetSystemPlaylistsSaveDir()
			if( not os.path.exists( device_playlist_dir ) ):
				os.makedirs( device_playlist_dir )
				
			#Get the playlist filename and add .m3u extension if not exists
			filename = dlg.GetPlaylistName()			
			aux, dot_file_extension = os.path.splitext( filename )
			file_extension = dot_file_extension[1:]
			if( file_extension.lower() != 'm3u' ):
				filename = u'{}{}m3u'.format( filename, ( '.' if not filename.endswith( '.' ) else '' ) )
				
			#Check if the playlist already exists and ask to overwrite
			full_filename = os.path.join( device_playlist_dir, filename )
			save = True
			if( os.path.exists( full_filename ) ):
				print( 'playlist {} already exists'.format( filename ) )
				msg_dlg = wx.MessageDialog( dlg, u'Playlist {} already exists for this device. Ovewrite ?'.format( filename ), 
					u'Overwite {}'.format( filename ), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION )
				if( msg_dlg.ShowModal() != wx.ID_YES ):
					save = False
			if( save ):
				try:
					with open( full_filename, 'w' ) as f:
						for item in self.GetPlaylistItems():
							f.write( u'{}\n'.format( item.Hash().encode( 'utf-8') ) )
					self.UpdateSystemPlaylistsObservers()
				except:
					import sys; print('Error: %s' % sys.exc_info()[1])
					msg_dlg = wx.MessageDialog( dlg, 'An error occured while trying to save playlist {}.'.format( filename ), wx.OK | wx.ICON_ERROR )
		dlg.Destroy()

	def MediaIsValid( self, media_hash ):
		if( self.FileIsPlaylist( media_file ) ):
			return True
		return False	

	#End of functions to be overriden by concrete devices
	
	#Concrete may choose to override the following functions. MediaDevice supports 
	#default functionality for these functions

	def InitUI( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		self._video_panel_parent = video_panel_parent
		self._controls_panel_parent = control_panel_parent
			
	def MainFrameInitUIFinished( self ):
		'''
		For any device that requires to initialize stuff after the parent is Shown
		e.g. vlc based tv tunr
		'''
		pass
		
	def Hash( self ):
		return '{0}_{1}_{2}'.format( self.dev_type, self.name, self.dev_path )
		
	def NeedsMedia( self ):
		return MediaDevice._dev_needs_media[ self.dev_type ]
		
	def HasMedia( self ):
		return False
	
	def GetCurrentPlaylistHash( self ):
		'''
		Devices may choose to override this to indicate that the playlist that is currently loaded has a hash
		and therefore is retrievable.
		This function is initially used to indicate to the speeddial popup creator that a playlist is loaded
		and its hash can be stored in a speeddial button.
		Filesystem devices should override this
		'''
		return self._current_playlist_hash
		
	def GetCurrentPlaylistName( self ):
		cph = self.GetCurrentPlaylistHash()
		return ( '' if cph is None else os.path.basename( cph ) )
		
	def GetCurrentDirectoryHash( self ):
		'''
		Filesystem devices must override this to indicate that the directory currently loaded has a hash
		and therefore is retrievable.
		This function is initially used to indicate to the speeddial popup creator that a directory is loaded
		and its hash can be stored in a speeddial button.
		'''
		raise Exception( 'GetCurrentDirectoryHash should not be called because I am not a filesystem device' )
			
	def SupportsStereoMono( self ):
		return False
		
	def IsStereo( self, is_stereo = None ):
		'''
		Ugly overloading, if is_stereo is None then return self._is_stereo, else set _is_stereo and UpdateStereoMonoObservers
		'''
		if( is_stereo ):
			self._is_stereo = is_stereo
			self.UpdateStereoMonoObservers()
	
		return is_stereo
			
	def SupportsSignalStrength( self ):
		return False
		
	def SignalStrengthIs( self ):
		return -1
		
	def AddSignalStrengthObserver( self, observer ):
		self.signalStrengthObservers.append( observer )
	
	def DelSignalStrengthObserver( self, observer ):
		self.signalStrengthObservers.remove( observer )
		
	def UpdateSignalStrengthObservers( self ):
		for i in self.signalStrengthObservers:
			i.SignalStrengthIs( self.signalStrength )

	def AddStereoMonoObserver( self, observer ):
		self.stereoMonoObservers.append( observer )
		
	def DelStereoMonoObserver( self, observer ):
		self.stereoMonoObservers.remove( observer )
		
	def UpdateStereoMonoObservers( self ):
		#print( 'media_device will update {} stereoMonoObservers with is_stereo: {}'.format( len( self.stereoMonoObservers ), self._is_stereo ) )
		for i in self.stereoMonoObservers:
			#print( 'media_device updating stereoMonoObserver: {} with is_stereo: {}'.format( i, self._is_stereo ) )
			i.IsStereo( self._is_stereo )
			
	def AddTrackHashObserver( self, observer ):
		self.trackHashObservers.append( observer )
		
	def DelTrackHashObserver( self, observer ):
		self.trackHashObservers.remove( observer )
		
	def UpdateTrackHashObservers( self ):
		for i in self.trackHashObservers:
			i.CurrentTrackHashIs( self._current_track_hash )
			
	def AddFilelistObserver( self, observer ):
		self.filelistObservers.append( observer )
		
	def DelFilelistObserver( self, observer ):
		self.filelistObservers.remove( observer )
		
	def UpdateFilelistObservers( self ):
		filelistItems = self.GetFilelistItems()
		for i in self.filelistObservers:
			i.SetItems( filelistItems )
			
	def AddPlaylistObserver( self, observer ):
		self.playlistObservers.append( observer )
		
	def DelPlaylistObserver( self, observer ):
		self.playlistObservers.remove( observer )
		
	def UpdatePlaylistObservers( self ):
		listItems = self.GetPlaylistItems()
		for i in self.playlistObservers:
			i.SetItems( listItems )
			
	def AddSystemPlaylistsObserver( self, observer ):
		self.systemplaylistsObservers.append( observer )
		
	def DelSystemPlaylistsObserver( self, observer ):
		self.systemplaylistsObservers.remove( observer )
		
	def UpdateSystemPlaylistsObservers( self ):
		listItems = self.GetSystemPlaylists()
		for i in self.systemplaylistsObservers:
			i.SetItems( listItems )
			
	def Stop( self ):
		media_button = self._mmedia_gui.GetMediaButtonByFunctionName( 'play' )
		media_button.is_pressed = False
		self._mmedia_gui.RefreshMediaButton( media_button )
		self._ShowMessage( '' )
		self._mmedia_gui.ResetSpeedDials()

	def GetSubtitlesDialog( self ):
		return None
		
	def GetCurrentSubtitle( self ):
		return ''
		
	def SetSubtitle( self, show_subtitles, subtitle_object ):
		return
		
	def SubtitlesAreAvailable( self ):
		'''
		This function is used to let the gui know of the "select subtitles" button should be available.
		The subtitles are available based on the fact that the media_player is currently playing a video item
		(file, dvd, upnp video item, etc.)
		The whole process of enabling/disabling the "select subtitles" button (and others) is triggered by 
		callback functions handling the IsPlaying, IsPaused events of a devices media player (for those devices
		that have a media player)
		'''
		return False
		
	#End of functions that may be overriden

	def ReadDirectory( self, directory ):
		file_items = []
		if( not directory.endswith( '/' ) ):
			directory += '/'
			
		if( not os.path.exists( directory ) ):
			return file_items
			
		#items = os.listdir( os.path.normpath( directory ) )
		#print( 'will glob directory {}'.format( directory ) )
		items = os.listdir( os.path.abspath( directory ) ) #
		#items = glob.glob( os.path.abspath( directory ) + '/*' )
		#import pprint; pprint.pprint( items )
		dirs = [ i for i in items if os.path.isdir( os.path.abspath( os.path.join( directory, i ) ) ) ]
		#import pprint; pprint.pprint( dirs )
		files = [ i for i in items if os.path.isfile( os.path.abspath( os.path.join( directory, i ) ) ) ]
		#import pprint; pprint.pprint( files )
		for d in sorted( dirs ):
			file_items.append( FileItem( os.path.abspath( os.path.join( directory, d ) ), FileItem.FOLDER_TYPE ) )
		for f in sorted( files ):
			#print( 'adding file {} to the list of files'.format( f ) )
			full_file_path = os.path.abspath( os.path.join( directory, f ) )
			file_items.append( 
				FileItem( 
					full_file_path, 
					FileItem.FILE_TYPE, 
					is_enabled = self.MediaIsValid( full_file_path ),
					is_playlist = self.FileIsPlaylist( full_file_path )
					) 
				)
		return file_items
		
	def FileIsPlaylist( self, filename ):
		'''
		For now the only test is done on the file extension expected to be m3u
		'''
		fileName, dot_file_extension = os.path.splitext( filename )
		file_extension = dot_file_extension[1:]
		is_playlist = ( file_extension.lower() == 'm3u' )
		return is_playlist
		
	def ReadM3UPlaylist( self, filename ):
		'''
		Returns a list of the playlist items or raises an exception if this is not a valid m3u playlist
		'''
		encoding = lambda x: detect(x)['encoding']
		
		items = []
		try:
			#items = [ unicode( line.strip(),encoding(line),errors='ignore') for line in file(filename) if not line.startswith('#') ]
			with open( filename , mode = 'r' ) as f:
				for line in f:
					if( line.startswith('#') or len( line.strip() ) == 0 ):
						continue					
					print encoding(line)
					items.append( line.strip() )
					#items.append( unicode(line,encoding(line),errors='ignore') )				
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
			print( 'invalid file {}'.format( filename ) )
		#print( 'ReadM3UPlaylist returns {}'.format( items ) )
		return items

	def DeleteSystemPlaylist( self, event ):
		#print( 'DeleteSystemPlaylist: self._GetSelectedSystemPlaylistItemsCallback is {}'.format( self._GetSelectedSystemPlaylistItemsCallback ) )
		if( self._GetSelectedSystemPlaylistItemsCallback ):
			items = self._GetSelectedSystemPlaylistItemsCallback()
			for item in items:
				print( 'will delete {}'.format( item ) )
				os.remove( item.Hash() )
				
			self.UpdateSystemPlaylistsObservers()

	@staticmethod
	def StrToType( str ):
		return MediaDevice._dev_str_to_types[str]
