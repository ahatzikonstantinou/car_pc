#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib

from discoverer import Discoverer

from generic_player import *

import time #for testing discoverer's discover time
import wx #for testing visualization only

import gobject
gobject.threads_init()

class FilesystemPlayer( GenericPlayer ):
	SUPPORTED_FILE_EXTS = ['.wav', '.wma', '.aac-', '.ogg', '.mp3', '.ac3', '.3gp', '.avi', '.b-mtp', '.flv', '.mov', '.spx', '.flac', '.aiff', '.au', '.vox', '.ape', '.msv', '.mp4', '.mpg', '.mpeg', '.raw', '.midi', '.msv', '.ulaw', '.alaw', '.mu law', '.gsm']

	def __init__( self, video_window, EndOfSongCallback = None, PlayerReadyCallback = None, ErrorCallback = None ):
		GenericPlayer.__init__( self, EndOfSongCallback, PlayerReadyCallback, ErrorCallback )
		self.discovery_start_time = 0
		self.ready_to_play = False
		self.asked_to_start = False
		self.video_window = video_window

		self.bus.connect("sync-message::element", self.on_sync_message)	#required for video

	def _OnDiscovered( self, discoverer, success ):
		# print( 'arg:{}, success:{}'.format( arg.__class__.__name__, success ) )
		print( '_OnDiscovered called with success: '.format( success ) )
		# import pprint; pprint.pprint( discoverer )
		import datetime
		elapsed_time = str(datetime.timedelta( seconds = ( time.time() - self.discovery_start_time ) ) )
		print( 'Discoverer finished in {} time?'.format( elapsed_time ) )
		discoverer.print_info()
		self.ready_to_play = True
		self.file_has_video = discoverer.is_video
		if( self.asked_to_start ):
			self.DoStart()

	def SetCurrentFile( self, filename ):
		self.current_file_uri = 'file://' + os.path.abspath( filename )
		self.pipeline.set_property( 'uri', self.current_file_uri )
		discoverer = Discoverer( os.path.abspath( filename ) )
		discoverer.connect( 'discovered', self._OnDiscovered )
		self.discovery_start_time = time.time()
		discoverer.discover()
		self.ready_to_play = False #will be ready when discoverer has finished

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

	def CanProbablyPlayFile( self, filename ):
		filename, extension = os.path.splitext( filename )
		return extension in FilesystemPlayer.SUPPORTED_FILE_EXTS

	def Start( self ):
		'''Override. Will play only after discoverer has finished file discovery'''
		self.asked_to_start = True

		#If ready, start now, else wait until the discoverer has finished and start then
		if( self.ready_to_play ):
			self.DoStart()

	def DoStart( self ):
			self.asked_to_start = False
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
	class GobjectThread(Thread):
		def __init__(self):
			Thread.__init__(self)
			##############################
			self.loop = gobject.MainLoop() # The mainloop to be separated from wx
			##############################

		def run(self): # Called on Thread.start()
			self.loop.run()

		def quit(self):
			# Stops the gobject Mainloop
			self.loop.quit()
			
	class TestFrame( wx.Frame ):
		def __init__( self, parent, title ):
			wx.Frame.__init__(self, id=-1, name='', parent=parent, pos=wx.Point(358, 184), size=wx.Size(299, 387), style=wx.DEFAULT_FRAME_STYLE, title=u'Test' )
			self.panel = wx.Panel( self )
			self.Show()

	app = wx.App()
	frame = TestFrame(None, "Test")
	app.SetTopWindow(frame)
	# frame.Show()

	player = FilesystemPlayer( frame.panel )
	player.Activate()
	# from os import listdir
	# directory = '/home/antonis/Videos/eftihismenoi mazoi'
	# files = listdir( directory )
	# for f in files:
		# f = directory + '/' + f
	#f = "/home/antonis/Videos/treadmill.wmv"
	f = '/home/antonis/Videos/to_Agistri.mp4'
	#f = '/home/antonis/Videos/VIDEO_001.mp4'
	# print f
	player.SetCurrentFile( f )
	# import pprint; pprint.pprint( player )
	print player.current_file_uri
	player.Start()
	#import time ; time.sleep( 15 )
	#player.Stop()
	# print( '{}'.format( player.pipeline.get_property( 'uri' ) ) )

	app.MainLoop()
	#GobjectThread()
