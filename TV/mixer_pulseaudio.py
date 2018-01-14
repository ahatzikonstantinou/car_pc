#!/usr/bin/python
# -*- coding: utf-8 -*-

from mixer import *
import subprocess
import os
from pprint import pprint
class PulseaudioMixer( mixer ):
	"""
	Pulseaudio implementation for a mixer.
	Executable Scripts 'set_volume', 'get_volume', 'set_mute', 'get_mute'
	must exist in subdir pulseaudio in the application's main dir
	"""
	CMDDIR = os.getcwd() + '/scripts/pulseaudio/'
	def __init__( self, shortName ):
		self.sourceName = self.GetSourceName( shortName )
		
	@staticmethod
	def GetSourceName( sourceName ):
		command = PulseaudioMixer.CMDDIR + 'get_source_name'
		#print( 'cmd:{}'.format( command ) )
		return ExecuteShellCommand( [ command, sourceName ] ).strip()
	
	def SetVolume( self, volume ):
		ExecuteShellCommand( [PulseaudioMixer.CMDDIR + 'set_volume', self.sourceName, str( volume ) + '%' ] )
		
	def GetVolume( self ):
		value = ExecuteShellCommand( [PulseaudioMixer.CMDDIR + 'get_volume', self.sourceName] )
		#print ' '.join( value.split() )
		volume = ' '.join( value.split() ).split( ' ' )[2]
		return int( volume.strip( '%' ) )
		
	def SetMute( self, on ):
		ExecuteShellCommand( [PulseaudioMixer.CMDDIR + 'set_mute', self.sourceName, ( '1' if on else '0' )] )

	def GetMute( self ):
		mute = ExecuteShellCommand( [PulseaudioMixer.CMDDIR + 'get_mute', self.sourceName] )
		#print( 'get_mute:{}'.format( mute ) )
		return mute.strip() == 'yes'
		
def ExecuteShellCommand( cmd ):
	#pprint( cmd )
	return subprocess.check_output( cmd )

if __name__ == '__main__':
	sname = 'TV'
	pMixer = PulseaudioMixer( sname )
	print( 'source:"{}"'.format( pMixer.sourceName ) )
	
	volume = 99
	print( 'set volume {}'.format( volume ) )
	pMixer.SetVolume( volume ) ;
	print( 'volume:{}%'.format( pMixer.GetVolume() ) )
	
	mute = False
	print( 'set mute' ) ; pMixer.SetMute( mute )
	print( 'mute:{}'.format( pMixer.GetMute() ) )
