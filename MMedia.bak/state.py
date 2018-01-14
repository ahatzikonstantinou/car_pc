#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

class State:
	'''This is the state of the mmedia e.g. currently active device'''
	
	Filename = "state.mmedia"	#the file were the state is saved
	def __init__( self ):
		self.current_device_hash = ''
		self._volume = 5
		self._mute = False
				
	def SetVolume( self, volume ):
		self._volume = volume
		self.Save()
	
	def GetVolume( self ):
		return self._volume
		
	def SetMute( self, mute ):
		self._mute = mute
		self.Save()
		
	def GetMute( self ):
		return self._mute
		
	def Load( self ):
		if( not os.path.isfile( State.Filename ) ):
			return
		with open( State.Filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
	
	def Save(self):
		with open( State.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )
			
	def SetCurrentDeviceHash( self, device_hash ):
		self.current_device_hash = device_hash
		self.Save()
	
if __name__ == "__main__":
    s = State()
    s.Save()
