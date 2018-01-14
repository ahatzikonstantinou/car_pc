#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
from media_device import *
from error_reporter import *
from message_reporter import *

class DeviceList:
	
	Filename = "devices_list.csv"
	def __init__( self, dev_media_functions, mmedia_gui, error_reporter = None, message_reporter = None, GetSelectedSystemPlaylistItemsCallback = None, playerLock = None ):#, playlist_select_callback = None ):
		self._dev_media_functions = dev_media_functions
		self._mmedia_gui = mmedia_gui
		self._error_reporter = error_reporter
		self._message_reporter = message_reporter
		self._GetSelectedSystemPlaylistItems = GetSelectedSystemPlaylistItemsCallback
		self._playerLock = playerLock
		#self._playlist_select_callback = playlist_select_callback
		self.devices = []
		
	def Load( self, filename = None ):
		if( not os.path.isfile( DeviceList.Filename ) ):
			return
			
		if( filename is None ):
			filename = DeviceList.Filename
		reader_list = csv.reader( CommentedFile( open( filename, "rb") ) )
		device_list = []
		device_list.extend(reader_list)
		for data in device_list:
			device = MediaDevice( mmedia_gui = self._mmedia_gui, gui_media_functions = self._dev_media_functions, error_reporter=self._error_reporter, message_reporter = self._message_reporter, playerLock = self._playerLock, GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItems, )#, playlist_select_callback=self._playlist_select_callback )
			device.name = data[0].strip().strip( '\'"')
			device.dev_path = data[1].strip().strip( '\'"')
			device.dev_type = MediaDevice.StrToType( data[2].strip().strip( '\'"') )
			print( device.name + ' - ' + device.dev_path + ' : ' + str( device.dev_type ) )
			self.devices.append( device )
			#print( 'device is {0}'.format( device.__class__.__name__ ) )
			
#from http://www.mfasold.net/blog/2010/02/python-recipe-read-csvtsv-textfiles-and-ignore-comment-lines/
#to skip comment lines use a file decorator

class CommentedFile:
	def __init__(self, f, commentstring="#"):
		self.f = f
		self.commentstring = commentstring
	def next(self):
		line = self.f.next()
		while line.startswith(self.commentstring):
			line = self.f.next()
		return line
	def __iter__(self):
		return self
		
if __name__ == '__main__':
	l = DeviceList()
	l.Load()
