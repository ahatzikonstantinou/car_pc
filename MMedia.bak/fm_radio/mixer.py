#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class mixer:
	def SetVolume( self, volume ):
		pass
		
	def GetVolume( self ):
		pass
		
	def SetMute( self, on ):
		pass
		
	def GetMute( self ):
		pass


class DummyMixer( mixer ):
	def __init__( self ):
		pass
		
	def SetVolume( self, volume ):
		pass
		
	def GetVolume( self ):
		return random.randint( 0, 100 )
		
	def SetMute( self, on ):
		pass
		
	def GetMute( self ):
		return 0 #random.randint( 0, 1 )
