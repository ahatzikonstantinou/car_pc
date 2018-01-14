#! /usr/bin/python
# -*- coding: utf-8 -*-

import wx # 2.8
import os
import string
import datetime
import imghdr	#used for a bug in determining valid media files, images should not be included
import uuid
from wx.lib.pubsub import Publisher
import logging
logging.basicConfig( level = logging.DEBUG )

import vlc
from gstreamer_players.discoverer import Discoverer
import time #for testing discoverer's discover time

from threading import *

import gobject
gobject.threads_init()

class MediaPlayer:
	''' 
	This media player is based on libvlc. Also it uses the discoverer module which uses the 
	gstreamer libraries to discover if a file contains video or not and create a vlc player
	with or without audio visualisation accordingly
	'''
	SetStep = 10
	SetMin = 0
	SetMax = 200

	def __init__( self, playerLock, video_parent_panel = None, videoPanelClickCallback = None ):
		self.Instance = None
		self.player = None
		self.event_manager = None
		self.discovery_start_time = 0
		self.ready_to_play = False
		self.asked_to_start = False
		self.current_media_str = None
		self.current_media_options = None
		self._volume = 10
		self._mute = False
		self._brightness = 1.0
		self._contrast = 1.0
		self._gamma = 1.0
		self._hue = 0
		self._saturation = 1.0
		
		if( video_parent_panel ):
			self.video_panel = wx.Panel( video_parent_panel )
			video_parent_panel.GetSizer().Add( self.video_panel )
			self.video_panel.SetBackgroundColour(wx.BLACK)
			#self.video_panel.SetBackgroundColour( 'blue' )
			
			self.videoPanelClickCallback = videoPanelClickCallback
			if( self.videoPanelClickCallback is not None ):
				print( 'binding videopanel with {}'.format( self.videoPanelClickCallback ) )
				#self.video_panel.Bind( wx.EVT_LEFT_UP, self.videoPanelClickCallback )
				self.video_panel.Bind( wx.EVT_LEFT_DCLICK, self.videoPanelClickCallback )
				#self.video_panel.Bind( wx.EVT_LEFT_DCLICK, self.VideopanelClicked )
		
		self.playerLock = playerLock
		
		self._uuid = uuid.uuid4()
		self._error_observers = []
		self._stereo_mono_observers = []
		self._EndOfTrack_observers = []
		self._PosChangeObservers = []
		self._playing_observers = []
		self._paused_observers = []
		self._END_OF_TRACK_MESSAGE_NAME = 'end_of_track_{}'.format( self._uuid )	#unique per media_player
		#print( '_END_OF_TRACK_MESSAGE_NAME: {}'.format( self._END_OF_TRACK_MESSAGE_NAME ) )
		self._POS_CHANGE_MESSAGE_NAME = 'pos_change_{}'.format( self._uuid )	#unique per media_player
		Publisher().subscribe( self._UpdateEndOfTrackObservers, self._END_OF_TRACK_MESSAGE_NAME )
		Publisher().subscribe( self._UpdatePosChangeObservers, self._POS_CHANGE_MESSAGE_NAME )
				
	def _OnDiscovered( self, discoverer, success ):
		# print( 'arg:{}, success:{}'.format( arg.__class__.__name__, success ) )
		print( '_OnDiscovered called with success: '.format( success ) )
		# import pprint; pprint.pprint( discoverer )
		#import datetime
		#elapsed_time = str(datetime.timedelta( seconds = ( time.time() - self.discovery_start_time ) ) )
		#print( 'Discoverer finished in {} time?'.format( elapsed_time ) )
		#discoverer.print_info()
		self.ready_to_play = True
		self.media_has_video = discoverer.is_video
		if( self.asked_to_start ):
			self.DoPlay( discoverer.is_video )

	def Start( self ):
		#Make sure that before Start is called you show the main application window so that 
		#the window is rendered, so that it gets a handle from the operating system in order 
		#to pass it on to the player, to display its content
		#self.Show()
		with self.playerLock :
			# set the window id where to render VLC's video output
			self.player.set_xwindow(self.video_panel.GetHandle())
			#pass
			#print( 'got xwindow {}'.format( self.video_panel.GetHandle() ) )
			#self.player.video_set_scale( 0.0 )
			#self.player.video_set_crop_geometry( None )

	def Stop( self ):
		with self.playerLock :
			if( self.player and self.player.is_playing() == 1 ):
				self.player.stop()
				for i in self._PosChangeObservers:
					i.OnPosChange( (0,0,0 ) )
	
	def Pause( self ):
		with self.playerLock :
			if( self.player and self.player.is_playing() == 1 ):
				self.player.pause()
				
	def Play( self, media_str, options = None ):
		with self.playerLock :
			cms = ( self.current_media_str.encode( 'utf-8' ) if self.current_media_str else '' )
			logging.debug( 'media_player was asked to play {}, self.current_media_str: {}'.format( media_str.encode( 'utf-8' ), cms ) )
			#if( media_str != self.current_media_str ):
				#self.current_media_str = media_str
				#self.current_media_options = options
				#discoverer = Discoverer( os.path.abspath( media_str ) )
				#discoverer.connect( 'discovered', self._OnDiscovered )
				#self.discovery_start_time = time.time()
				#replaced because it was inaccurate discoverer.discover()
				#self.asked_to_start = True
				#self.ready_to_play = False #will be ready when discoverer has finished
			#else:
			#IDLE/CLOSE=0, OPENING=1, BUFFERING=2, PLAYING=3, PAUSED=4, STOPPING=5, ENDED=6, ERROR=7
			#print( 'player.get_state(): {}'.format( self.player.get_state() ) )
			if( self.player and self.player.get_state() == vlc.State.Paused and 
				media_str == self.current_media_str and options == self.current_media_options ):
				#print( 'player is paused, will continue' )
				self.player.play()
			else:
				self.current_media_str = media_str
				self.current_media_options = options
				self.DoPlay()

	def DoPlay( self ):
		self.Stop()
		with self.playerLock :
			if( self.player ):
				self.player.release()
				#del self.player
			if( self.Instance ):
				self.Instance.release()
				#del self.Instance
			
			self.Instance = self.CreateInstance( self.MediaIsVideo( self.current_media_str ) )
			#flat, classical, club, dance, fullbass, fullbasstreble, fulltreble, headphones, largehall, live, party, pop, reggae, rock, ska, soft, softrock, techno
			# import pprint ; pprint.pprint( self.Instance.audio_filter_list_get() )
			# import pprint ; pprint.pprint( self.Instance.video_filter_list_get() )
			self.player = self.Instance.media_player_new()
			self.Start()
			m = self.Instance.media_new( self.current_media_str )
			if( self.current_media_options ):
				m.add_options( self.current_media_options )
			self.player.set_media( m )
			m.release()
			#self.player.video_set_mouse_input( False )
			#self.player.audio_set_volume( self._volume )
			#logging.debug( 'MediaPlayer.DoPlay: right before starting to play, setting volume to {}'.format( self._volume ) )
			if( self.player.play() == -1 ):
				print( 'Cannot play "{0}"'.format( self.current_media_str.encode( 'utf-8' ) ) )
			else:
				'''
				For some unknown reason, in order to set the volume of the vlc player right, I MUST do it some amount of time AFTER it starts playing e.g. 100 milliseconds or else no matter how I set the volume (in the Instance constructor or explicitly via self.player.audio_set_volume) the volume returned by self.player.audio_get_volume is the one I set, but the vlc application in ubuntu's settings clearly shows (and that is exactly how it sounds) that the vlc instance is playing at the volume level of the PREVIOUS vlc instance running in the previously active device. Same thing for Enabling video adjustments. WEIRD.
				'''				
				time.sleep( 0.1 )
				self.SetVolume( self._volume/10.0 )
				self.AdjustImageSettings()
				#self.player.audio_set_volume( self._volume )
				#logging.debug( 'MediaPlayer.DoPlay: right after starting to play, setting volume to {}'.format( self._volume ) )
				#logging.debug( 'MediaPlayer.DoPlay: started playing with volume {}'.format( self.player.audio_get_volume() ) )
				logging.debug( '\tplaying {}:{}'.format( self.current_media_str.encode( 'utf-8' ), self.current_media_options ) )
				#print('Subtitle count: {}'.format( self.player.video_get_spu_count() ) )
				#print( 'track description: {}'.format( self.player.audio_get_track_description() ) )
				#event_manager = self.Instance.vlm_get_event_manager()	#this returns an event manager that does not recognize MediaPlayerEndReached and MediaPlayerPositionChanged
				self._AttachEvents()
				self.PrintInfo()
				
	def _AttachEvents( self ):
		if( self.player ):
			self.event_manager = self.player.event_manager()
			self.event_manager.event_attach( vlc.EventType.MediaPlayerEndReached, self._OnEndOfTrack )
			self.event_manager.event_attach( vlc.EventType.MediaPlayerPositionChanged, self._OnPosChange )
			self.event_manager.event_attach( vlc.EventType.MediaPlayerPlaying, self._OnPlaying )
			self.event_manager.event_attach( vlc.EventType.MediaPlayerPaused, self._OnPaused )
			self.event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._OnErrorEvent )

	@vlc.callbackmethod
	def AddErrorObserver( self, observer ):
		self._error_observers.append( observer )
		
	def _UpdateErrorObservers( self, error_event ):
		for i in self._error_observers:
			wx.CallAfter( i.OnMediaPlayerError, error_event )
			
	def _OnErrorEvent( self, event ):
		logging.error( 'Mediaplayer caught an error event:' )
		self._UpdateErrorObservers( event )
		
	def AddStereoMonoObserver( self, observer ):
		self._stereo_mono_observers.append( observer )
		
	def UpdateStereoMonoObservers( self, is_stereo ):
		#print( 'media_player will UpdateStereoMonoObservers with: {}'.format( is_stereo ) )
		for i in self._stereo_mono_observers:
			#print( 'media_player updating stereoMonoObserver: {} with is_stereo: {}'.format( i, is_stereo ) )
			wx.CallAfter( i.IsStereo, is_stereo )
			
	def AddEndOfTrackObserver( self, observer ):
		#import pprint; pprint.pprint( self.playerLock )
		if self.playerLock.acquire( True ) :
			try:
				self._EndOfTrack_observers.append( observer )
			finally:
				self.playerLock.release()

	@vlc.callbackmethod
	def _OnEndOfTrack( self, event ):
		with self.playerLock :
			#We use wx.CallAfter because _OnEndOfTrack has been called from a forked thread and cannot update wx.Widgets
			#whcih is what is eventually done when calling _EndOfTrack_observers.OnEndOfTrack
			#print( 'Track ended. Will publish message {}'.format( self._END_OF_TRACK_MESSAGE_NAME ) )
			wx.CallAfter( Publisher().sendMessage, self._END_OF_TRACK_MESSAGE_NAME )

	def _UpdateEndOfTrackObservers( self, msg ):
		'''
		Note: the msg argument is required. This is the signature of callback functions for Publisher().subscribe
		The msg argument contains a property called data which conveys any actual message passed by the function that
		generated the message i.e. wx.CallAfter which in _OnEndOfTrack does not pass any messages
		'''
		with self.playerLock :
			#print( 'received published message {}. updating _EndOfTrack_observers...'.format( self._END_OF_TRACK_MESSAGE_NAME ) )
			for i in self._EndOfTrack_observers:
				wx.CallAfter( i.OnEndOfTrack )
	
	def AddPosChangeObserver( self, observer ):
		with self.playerLock :
			self._PosChangeObservers.append( observer )
		
	@vlc.callbackmethod
	def _OnPosChange( self, event ):
		with self.playerLock :
			#print( 'position of track changed to event: {}, player: {}, time: {}'.format( str( event.u.new_position ), str( self.player.get_position() ), datetime.timedelta( milliseconds = self.player.get_time() ) ) )
			#print( 'Pos changed. Will publish message {} with data: {}'.format( self._POS_CHANGE_MESSAGE_NAME, str( self.player.get_time() ) ) )
			name = self._POS_CHANGE_MESSAGE_NAME
			time = self.player.get_time()
			duration = self.player.get_media().get_duration()
			position = self.player.get_position()
			wx.CallAfter( Publisher().sendMessage, name, ( time, duration, position ) )

	def _UpdatePosChangeObservers( self, msg ):
		'''
		Note: the msg argument is required. This is the signature of callback functions for Publisher().subscribe
		The msg argument contains a property called data which conveys any actual message passed by the function that
		generated the message
		'''
		with self.playerLock :
			#print( 'received published message {}. updating _PosChangeObservers...'.format( self._POS_CHANGE_MESSAGE_NAME ) )
			audio_channel = self.player.audio_get_channel()
			#print( 'audio_channel: {}'.format( audio_channel ) ) #; import pprint; pprint.pprint( audio_channel )
			#print( 'vlc.AudioOutputChannel.Stereo: {}'.format( vlc.AudioOutputChannel.Stereo ) )
			self.UpdateStereoMonoObservers( vlc.AudioOutputChannel( audio_channel ) == vlc.AudioOutputChannel.Stereo )
			for i in self._PosChangeObservers:
				wx.CallAfter( i.OnPosChange, msg.data )
			
	def AddPlayingObserver( self, observer ):
		self._playing_observers.append( observer )
		
	def UpdatePlayingObservers( self ):
		for o in self._playing_observers:
			wx.CallAfter( o.MediaPlayerIsPlaying )
			
	@vlc.callbackmethod
	def _OnPlaying( self, event ):
		'''
		For some unknown reason, in order to set the volume of the vlc player right, I MUST do it some amount of time AFTER it starts playing e.g. 100 milliseconds or else no matter how I set the volume (in the Instance constructor or explicitly via self.player.audio_set_volume) the volume returned by self.player.audio_get_volume is the one I set, but the vlc application in ubuntu's settings clearly shows (and that is exactly how it sounds) that the vlc instance is playing at the volume level of the PREVIOUS vlc instance running in the previously active device. WEIRD.
		'''
		#wx.CallLater( 100, self.SetVolume, self._volume/10.0 )
		with self.playerLock :
			logging.debug( 'Media player event "Playing"' )
			#logging.debug( 'MediaPlayer._OnPlaying: started playing with volume {}'.format( self.player.audio_get_volume() ) )
			#res = self.player.audio_set_volume( self._volume )
			#logging.debug( 'MediaPlayer._OnPlaying: now that the player is playing volume was set to {} ({})'.format( self.player.audio_get_volume(), ( 'successfully' if res == 0 else 'error: out of range' ) ) )
			self.UpdatePlayingObservers()
		
	def AddPausedObserver( self, observer ):
		self._paused_observers.append( observer )
		
	def UpdatePausedObservers( self ):
		for o in self._paused_observers:
			wx.CallAfter( o.MediaPlayerPaused )
			
	@vlc.callbackmethod
	def _OnPaused( self, event ):
		logging.debug( 'Media player event "Paused"' )
		self.UpdatePausedObservers()
		
	def IsPlaying( self ):
		with self.playerLock :
			if( self.player is None ):
				return False
				
			return self.player.is_playing() == 1
		
	def Dump( self ):
		with self.playerLock :
			scale = self.player.video_get_scale()
			print( 'scale:{}'.format( scale ) )
			ar = self.player.video_get_aspect_ratio()
			print( 'aspect ratio:{}'.format( ar ) )
			self.videoWidth = self.player.video_get_width()
			print( 'width:{}'.format( self.videoWidth ) )
			self.videoHeight = self.player.video_get_height()
			print( 'height:{}'.format( self.videoHeight ) )

	def SetBrightness( self, brightness = None ):
		'''<float> : set the image brightness, between 0 and 2. Defaults to 1'''
		with self.playerLock :
			if( brightness ):
				self._brightness = brightness
			logging.debug( 'MediaPlayer.SetBrightness to {}'.format( self._brightness ) )
			if self.player and self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, self._brightness ) == -1:
				self.errorDialog("Failed to set brightness")

	def SetContrast( self, contrast = None ):
		'''<float> : set the image contrast, between 0 and 2. Defaults to 1'''
		with self.playerLock :
			if( contrast ):
				self._contrast = contrast
			logging.debug( 'MediaPlayer.SetContrast to {}'.format( self._contrast ) )
			if self.player and self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, self._contrast ) == -1:
				self.errorDialog("Failed to set contrast")

	def SetGamma( self, gamma = None ):
		'''<float> : set the image gamma, between 0.01 and 10.0. Defaults to 1.0'''
		with self.playerLock :
			if( gamma ):
				self._gamma = gamma
			logging.debug( 'MediaPlayer.SetGamma to {}'.format( self._gamma ) )
			if self.player and self.player.video_set_adjust_float( vlc.VideoAdjustOption.Gamma, self._gamma ) == -1:
				self.errorDialog("Failed to set gamma")

	def SetHue( self, hue = None ):
		'''<integer> : Set the image hue, between 0 and 360. Defaults to 0'''
		with self.playerLock :
			if( hue ):
				self._hue = hue
			logging.debug( 'MediaPlayer.SetHue to {}'.format( self._hue ) )
			if self.player and self.player.video_set_adjust_float( vlc.VideoAdjustOption.Hue, self._hue ) == -1:
				self.errorDialog("Failed to set hue")
	
	def SetSaturation( self, saturation = None ):
		'''<float> : Set the image saturation, between 0 and 3. Defaults to 1'''
		with self.playerLock :
			if( saturation ):
				self._saturation = saturation
			logging.debug( 'MediaPlayer.SetSaturation to {}'.format( self._saturation ) )
			if self.player and self.player.video_set_adjust_float( vlc.VideoAdjustOption.Saturation, self._saturation ) == -1:
				self.errorDialog("Failed to set saturation")

	def AdjustImageSettings( self ):
		with self.playerLock :
			self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			#self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, self.State.brightness/50.0 )
			#self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, self.State.contrast/50.0 )
			#vlc.VideoAdjustOption.Gamma, vlc.VideoAdjustOption.Hue, VideoAdjustOption.Saturation
			self.SetBrightness()
			self.SetContrast()
			self.SetGamma()
			#self.SetHue()
			#self.SetSaturation()
		
	#functions that are not used anymore
	
	def IncreaseBrightness( self, event ):
		with self.playerLock :
			brightness = self.brightnessSlider.GetValue() * 2
			if( brightness >= VLCControl.SetMax ):
				print( 'brightness:{} >= VLCControl.SetMax:{}'.format( brightness, VLCControl.SetMax ) )
				return
			brightness += VLCControl.SetStep
			self.brightnessSlider.SetValue( brightness/2 )
			self.OnSetBrightness()
			return

	def DecreaseBrightness( self, event ):
		with self.playerLock :
			brightness = self.brightnessSlider.GetValue() * 2
			if( brightness <= VLCControl.SetMin ):
				print( 'brightness:{} <= VLCControl.SetMax:{}'.format( brightness, VLCControl.SetMax ) )
				return
			brightness -= VLCControl.SetStep
			self.brightnessSlider.SetValue( brightness/2 )
			self.OnSetBrightness()
			return

	def IncreaseContrast( self, event ):
		with self.playerLock :
			contrast = self.contrastSlider.GetValue() * 2
			if( contrast >= VLCControl.SetMax ):
				print( 'contrast:{} >= VLCControl.SetMax:{}'.format( contrast, VLCControl.SetMax ) )
				return
			contrast += VLCControl.SetStep
			self.contrastSlider.SetValue( contrast/2 )
			self.OnSetContrast()
			return

	def DecreaseContrast( self, event ):
		with self.playerLock :
			contrast = self.contrastSlider.GetValue() * 2
			if( contrast <= VLCControl.SetMin ):
				print( 'contrast:{} <= VLCControl.SetMax:{}'.format( contrast, VLCControl.SetMax ) )
				return
			contrast -= VLCControl.SetStep
			self.contrastSlider.SetValue( contrast/2 )
			self.OnSetContrast()
			return

	def OnSetBrightness(self, evt=None):
		"""Set the brightness according to the brightness slider.
		"""
		with self.playerLock :
			#self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			brightness = self.brightnessSlider.GetValue() * 2
			print( 'new brightness: {}'.format( brightness ) )
			if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, brightness/100.0 ) == -1:
				self.errorDialog("Failed to set brightness")
			else:
				self.State.brightness = brightness/2
				self.SaveState()

	def OnSetContrast(self, evt=None):
		"""Set the contrast according to the contrast slider.
		"""
		with self.playerLock :
			#self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			contrast = self.contrastSlider.GetValue() * 2
			print( 'new contrast: {}'.format( contrast ) )
			if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, contrast/100.0 ) == -1:
				self.errorDialog("Failed to set contrast")
			else:
				self.State.contrast = contrast/2
				self.SaveState()

	def VideopanelClicked( self, event ):
		if( self.videoPanelClickCallback is not None ):
			self.videoPanelClickCallback()
			self.video_panel.SetBackgroundColour( 'yellow' )
			logging.debug( 'self.video_panel size:{}'.format( self.video_panel.GetClientSize() ) )
		event.Skip()

	def errorDialog(self, errormessage):
		"""Display a simple error dialog.
		"""
		edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK|wx.ICON_ERROR)
		edialog.ShowModal()
	
	#end of functions that are not used anymore
	
	def IsStereo( self ):
		audio_channel = self.player.audio_get_channel()
		return vlc.AudioOutputChannel( audio_channel ) == vlc.AudioOutputChannel.Stereo
		
	def SetVolume( self, volume ):
		with self.playerLock:
			self._volume = int( round( volume*10 ) )
			logging.debug( 'MediaPlayer.SetVolume: saving internal volume to {}'.format( self._volume ) )
			if( self.player ):
				logging.debug( 'MediaPlayer.SetVolume: volume was {}'.format( self.player.audio_get_volume() ) )
				#res: 0 if the volume was set, -1 if it was out of range.
				res = self.player.audio_set_volume( self._volume )
				logging.debug( 'MediaPlayer: setting volume to {} ({})'.format( self._volume, ( 'successfully' if res == 0 else 'error: out of range' ) ) )
		
	def GetVolume( self ):
		with self.playerLock :
			if( self.player ):
				self._volume = self.player.audio_get_volume()
				
			logging.debug( 'MediaPlayer: returning volume = {}'.format( self._volume ) )
			return self._volume/10
		
	def SetMute( self, on ):
		with self.playerLock:
			if( self.player ):
				self.player.audio_set_mute( on )
		
	def GetMute( self ):
		with self.playerLock :
			self._mute = False
			if( self.player ):
				self._mute = self.player.audio_get_mute()
				
			return self._mute
		
	def MoveTrackTime( self, move_time_millisecs ):
		"""Go backward one sec"""
		with self.playerLock:
			if( self.player ):
				print( 'moving track time from {} to {} of {}'.format( datetime.timedelta( milliseconds = self.player.get_time() ), datetime.timedelta( milliseconds = ( self.player.get_time() + move_time_millisecs ) ), datetime.timedelta( milliseconds=self.player.get_media().get_duration() ) ) ) 
				self.player.set_time( self.player.get_time() + move_time_millisecs )
				
	def SetTime( self, time_in_msecs ):
		with self.playerLock:
			if( self.player ):
				self.player.set_time( time_in_msecs )
			
	def GetState( self ):
		'''
		returns a string in [ 'NothingSpecial', 'Opening', 'Buffering', 'Playing', 'Paused', 'Stopped', 'Ended', 'Error' ]
		In your code you may import vlc and compare them to vlc.Status.Buffering, vlc.Status.Ended etc.
		'''
		with self.playerLock:
			state = vlc.State.Error #default value is that there is no player
			if( self.player ):
				state = self.player.get_state()
			return state
		
	def PrintInfo( self ):
		"""Print information about the media"""
		with self.playerLock :
			try:
				#vlc.print_version()
				media = self.player.get_media()			
				media.parse()	#this is required or else duration of media will be 0
				print( 'Duration: {}'.format( datetime.timedelta( milliseconds = media.get_duration() ) ) )
				print('State: %s' % self.player.get_state())
				print('Media: %s' % vlc.bytes_to_str(media.get_mrl()))
				print('Track: %s/%s' % (self.player.video_get_track(), self.player.video_get_track_count()))
				print('Current time: %s/%s' % (self.player.get_time(), media.get_duration()))
				print('Position: %s' % self.player.get_position()) #position is [0.0 .. 1.0]
				#print('FPS: %s (%d ms)' % (self.player.get_fps(), self._mspf()))
				print('Rate: %s' % self.player.get_rate())
				print('Video size: %s' % str(self.player.video_get_size(0)))  # num=0
				print('Scale: %s' % self.player.video_get_scale())
				print('Aspect ratio: %s' % self.player.video_get_aspect_ratio())
				print('Subtitle count: {}'.format( self.player.video_get_spu_count() ) )
				#print('Window:' % player.get_hwnd()
			except Exception:
				import sys
				print('Error: %s' % sys.exc_info()[1])
		
	def MediaIsValid( self, media_file ):
		with self.playerLock :
			is_valid = False
			try:
				#image files are recognised as valid with a duration of 1000
				#This is a bug for my application
				if( self.MediaIsImage( media_file ) ):
					return False
					
				test_instance = vlc.Instance() #just to parse media
				m = test_instance.media_new( media_file )
				m.parse()
				duration = m.get_duration()
				m.release()
				
				#debugging
				#fileName, dot_file_extension = os.path.splitext( media_file )
				#file_extension = dot_file_extension[1:]
				#print( 'duration of {}: {}'.format( file_extension, str( duration ) ) )
				#end of debugging
				
				if( duration and duration > 0.1 ):
					is_valid = True
				test_instance.release()
				#del test_instance
			except:
				#is_valid is False
				pass
			
			return is_valid
			
	def MediaIsImage( self, media_str = None ):
		with self.playerLock :
			if( media_str is None ):
				media_str = self.current_media_str
			return imghdr.what( media_str )
		
	def MediaIsVideo( self, media_str = None ):
		'''
		If no media string is passed then the request is considered to refer to the currently
		loaded media, so use the current player. If no player exists or no media is loaded return False.
		If a media string is specified use a test Intance and Player.
		'''
		with self.playerLock :
			if( media_str is None ):
				logging.debug( 'No media string, will use the current player' )
				if( self.player is None ):
					logging.debug( '\tNo current player, returning False' )
					return False
				else:
					is_video = self.player.video_get_track_count() > 0
					logging.debug( '\tcurrent player says is_video: {}'.format( is_video ) )
					return is_video
				
			testInstance = vlc.Instance( '--novideo --noaudio' ) #just to parse media and see if it has video
			m = testInstance.media_new( media_str )
			m.parse()
			testPlayer = testInstance.media_player_new()
			testPlayer.set_media( m )
			tries = 0
			testPlayer.play()
			while testPlayer.is_playing() != 1 and tries < 10:
				tries += 1
				time.sleep( 0.5 )
			if( testPlayer.is_playing() ):
				logging.debug( 'MediaIsVideo: testPlayer is playing' )
				track_count = testPlayer.video_get_track_count()
				logging.debug( '\tvideo tracks found: {}'.format( track_count ) )			
				testPlayer.stop()
				return ( track_count > 0 )
			else:
				logging.debug( 'MediaIsVideo: testPlayer is not playing' )			
				logging.debug( 'testPlayer.video_get_size(): {}'.format( testPlayer.video_get_size() ) )
				media_has_video = testPlayer.video_get_size() != ( 0L, 0L ) or media_str.startswith( 'dvd:' ) or media_str.startswith( 'dvdsimple:' )
				logging.debug( 'media_has_video: {}'.format( media_has_video ) )
				
			m.release()
			#del m
			testPlayer.release()
			#del self.player
			testInstance.release()
			#del self.Instance
			return media_has_video
			
	def MediaIsAudio( self, media_str ):
		return not self.MediaIsVideo( media_str )
		
	def CreateInstance( self, for_video ):
		logging.debug( 'MediaPlayer.CreateInstance: with volume {}'.format( self._volume ) )
		if( for_video ):
			return vlc.Instance( '--volume {} --no-video-title-show --verbose -1 --sub-filter marq --sub-source marq --sub-track 0'.format( self._volume ) )
		else:
			return vlc.Instance( '--volume {} --no-video-title-show --verbose -1 --sub-filter marq --sub-source marq --audio-visual visual --effect-list=spectrum --effect-width=1150 --audio-filter=equalizer --equalizer-preset=largehall'.format( self._volume ) )
			
	def SetSubtitleFile( self, subtitle_file ):
		if( self.player is not None ):
			if( not self.player.video_set_subtitle_file( subtitle_file ) ):
				return False
			subtitle_list = self.player.video_get_spu_description()
			index = len( subtitle_list ) - 1
			for i in reversed( subtitle_list ):
				if( i[0] > 0 and i[1] != 'Disable' ):
					return self.SetSubtitleByIndex( index ) #i[0] )
				index -= 1
			return False
		logging.debug( 'There is no vlc player!' )
		return False
				
	def GetCurrentSubtitle( self ):
		if( self.player ):
			subtitle_list = self.player.video_get_spu_description()
			logging.debug( 'subtitle_list: {}'.format( subtitle_list ) )
			current_subtitle_index = self.player.video_get_spu()
			logging.debug( 'current_subtitle_index: {}'.format( current_subtitle_index ) )
			try:
				#The index might be out of range or the list may be empty
				logging.debug( 'current_subtitle_index: {} ({})'.format( current_subtitle_index, subtitle_list[ current_subtitle_index ][1] ) )
				if( current_subtitle_index in [-1,0] or subtitle_list[ current_subtitle_index ][1] == 'Disable' ):
					subtitle = ''
				else:
					subtitle = subtitle_list[ current_subtitle_index ][1]
			except:
				subtitle = ''
			logging.debug( 'Mediaplayer.GetCurrentSubtitle returns: {}'.format( subtitle ) )
			return subtitle
			
		return ''
		
	def GetSubtitlesList( self ):
		sl = []
		if( self.player ):
			sl = self.player.video_get_spu_description()
		return sl
			
	def SetSubtitleByIndex( self, sub_index ):
		'''
		Returns True on success, False otherwise
		'''
		if( self.player ):
			success = self.player.video_set_spu( sub_index ) == 0
			logging.debug( 'set subtitle index {}, success: {}'.format( sub_index, success ) )
			return success
			
		return False
			
