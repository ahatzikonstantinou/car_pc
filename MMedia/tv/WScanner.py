#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
#import shlex
import sys
import re
import signal

from Channel import *

import traceback 

class ProcessException( Exception ):
	def __init__( self, command, exitCode, output ):
		self.command = command
		self.exitCode = exitCode
		self.output = output

class WScannerStatus:
	NOTSTARTED = 0
	SCANNING = 1
	FINALIZING = 2
	FINISHED = 3
	
class WScanner:
	CHANNELSCONFFILE = 'mychannels.conf'
	TMPEXT = '.tmp'
	#min and max channel will be used to calculate progress
	__MINCHANNEL = 0
	__MAXCHANNEL = 133
	
	def __init__( self, callbackFunction = None, channels = {},
		w_scanCommand = 'w_scan -"vv" -ft -c GR -X', channelsFile = 'mychannels.conf'
		):
		'''The command line must include -X and -vv. -X specifies the file format.
		   -vv (or more v's) ensures that channellist and channel number info will be generated
		   as w_scan runs. These are required to be able to give progress feedback to the calling 
		   application'''
		self.w_scanCommand = w_scanCommand + ' > '
		self.channelsFile = channelsFile
		self.status = WScannerStatus.NOTSTARTED
		self.scanProcess = None
		self.callbackFunction = callbackFunction
		self.channels = channels

	def Scan( self, merge = False ):
		outfile = self.channelsFile
		if( merge ):
			outfile += WScanner.TMPEXT

		command = self.w_scanCommand + outfile
		print( 'Executing: "{}"'.format( command ) )
		process = subprocess.Popen( command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		self.status = WScannerStatus.SCANNING
		self.scanProcess = process
		try:			
			channel = -1
			# Poll process for new output until finished
			while True:
				nextline = process.stdout.readline()
				if nextline == '' and process.poll() != None:
					break
								
				if( 'channel=' in nextline ):
					#print( 'got a channel line:{}'.format( nextline ) )
					m = re.compile( r'.*, channel=([0-9]+),' ).match( nextline )
					if( m is None ):
						continue
					mg = m.groups()
					#print( mg )
					newChannel = int( mg[0] )
					#print( '\tchannel was {} and now is {}'.format( channel, newChannel ) )
					if( channel != newChannel ):						
						channel = newChannel
						print( 'Current channel: {}'.format( channel ) )
						self.CallCallback( channel, 'Scanning...' )
						
					if( channel >= WScanner.__MAXCHANNEL ):
						self.status = WScannerStatus.FINALIZING
						self.CallCallback( channel, 'Finalizing...' )
						
				#else:
					#print( 'this is not a channel line:{}'.format( nextline ) )
				#sys.stdout.write(nextline)
				#sys.stdout.flush()

			output = process.communicate()[0]
			exitCode = process.returncode
			self.status = WScannerStatus.FINISHED
			self.CallCallback( channel, 'Finished' )
		except:
			traceback.print_exc()
			print "Bye"
			self.StopScan()
			sys.exit()

		if (exitCode == 0):
			if( merge ):				
				self.MergeChannels( self.ReadConf( outfile ) )
			return output
		else:
			raise ProcessException(command, exitCode, output)
	
	def CallCallback( self, channel, message ):
		#self.Progress( channel )
		if( self.callbackFunction is not None ):
			self.callbackFunction( CallbackData( self.Progress( channel ), self.status, message ) )
			
	def Progress( self, channel ):
		pr = int( ( ( channel - WScanner.__MINCHANNEL )*100.0 )/( WScanner.__MAXCHANNEL - WScanner.__MINCHANNEL ) )
		#print( 'Returning progress {}%'.format( pr ) )
		return pr
		
	def MergeChannels( self, newChannels ):
		#print( 'MergeChannels:' );
		for key, value in newChannels.iteritems():
			#print( 'merging key:{0}, channel:{1}'.format( key, value.name ) )
			self.channels[key] = value
		#print( 'Returning merged channels:' )
		#for st in self.channels.values():
			#st.Dump()

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
			channels[ channel.GetHash() ] = channel
		file.close()
		
		#print( 'Read channels:' )
		#for key, value in channels.iteritems():
			#value.Dump()
		#print( 'End of channels' )
		return channels

	def StopScan( self ):
		if( self.status != WScannerStatus.NOTSTARTED and
			self.status != WScannerStatus.FINISHED and
			self.scanProcess is not None 
			):
			self.scanProcess.kill()
			self.status = WScannerStatus.NOTSTARTED

class CallbackData:
	def __init__( self, progressPercent, status, message ):
		self.progressPercent = progressPercent
		self.status = status
		self.message = message
		
def Callback( callbackData ):
	print( '{}%, status:{}, message:{}'.format( 
		callbackData.progressPercent, callbackData.status, callbackData.message ) )
	
if( __name__ == '__main__' ):
    scanner = WScanner( callbackFunction = Callback )
    #scanner.Scan()
    scanner.ReadConf( 'channels.conf' )
