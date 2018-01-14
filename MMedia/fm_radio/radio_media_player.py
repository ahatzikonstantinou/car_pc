#! /usr/bin/python
# -*- coding: utf-8 -*-

from media_player import *

class RadioMediaPlayer( MediaPlayer ):
	''' 
	This media player just has different MediaIsVideo and MediaIsAudio detection methods
	'''

	def __init__( self, playerLock, pulseuadio_source ):
		MediaPlayer.__init__( self,	playerLock )
		self.Instance = self.CreateInstance()
		self.player = self.Instance.media_player_new()
		self.current_media_str = pulseuadio_source
		m = self.Instance.media_new( self.current_media_str )
		self.player.set_media( m )
		#self.player.audio_set_mute( True )
		self.player.play()
		#self.player.audio_set_mute( True )
		m.release()
		
	def Start( self ):
		'''
		Override this because this player will not draw any graphics anywhere
		'''
		return
		
	def CreateInstance( self ):
		'''
		Only audio for radio
		'''
		return vlc.Instance( '--volume 0 --no-video-title-show --verbose -1 --sub-filter marq --sub-source marq  --effect-list=spectrum --audio-filter=equalizer --equalizer-preset=largehall' )
		
	def Play( self, media_str, options = None ):
		with self.playerLock :
			#self.current_media_str = media_str
			#self.Instance = MediaPlayer.CreateInstance( self, False )
			#self.player = self.Instance.media_player_new()
			#self.Start()
			#m = self.Instance.media_new( self.current_media_str )
			#if( self.current_media_options ):
				#m.add_options( self.current_media_options )
			#self.player.set_media( m )
			#m.release()
			self.player.play()
			
	def _AttachEvents( self ):
		if( self.player ):
			self.event_manager = self.player.event_manager()
			self.event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._OnErrorEvent )
			#self.event_manager.event_attach( vlc.EventType.MediaPlayerPlaying, self._OnPlaying )
		
	@vlc.callbackmethod
	def _OnPlaying( self, event ):
		'''
		For some unknown reason, in order to set the volume of the vlc player right, I MUST do it some amount of time AFTER it starts playing e.g. 100 milliseconds or else no matter how I set the volume (in the Instance constructor or explicitly via self.player.audio_set_volume) the volume returned by self.player.audio_get_volume is the one I set, but the vlc application in ubuntu's settings clearly shows (and that is exactly how it sounds) that the vlc instance is playing at the volume level of the PREVIOUS vlc instance running in the previously active device. WEIRD.
		'''
		wx.CallLater( 100, self.player.audio_set_mute, True )

if __name__ == '__main__':
	class TestFrame( wx.Frame ):
		def __init__( self, parent, title ):
			wx.Frame.__init__(self, id=-1, name='', parent=parent, pos=wx.Point(358, 184), size=wx.Size(299, 387), style=wx.DEFAULT_FRAME_STYLE, title=u'Test' )
			self.panel = wx.Panel( self )
			self.Show()

	app = wx.App()
	frame = TestFrame(None, "Test")
	app.SetTopWindow(frame)

	player = VlcPlayer( frame.panel )
	# file = '/home/antonis/Shared/SkidRow - Youth Gone Wild.mp3'
	file ='/home/antonis/Videos/to_Agistri.mp4'
	player.Play( file )

	app.MainLoop()
