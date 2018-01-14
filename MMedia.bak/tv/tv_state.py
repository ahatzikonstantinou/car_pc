#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
#from VLCControl import *
from media_device import MediaDeviceState

class TVState( MediaDeviceState ):
	'''This is the state of the tv e.g. currently tuned channel'''
	
	Filename = "state.tv"	#the file were the state is saved
	def __init__( self ):
		MediaDeviceState.__init__( self )
		self.channelHash = ''
		self.frequency = 0
		self.service_id = 0
		self.mute = False
		self.speedDials = {}	#it's a dictionary {index, channel_hash}
		self.volume = 0
		self.brightness = 50
		self.contrast = 50
		self.device = 'dvb-t:// :frequency={0} :adapter=0 :bandwidth=8' #'v4l2:///dev/video0'
				
	def SetMute( self, mute ):
		self.mute = mute
		self.Save()
		
	def SetSpeedDial( self, index ):
		self.speedDials[index] = self.channelHash
		self.Save()
	
	def DelSpeedDial( self, index ):
		del self.speedDials[index]
		self.Save()
		
	def Load( self ):
		if( not os.path.isfile( TVState.Filename ) ):
			return
		with open( TVState.Filename, mode='r' ) as f:
			self.__dict__ = json.load( f )
		#~ print( self.speedDials )
	
	def Save(self):
		with open( TVState.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )
	
	def TunedChannelIs( self, channel ):
		'''FrequencyObserver'''
		self.channelHash = channel.Hash()
		self.frequency = channel.frequency
		self.service_id = channel.service_id
		self.Save()
		
	def VolumeIs( self, volume ):
		self.volume = volume
		self.Save()
		
	def Report( self ):
		print( 'Tuned to {0} Hz, service id:{}, channel_hash:{}'.format( self.frequency, self.service_id, self.channelHash ) )

if __name__ == "__main__":
    s = State()
    s.Save()
