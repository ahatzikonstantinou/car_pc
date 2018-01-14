#!/usr/bin/python
# -*- coding: utf-8 -*-

from custom_controls import MMediaListItem

class RadioStationMediaListItem( MMediaListItem ):
	def __init__( self, frequency, name ):
		MMediaListItem.__init__( self, hash = frequency, text = name )

	def Text( self ):
		return '{} MHz - {}'.format( self._hash, self._text )
