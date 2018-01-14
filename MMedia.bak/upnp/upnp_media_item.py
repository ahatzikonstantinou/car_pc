#!/usr/bin/python
# -*- coding: utf-8 -*-

import lib.DIDLLite
from urlparse import urlparse
import logging

from file_item import *

class UPnPMediaItem( FileItem ):
	def __init__( self, hostname, didllite_object ):
		self.hostname = hostname
		self.didllite_object = didllite_object
		FileItem.__init__( self, 
			name = self.ResGetUrl(), 
			file_type = ( FileItem.FOLDER_TYPE if self.IsDir() else FileItem.FILE_TYPE ), 
			text = self.didllite_object.title,
			is_enabled = True, 
			is_playlist = False
		)

	def IsDir( self ):
		#logging.debug( 'UPnPMediaItem.IsDir...' )
		return ( 'container' in self.didllite_object.upnp_class )
		
	def ParentDir( self ):
		logging.debug( 'UPnPMediaItem.ParentDir: I am {} with id: {} and parentID: {}'.format( self.Text(), self.didllite_object.id, self.didllite_object.parentID ) )
		return 'http://{}/{}'.format( self.hostname, self.didllite_object.parentID )
		
	def ResGetUrl( self ):
		'''
		Will return the url by which the current didllite item may be retrieved from the mediaserver
		'''
		#Note: some mediaservers return object ids for directories with leading '/'.
		#If I also add a '/' beyween the hostname and the id they resulting object "does not exist"
		slash = ( '' if self.didllite_object.id.startswith( '/' ) else '/' )
		get_url = 'http://{}{}{}'.format( self.hostname, slash, self.didllite_object.id )
		#import pprint; pprint.pprint( self.didllite_object.res )
		if( len( self.didllite_object.res ) > 0 ):
			#parsed = urlparse( self.didllite_object.res[0].data )
			#get_url = '{}://{}{}{}'.format( parsed.scheme, parsed.netloc, slash, self.didllite_object.id )
			get_url = self.didllite_object.res[0].data
			#logging.debug( 'UPnPMediaItem.ResGetUrl returning {}'.format( get_url ) )
		return get_url
		
	def IsVideo( self ):
		return 'video' in self.didllite_object.upnp_class
		
	def IsAudio( self ):
		return 'audio' in self.didllite_object.upnp_class
		
	def Dump( self ):
		print( '{}, id:{}, isDir():{}'.format( self.name, self.didllite_object.id, self.IsDir() ) )
		
	def DumpStr( self ):
		return '{}, id:{}, isDir():{}, parent_id:{}, fileItem:[{}]'.format( self.name, self.didllite_object.id, self.IsDir(), self.didllite_object.parentID, FileItem.DumpStr( self ) )
