#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from media_device import MediaDeviceState

class RadioState( MediaDeviceState ):
	'''This is the state of the radio e.g. currently tuned frequency'''
	
	Filename = "state.radio"	#the file were the state is saved
	STATIONSELECTOR = 0
	NUMERICSELECTOR = 1
	def __init__( self ):
		MediaDeviceState.__init__( self )
		self.selector = RadioState.STATIONSELECTOR
		self.frequency = 87.5
		#self.mute = False
		#self.speed_dials = {}
		#self.volume = 0
		
	def SetFrequency( self, frequency ):
		self.frequency = frequency
		
	def SetStationSelector( self, selector ):
		self.selector = selector
		self.Save()
		
	#def SetMute( self, mute ):
		#self.mute = mute
		#self.Save()
		
		
	def Load( self ):
		print( 'RadioState loading from {}'.format( RadioState.Filename ) )
		if( not os.path.isfile( RadioState.Filename ) ):
			print( 'file {} not found'.format( RadioState.Filename ) )
			return
		with open( RadioState.Filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
			print( 'file {} loaded successfully'.format( RadioState.Filename ) )
		#~ print( self.speed_dials )
	
	def Save(self):
		with open( RadioState.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )
	
	def FrequencyIs( self, frequency ):
		'''FrequencyObserver'''
		self.frequency = round( frequency, 2 )
		self.Save()
		
	def Report( self ):
		print( 'Tuned to {0}MHz'.format( self.frequency ) )

if __name__ == "__main__":
    s = State()
    s.Save()
