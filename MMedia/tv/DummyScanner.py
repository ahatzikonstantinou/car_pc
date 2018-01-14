#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
#import shlex
import sys
import re
import signal

from Channel import *
from WScanner import *
import traceback
import time

class DummyScanner( WScanner ):	
	def __init__( self, callbackFunction = None, channels = {}, progressStepSeconds = 0.1, 
		progressStepSize = 15 ):
		self.status = WScannerStatus.NOTSTARTED
		self.callbackFunction = callbackFunction
		self.channels = channels
		self.newChannels = { 1:Channel('A'), 2:Channel('B'), 3:Channel('C') }
		self.progress = WScanner._WScanner__MINCHANNEL
		self.progressStepSeconds = progressStepSeconds
		self.progressStepSize = progressStepSize

	def __Progress( self ):
		if( self.progress >= WScanner._WScanner__MAXCHANNEL ):
			return
			
		self.progress += self.progressStepSize
		if( self.progress > 90 and self.progress < WScanner._WScanner__MAXCHANNEL ):
			self.status = WScannerStatus.FINALIZING
			self.CallCallback( self.progress, 'Finalizing...' )
		elif( self.progress == WScanner._WScanner__MAXCHANNEL ):
			self.status = WScannerStatus.FINISHED
			self.CallCallback( self.progress, 'Finished' )
		else:
			self.CallCallback( self.progress, 'Scanning...' )
		
	def Scan( self, merge = False ):
		self.status = WScannerStatus.SCANNING
		while( self.progress < WScanner._WScanner__MAXCHANNEL and
			( self.status == WScannerStatus.SCANNING or self.status == WScannerStatus.FINALIZING ) ):
			self.__Progress()
			time.sleep( self.progressStepSeconds )
		if( merge ):
			#print( 'Merging...' )
			self.MergeChannels( self.newChannels )
		else:
			#print( 'Replacing...' )
			self.channels = self.newChannels
	
	def CallCallback( self, channel, message ):
		#self.Progress( channel )
		if( self.callbackFunction is not None ):
			self.callbackFunction( CallbackData( self.Progress( channel ), self.status, message ) )
			
	def Progress( self, channel ):
		pr = int( ( ( channel - WScanner._WScanner__MINCHANNEL )*100.0 )/( WScanner._WScanner__MAXCHANNEL - WScanner._WScanner__MINCHANNEL ) )
		#print( 'Returning progress {}%'.format( pr ) )
		return pr

	def ReadConf( self, filename ):
		channels = {}
		#print( 'Opening file:{}'.format( filename ) )
		file = open( filename )
		while 1:
			line = file.readline()
			#print( 'read line:{}'.format( line ) )
			if not line:
				break
			channel = Channel.Parse( line )
			#print( 'got parsed channel:' ) ; channel.Dump()
			key = channel.frequency + '_' + channel.service_id.strip()
			channels[key] = channel
		file.close()
		
		#print( 'Read channels:' )
		#for key, value in channels.iteritems():
			#value.Dump()
		#print( 'End of channels' )
		return channels

	def StopScan( self ):
		if( self.status != WScannerStatus.NOTSTARTED and
			self.status != WScannerStatus.FINISHED 
			):
			self.status = WScannerStatus.NOTSTARTED

class CallbackData:
	def __init__( self, progressPercent, status, message ):
		self.progressPercent = progressPercent
		self.status = status
		self.message = message
