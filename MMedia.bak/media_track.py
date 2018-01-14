#!/usr/bin/python
# -*- coding: utf-8 -*-

import random #for testing only
			
class MediaTrack:
	'''This is required to at least return its hash so that the device
		 and the media player will be able to pass it to each other
	'''
	def __init__( self, hash='', text='' ):
		self._hash = hash #.encode('utf-8', 'ignore')
		self._text = text #.encode('utf-8', 'ignore')
		
	def Hash( self ):
		return self._hash
		#return random.randint( 1000, 2000 ) #for testing only

	def Text( self ):
		return self._text
		
	def Dump( self ):
		print( 'Hash: {}, Text: {}'.format( self._hash, self._text ) )
