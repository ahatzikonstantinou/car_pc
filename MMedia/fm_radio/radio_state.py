#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from media_player_device import MediaPlayerDeviceState

class RadioState( MediaPlayerDeviceState ):
	'''This is the state of the radio e.g. currently tuned frequency'''
	
	Filename = "state.radio"	#the file were the state is saved
	STATIONSELECTOR = 0
	NUMERICSELECTOR = 1
	def __init__( self ):
		MediaPlayerDeviceState.__init__( self )
		self.selector = RadioState.STATIONSELECTOR
		self.frequency = 87.5
		
	def SetFrequency( self, frequency ):
		self.frequency = frequency
		
	def SetStationSelector( self, selector ):
		self.selector = selector
		self.Save()

	def Load( self ):
		print( 'RadioState loading from {}'.format( RadioState.Filename ) )
		if( not os.path.isfile( RadioState.Filename ) ):
			print( 'file {} not found'.format( RadioState.Filename ) )
			return
		with open( RadioState.Filename, mode='r' ) as f:
			data = json.load( f )
			#self.__dict__ = json.load( f )
			for key in self.__dict__:
				if( key in data.keys() ):
					self.__dict__[key] = data[key]
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
