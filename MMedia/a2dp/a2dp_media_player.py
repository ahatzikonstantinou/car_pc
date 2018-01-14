#! /usr/bin/python
# -*- coding: utf-8 -*-

from media_player import *

class A2DPMediaPlayer( MediaPlayer ):
	''' 
	This media player just has different MediaIsVideo and MediaIsAudio detection methods
	'''

	def __init__( self, playerLock, video_parent_panel, videoPanelClickCallback = None ):
		MediaPlayer.__init__( self,	playerLock, video_parent_panel, videoPanelClickCallback )
		
	def CreateInstance( self, for_video ):
		'''
		Only audio for a2dp devices
		'''
		return MediaPlayer.CreateInstance( self, False )

	def _AttachEvents( self ):
		if( self.player ):
			self.event_manager = self.player.event_manager()
			self.event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._OnErrorEvent )

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
