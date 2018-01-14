#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygst
pygst.require("0.10")
import gst

from threading import Thread

import gobject
gobject.threads_init()

#'When using gi.repository you must not import static modules like "gobject". Please change all occurrences of "import gobject" to "from gi.repository import GObject".'
# from gi.repository import GObject
# GObject.threads_init()


class GenericPlayer:
	def __init__( self, EndOfSongCallback = None, PlayerReadyCallback = None, ErrorCallback = None ):
		self.EndOfSongCallback = EndOfSongCallback
		self.PlayerReadyCallback = PlayerReadyCallback
		self.ErrorCallback = ErrorCallback
		
		self.thread = GobjectThread()

		self.pipeline = gst.Pipeline( 'pipeline' )
		
		#Concrete players must create these elements and add them in the pipeline
		#and link them (see the commented code in AddPipelineElements for an example)
		self.volume = None
		self.equalizer = None

		self.AddPipelineElements( self.pipeline )
		
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()
		self.bus.enable_sync_message_emission()
		self.bus.connect('message', self._OnMessage)
		
	def AddPipelineElements( self, pipeline ):
		raise Exception( 'All concrete player must override AddPipelineElements' )
		#pulsesrc = gst.element_factory_make( 'pulsesrc', 'pulsesrc' )
		#pulsesrc.set_property( 'device', self.pulsesrc_device )
		#self.volume = gst.element_factory_make( 'volume', 'volume' )
		#self.equalizer = gst.element_factory_make( 'equalizer-3bands', 'equalizer' )
		#pulsesink = gst.element_factory_make( 'pulsesink', 'pulsesink' )
		#
		#pipeline.add( pulsesrc, self.volume, self.equalizer, pulsesink )
		#gst.element_link_many( pulsesrc, self.volume, self.equalizer, pulsesink )
		

	def Activate( self ):
		self.thread.start()
		
	def Deactivate( self ):
		self.pipeline.set_state( gst.STATE_NULL )
		self.thread.quit() #End the gobject.MainLoop()
          
	def Start( self ):
		self.pipeline.set_state( gst.STATE_PLAYING )
		
	def Stop( self ):
		self.pipeline.set_state( gst.STATE_NULL )
		
	def SetVolume( self, volume ):
		'''
		Volume [0.0 - 1.0]
		'''
		self.volume.set_property( 'volume', volume )
		
	def GetVolume( self ):
		return self.volume.get_property( 'volume' )
		
	def SetMute( self, mute ):
		#mute = ( 1 if mute else 0 )
		#print( 'player: setting mute to {}'.format( mute ) )
		self.volume.set_property( 'mute', mute )
		
	def GetMute( self ):
		return self.volume.get_property( 'mute' )
		
	def SetEqualizer( self, band0, band1, band2 ):
		'''
		band0 gain for the frequency band 100 Hz, ranging from -24.0 to +12.0.
		band1 gain for the frequency band 1100 Hz, ranging from -24.0 to +12.0.
		band2 gain for the frequency band 11 kHz, ranging from -24.0 to +12.0.
		Allowed values: [-24,12]
		Default value: 0
		'''
		if( band0 > 12.0 or band0 < -24.0 or 
			band1 > 12.0 or band1 < -24.0 or 
			band2 > 12.0 or band2 < -24.0 ):
			raise Exception( 'The band values must be in the range [-24.0 - 12.0]. Band0:{}, Band1:{}, Band2:{}'.format( band0, band1, band3 ) )
			
		self.equalizer.set_property( 'band0', band0 )
		self.equalizer.set_property( 'band1', band1 )
		self.equalizer.set_property( 'band2', band2 )
                          
	def _OnMessage(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.pipeline.set_state( gst.STATE_NULL )
			if( self.EndOfSongCallback ):
				self.EndOfSongCallback()
		elif t == gst.MESSAGE_ERROR:
			self.pipeline.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			if( self.ErrorCallback ):
				self.ErrorCallback( err )
			if( self.PlayerReadyCallback ):
				self.PlayerReadyCallback()
	
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

