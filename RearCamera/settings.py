#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import wx
import pprint

class Settings:
	'''These are the settings of the viewer'''

	Filename = 'settings.camera' #the file were the settings are saved

	def __init__( self ):
		self.radioDevice = 'v4l2:///dev/video0'

	def Load( self ):
		with open( Settings.Filename, mode='r' ) as f:
			settingsDict = {}
			self.__dict__ = json.load( f )

	def Save(self):
		with open( Settings.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2 )
        
        
if __name__ == "__main__":
    s = Settings()
    s.Load()
    #json.dumps( s.__dict__, indent=2 )
    pprint.pprint( s.radioDevice )
    s.Save()
