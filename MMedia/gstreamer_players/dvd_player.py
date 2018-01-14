#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib

from generic_player import *

import wx #for testing visualization only

class DVDPlayer( GenericPlayer ):

	def __init__( self, video_window, EndOfSongCallback = None, PlayerReadyCallback = None, ErrorCallback = None ):
		GenericPlayer.__init__( self, EndOfSongCallback, PlayerReadyCallback, ErrorCallback )
		self.video_window = video_window
		self.bus.connect("sync-message::element", self.on_sync_message)	#required for video

	def SetCurrentFile( self, filename ):
		self.current_file_uri = filename
		self.pipeline.set_property( 'uri', self.current_file_uri )

	def AddPipelineElements( self, pipeline ):
		#Major override. The self.pipeline is not a pipeline anymore as in generic_player
		#but a playbin2 element
		self.pipeline = gst.element_factory_make( 'playbin2', 'playbin' )
		# self.src = gst.element_factory_make( 'filesrc', 'filesrc' )
		# self.decodebin = gst.element_factory_make( 'decodebin2', 'decodebin' )
		self.videosink = gst.element_factory_make( 'autovideosink', 'videosink' )
		self.pipeline.set_property( 'video-sink', self.videosink )

		#put volume and equalizer elements in ghost bin to use a sink for playbin2
		self.bin = gst.Bin()
		self.volume = gst.element_factory_make( 'volume', 'volume' )
		self.equalizer = gst.element_factory_make( 'equalizer-3bands', 'equalizer' )
		sink = gst.element_factory_make( 'gconfaudiosink', 'sink' )
		
		self.bin.add_many( self.volume, self.equalizer, sink )
		gst.element_link_many(  self.volume, self.equalizer, sink )

		pad = self.volume.get_static_pad( "sink" )

		ghost_pad = gst.GhostPad( "sink", pad )
		ghost_pad.set_active( True )
		self.bin.add_pad( ghost_pad )
		#gst_object_unref (pad);

		# For testing only Configure the equalizer
		self.pipeline.set_property( "volume", 0.1 )
		self.equalizer.set_property( "band1", -24.0 )
		self.equalizer.set_property( "band2", -24.0, )

		# Set playbin2's audio sink to be our sink bin
		self.pipeline.set_property( "audio-sink", self.bin )

		#add visualization
		visualization = gst.element_factory_make( 'libvisual_lv_scope' )
		self.pipeline.set_property( 'vis-plugin', visualization )
		self.pipeline.set_property( 'flags', 0x00000001f )


	def Start( self ):
			# print( 'DoStart is running now with{} visualization'.format( ( 'out' if self.file_has_video else '' ) ) )
			# if( self.file_has_video ):
			# 	self.pipeline.set_property( 'vis-plugin', None )
			# else:
			# 	print( 'adding goom' )
			# 	visualization = gst.element_factory_make( 'goom' )
			# 	self.pipeline.set_property( 'vis-plugin', visualization )
			GenericPlayer.Start( self )

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == 'prepare-xwindow-id':
			imagesink = message.src
			imagesink.set_property('force-aspect-ratio', True)
			imagesink.set_xwindow_id( self.video_window.GetHandle() )

if __name__ == '__main__':
	class TestFrame( wx.Frame ):
		def __init__( self, parent, title ):
			wx.Frame.__init__(self, id=-1, name='', parent=parent, pos=wx.Point(358, 184), size=wx.Size(299, 387), style=wx.DEFAULT_FRAME_STYLE, title=u'Test' )
			self.panel = wx.Panel( self )
			self.Show()

	app = wx.App()
	frame = TestFrame(None, "Test")
	app.SetTopWindow(frame)
	# frame.Show()

	player = DVDPlayer( frame.panel )
	player.Activate()
	# from os import listdir
	# directory = '/home/antonis/Videos/eftihismenoi mazoi'
	# files = listdir( directory )
	# for f in files:
		# f = directory + '/' + f
	# f = "/home/antonis/Videos/treadmill.wmv"
	# f = '/home/antonis/Videos/to_Agistri.mp4'
	#f = '/home/antonis/Videos/VIDEO_001.mp4'
	f = 'dvd:///media/DANCING_WITH_WOLVES_DISC_2/'
	# print f
	player.SetCurrentFile( f )
	# import pprint; pprint.pprint( player )
	print player.current_file_uri
	player.Start()
	import time ; time.sleep( 150 )
	player.Stop()
	# print( '{}'.format( player.pipeline.get_property( 'uri' ) ) )

	app.MainLoop()
