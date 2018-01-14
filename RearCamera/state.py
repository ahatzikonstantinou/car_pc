#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class State:
	'''This is the state of the viewer'''
	
	Filename = "state.camera"	#the file were the state is saved
	IMAGEMAX = True
	IMAGENORMAL = False
	def __init__( self ):
		self.maxImage = State.IMAGEMAX
		self.brightness = 50
		self.contrast = 50
		self.device = 'v4l2:///dev/video0'
		
	def SetBrightness( self, brightness ):
		self.brightness = brightness
		self.Save()
						
	def SetContrast( self, contrast ):
		self.contrast = contrast
		self.Save()
		
	def SetDevice( self, device ):
		self.device = device
		self.Save()
						
	def Load( self ):
		with open( State.Filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
	
	def Save(self):
		with open( State.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )

if __name__ == "__main__":
    s = State()
    s.Save()
