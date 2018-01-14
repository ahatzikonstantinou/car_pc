#! /usr/bin/python
# -*- coding: utf-8 -*-

from media_player import *

class UPnPMediaPlayer( MediaPlayer ):
	''' 
	This media player just has different MediaIsVideo and MediaIsAudio detection methods
	'''

	def __init__( self, video_parent_panel, playerLock, videoPanelClickCallback = None ):
		MediaPlayer.__init__( self,	video_parent_panel, playerLock, videoPanelClickCallback )

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
