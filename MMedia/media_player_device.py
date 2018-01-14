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
from media_player import MediaPlayer
from device_behavior_on_activate import *


class MediaPlayerDevice( MediaDevice ):
	
	def __init__( self, abstract_device, SetPlaylistLabelTextCallback = None, GetSelectedPlaylistItemsCallback = None ):
		MediaDevice.__init__( self, abstract_device.name, abstract_device.dev_path, abstract_device.dev_type, abstract_device._mmedia_gui, abstract_device._gui_media_functions, abstract_device._playerLock, abstract_device._error_reporter, abstract_device._message_reporter, GetSelectedSystemPlaylistItemsCallback = abstract_device._GetSelectedSystemPlaylistItemsCallback )
		self.media_player = None
		self._SetPlaylistLabelTextCallback = SetPlaylistLabelTextCallback
		self._GetSelectedPlaylistItemsCallback = GetSelectedPlaylistItemsCallback
		self.playlist_items = []
	
	#All concrete devices should override the following functions
	def _GetDeviceBehaviorOnActivate( self ):
		MediaDevice._RaiseNoConcreteImplementationException( '_GetDeviceBehaviorOnActivate' )

	def IsPlaying( self ):
		'''
		Devices that use media_players should override this function and return True if the media_player is playing
		'''
		if( not self.media_player ):
			return False
			
		return self.media_player.IsPlaying()
	
	def GetMute( self ):
		return self.media_player.GetMute()

	def SetMute( self, on ):
		self.media_player.SetMute( on )
		MediaDevice.SetMute( self, on )
	
	def SetVolume( self, volume ):
		preamp = self.state.GetPreamp()
		final_volume = volume*( 1 + preamp / 100.0 )
		logging.debug( 'MediaPlayerDevice.SetVolume: preamp={}, volume={}, final_volume={}'.format( preamp, volume, final_volume ) )
		self.media_player.SetVolume( final_volume )

	def GetVolume( self ):
		volume = self.media_player.GetVolume()
		preamp = self.state.GetPreamp()
		device_volume = volume/( 1 + preamp / 100.0 )
		logging.debug( 'MediaPlayerDevice.GetVolume: preamp={}, volume={}, device_volume={}'.format( preamp, volume, device_volume ) )
		return device_volume

	def SetBrightness( self, brightness ):
		self.media_player.SetBrightness( brightness )
		MediaDevice.SetBrightness( self, brightness )

	def SetContrast( self, contrast ):
		self.media_player.SetContrast( contrast )
		MediaDevice.SetContrast( self, contrast )
	
	def SetGamma( self, gamma ):
		self.media_player.SetGamma( gamma )
		MediaDevice.SetGamma( self, gamma )
	
	def SetHue( self, hue ):
		self.media_player.SetHue( hue )
		MediaDevice.SetHue( self, hue )
	
	def SetSaturation( self, saturation ):
		self.media_player.SetSaturation( saturation )
		MediaDevice.SetSaturation( self, saturation )
		
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
		self.media_player = self._CreateMediaPlayer( video_panel_parent, self._playerLock, video_panel_click_callback )
		self.media_player.AddEndOfTrackObserver( self )
		self.media_player.AddPosChangeObserver( self )
		self.media_player.AddPlayingObserver( self )
		self.media_player.AddPausedObserver( self )
		self.media_player.AddErrorObserver( self )
		self._video_panel = self.media_player.video_panel
		#self._controls_panel = self.media_player.ctrlpanel
		self._video_panel_parent.GetSizer().Add( self._video_panel, 1, wx.EXPAND )
	
	def MainFrameInitUIFinished( self ):
		if( self.HasVideoSettings() ):
			self.media_player.SetBrightness( self.state.GetBrightness() )
			self.media_player.SetContrast( self.state.GetContrast() )
			self.media_player.SetGamma( self.state.GetGamma() )
			#self.media_player.SetHue( self.state.GetHue() )
			#self.media_player.SetSaturation( self.state.GetSaturation() )
			
	def Stop( self ):
		self.media_player.Stop()
		MediaDevice.Stop( self )
	
	#End of functions that may be overriden
	
	def OnMediaPlayerError( self, error_event ):
		self._ReportError( error_event )
	
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
		#the following line is required so that the device will not start playing if it is deactivated and reactivated
		self._behavior_on_activate.SetUserStop()
		wx.CallAfter( self._mmedia_gui.GU_IsPaused )
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
		wx.CallAfter( self._mmedia_gui.SetPlayProgressDuration, '{:02d}:{:02d}:{:02d}'.format( hours, minutes, seconds ) )
		
		time_delta = datetime.timedelta( milliseconds = player_time )
		s = time_delta.seconds
		hours, remainder = divmod(s, 3600)
		minutes, seconds = divmod(remainder, 60)		
		position = round( player_position * 100, 0 )
		wx.CallAfter( self._mmedia_gui.SetPlayProgressPosition, position, '{:02d}:{:02d}:{:02d}'.format( hours, minutes, seconds ) )
	
	def OnShuffle( self, event ):
		button = event.GetEventObject()
		media_button = self._mmedia_gui.GetMediaButtonByFunctionName( button.function_name )
		print( 'MediaPlayerDevice.OnShuffle function: {}, media_button: {}, is_pressed: {}'.format( button.function_name, media_button, media_button.is_pressed ) )
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
		#media_button = wx.CallAfter( self._mmedia_gui.GetMediaButtonByFunctionName, button.function_name )
		#if( media_button.is_pressed ):
		media_button_is_pressed = self._mmedia_gui.GU_GetMediaButtonIsPressed( button.function_name )
		if( media_button_is_pressed ):
			if( self._current_track_hash is not None and len( self._current_track_hash ) > 0 ):
				self.Play()
			else:
				raise Exception( 'Fix me' )
				wx.CallAfter( self._mmedia_gui.RefreshMediaButton, media_button )
		else:
			self.Pause() #self.Stop()
		event.Skip()
	
	def Pause( self ):
		MediaDevice.Pause( self )
		self.media_player.Pause()

	def ClearPlaylist( self, event = None ):
		self.playlist_items = []
		self._current_track_hash = None
		self._current_playlist_hash = None
		self.Stop()
		self.UpdatePlaylistObservers()
	
	def NewPlaylist( self, event ):
		if( self._SetPlaylistLabelTextCallback ):
			wx.CallAfter( self._SetPlaylistLabelTextCallback, 'New' )
		self._current_playlist_hash = None
		self.ClearPlaylist()
	
	def RemovePlaylistItem( self, event ):
		if( self._GetSelectedPlaylistItemsCallback ):
			items = self._GetSelectedPlaylistItemsCallback()
			self.playlist_items = [ i for i in self.playlist_items if i not in items ]
			self.UpdatePlaylistObservers()
	
	def _CreateMediaPlayer( self, video_panel_parent, control_panel_parent, video_panel_click_callback ):
		'''
		Override if a simple MediaPlayer is not enough
		'''
		return MediaPlayer( playerLock = self._playerLock, video_parent_panel = video_panel_parent, videoPanelClickCallback = video_panel_click_callback )
	
	def GetMediaStringForPlayer( self, item_str ):
		'''
		Override if item_str should be processed first
		For almost any filesystem derived device this is just the item_str
		But for the UPnP MediaServer device this is the mediaservers hostname concat with the object's id
		There is a bug here. Some object id's come prefixed with '/'. If this is concatenated to
		http://hostname/ there will be two '/' after the hostname and this is a "not exists" error
		'''
		return item_str
		
	def MediaPlayerIsPlaying( self ):
		wx.CallAfter( self._mmedia_gui.GU_IsPlaying )
	
	def MediaPlayerPaused( self ):
		wx.CallAfter( self._mmedia_gui.GU_IsPaused )

class MediaPlayerDeviceState( MediaDeviceState ):
	def __init__( self ):
		self.shuffle = False
		self.repeat = False
		MediaDeviceState.__init__( self )
	
	def SetShuffle( self, shuffle ):
		self.shuffle = shuffle
		self.Save()

	def SetRepeat( self, repeat ):
		self.repeat = repeat 
		self.Save()
