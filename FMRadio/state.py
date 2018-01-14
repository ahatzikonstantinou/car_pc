#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class State:
	'''This is the state of the radio e.g. currently tuned frequency'''
	
	Filename = "state.radio"	#the file were the state is saved
	STATIONSELECTOR = 0
	NUMERICSELECTOR = 1
	def __init__( self ):
		self.selector = State.STATIONSELECTOR
		self.frequency = 87.5
		#self.mute = False
		self.speedDials = {}
		#self.volume = 0
		
	def SetStationSelector( self, selector ):
		self.selector = selector
		self.Save()
		
	#def SetMute( self, mute ):
		#self.mute = mute
		#self.Save()
		
	def SetSpeedDial( self, index, frequency ):
		self.speedDials[index] = frequency
		self.Save()
	
	def DelSpeedDial( self, index ):
		del self.speedDials[index]
		self.Save()
		
	def Load( self ):
		with open( State.Filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
	
	def Save(self):
		with open( State.Filename, mode='w' ) as f:
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
