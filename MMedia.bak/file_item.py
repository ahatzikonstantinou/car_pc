#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging

from custom_controls.mmedia_list import *

class FileItem( MMediaListItem ):
	FOLDER_TYPE = 0
	FILE_TYPE = 1
	def __init__( self, name, file_type, text = None, is_enabled = True, is_playlist = False ):
		if( text is None ):
			text = os.path.basename( os.path.normpath( name ) )
		MMediaListItem.__init__( self, name, text, is_enabled, is_playlist )
		self.name = name
		self.file_type = file_type
		
	def IsDir( self ):
		logging.debug( 'FileItem.IsDir...' )
		return os.path.isdir( self.name )
		
	def DumpStr( self ):
		return 'name: {}, file_type:{}, text:{}, is_enabled:{}, is_playlist:{}'.format( self.name, self.file_type, self.Text(), self.is_enabled, self.is_playlist )
