#!/usr/bin/python
# -*- coding: utf-8 -*-

from mixer import *

class DummyMixer( mixer ):
	def __init__( self ):
		self.__mute = False
		self.__volume = 0
		
	def SetVolume( self, volume ):
		self.__volume = volume
		
	def GetVolume( self ):
		return self.__volume
		
	def SetMute( self, on ):
		self.__mute = on
		
	def GetMute( self ):
		return self.__mute
