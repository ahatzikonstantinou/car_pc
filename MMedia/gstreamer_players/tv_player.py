#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygst
pygst.require("0.10")
import gst
import gobject
from threading import Thread

import gobject
gobject.threads_init()

from generic_player import *

class RadioPlayer( GenericPlayer ):
	PULSESRC_DEVICE = 'alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo'
	def __init__( self, pulsesrc_device = PULSESRC_DEVICE, EndOfSongCallback = None, PlayerReadyCallback = None, ErrorCallback = None ):
		GenericPlayer.__init__( self, pulsesrc_device, EndOfSongCallback, PlayerReadyCallback, ErrorCallback )
		
		#pulsesrc device=alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo ! volume volume=10.0 mute=False ! equalizer-3bands band0=12.0 band1=-24.0 band2=-24.0 ! pulsesink
		
	def AddPipelineElements( self, pipeline ):
		pulsesrc = gst.element_factory_make( 'pulsesrc', 'pulsesrc' )
		pulsesrc.set_property( 'device', self.pulsesrc_device )
		self.volume = gst.element_factory_make( 'volume', 'volume' )
		self.equalizer = gst.element_factory_make( 'equalizer-3bands', 'equalizer' )
		pulsesink = gst.element_factory_make( 'pulsesink', 'pulsesink' )
		
		pipeline.add( pulsesrc, self.volume, self.equalizer, pulsesink )
		gst.element_link_many( pulsesrc, self.volume, self.equalizer, pulsesink )