if __name__ == '__main__':
	class TestFrame( wx.Frame ):
		def __init__( self, parent, title ):
			wx.Frame.__init__(self, id=-1, name='', parent=parent, pos=wx.Point(358, 184), size=wx.Size(299, 387), style=wx.DEFAULT_FRAME_STYLE, title=u'Test' )
			self.panel = wx.Panel( self )
			self.Show()

	app = wx.App()
	frame = TestFrame(None, "Test")
	app.SetTopWindow(frame)

	player = MediaPlayer( frame.panel, RLock() )
	# file = '/home/antonis/Shared/SkidRow - Youth Gone Wild.mp3'
	file ='/home/antonis/Videos/to_Agistri.mp4'
	file = 'http://192.168.1.1:57645/external/video/media/615.avi'
	sub_file = 'http://192.168.1.1:57645/b64/H4sIAAAAAAAAANMvLskvSkxP1U_NLc1JLElN0TfQ980vy0wt1nfMy0vU804sSs3LBDKMDAyN9FzCXIKdg_QiyjJddP0iXTydiVKkV1xUAgCvZTDjaAAAAA==.srt'
	player.SetSubtitleFile( sub_file )
	player.Play( file )
	logging.debug( 'subtitles: {}'.format( player.GetSubtitlesList() ) )
	app.MainLoop()
