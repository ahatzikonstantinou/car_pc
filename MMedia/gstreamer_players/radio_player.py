#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygst
pygst.require("0.10")
import gst
from threading import Thread

# from gi.repository import GstPbutils

from generic_player import *

class RadioPlayer( GenericPlayer ):
	PULSESRC_DEVICE = 'alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo'
	def __init__( self, pulsesrc_device = PULSESRC_DEVICE, EndOfSongCallback = None, PlayerReadyCallback = None, ErrorCallback = None ):
		self.pulsesrc_device = pulsesrc_device 	#this line needs to be executed before the parent class
												#constructor, because the parent constructor will call 
												#the overriden AddPipelineElements which uses self.pulsesrc_device
		GenericPlayer.__init__( self, EndOfSongCallback, PlayerReadyCallback, ErrorCallback )
		
		#pulsesrc device=alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo ! volume volume=10.0 mute=False ! equalizer-3bands band0=12.0 band1=-24.0 band2=-24.0 ! pulsesink

	# 	# self.discoverer = GstPbutils.Discoverer()
	# 	# self.discoverer.connect( 'discovered', self._OnDiscovered )
	# 	# self.discoverer.discover_uri( 'file:///home/antonis/Shared/Skidrow - Slave To The Grind.mp3' )

	# def _OnDiscovered( self, success ):
	# 	print( '_OnDiscovered called with success: '.format( success ) )
		
	def AddPipelineElements( self, pipeline ):
		pulsesrc = gst.element_factory_make( 'pulsesrc', 'pulsesrc' )
		pulsesrc.set_property( 'device', self.pulsesrc_device )
		self.volume = gst.element_factory_make( 'volume', 'volume' )
		self.equalizer = gst.element_factory_make( 'equalizer-3bands', 'equalizer' )
		sink = gst.element_factory_make( 'pulsesink', 'pulsesink' )
		# sink = gst.element_factory_make( 'gconfaudiosink', 'sink' )
		
		pipeline.add( pulsesrc, self.volume, self.equalizer, sink )
		gst.element_link_many( pulsesrc, self.volume, self.equalizer, sink )
