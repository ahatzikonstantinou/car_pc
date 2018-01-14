#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
import glib, gio, gobject
import logging

class MountDetector:
	def __init__( self, MountAddedCallback = None, MountRemovedCallback = None ):
		monitor = gio.volume_monitor_get()
		self._MountAddedCallback = MountAddedCallback
		self._MountRemovedCallback = MountRemovedCallback
		monitor.connect( "mount-added", self.MountAdded )
		monitor.connect( "mount-removed", self.MountRemoved )
		
	def MountAdded( self, volume_monitor, mount ):
		print( 'new mount {} was added'.format( mount.get_name() ) )
		#PrintMountInfo( mount )
		if( self._MountAddedCallback ):
			self._MountAddedCallback( mount )

	def MountRemoved( self, volume_monitor, mount ):
		print( 'mount {} was removed'.format( mount.get_name() ) )
		#PrintMountInfo( mount )
		if( self._MountRemovedCallback ):
			self._MountRemovedCallback( mount )
		
	@staticmethod	
	def IsAudioCd( gio_mount ):
		content_type_list = gio_mount.guess_content_type_sync( 0 )
		return( content_type_list and 'x-content/audio-cdda' in content_type_list )
		
	@staticmethod
	def IsSamba( gio_mount ):
		return gio_mount.get_root().has_uri_scheme( 'smb' )
			 
	@staticmethod
	def GetMounts():
		monitor = gio.volume_monitor_get()
		mos = monitor.get_mounts()
		return [ m for m in mos if ( not MountDetector.IsAudioCd( m ) or m.can_eject() ) ]
		
def PrintMountInfo( m ):
	print( '\tName:{}'.format( m.get_name() ) )
	drive = m.get_drive()
	print( '\t\tUIID: {}'.format( m.get_uuid() ) )
	print( '\t\tURI: {}'.format( m.get_root().get_uri() ) )
	print( '\t\tDrive: {}'.format( ( drive.get_name() if drive else 'None' ) ) )
	print( '\t\tRoot: {}'.format( m.get_root().get_path() ) )
	print( '\t\tCan unmount: {}'.format( m.can_unmount() ) )
	print( '\t\tCan eject: {}'.format( m.can_eject() ) )
	print( '\t\tContent type: {}'.format( m.guess_content_type_sync( 0 ) ) )
	current = m.get_root()
	infos = current.enumerate_children('standard::name,standard::type,standard::size')
	for info in infos:
		child = current.get_child(info.get_name())
		if info.get_file_type() == gio.FILE_TYPE_DIRECTORY:
			print( '\t\t\tdir:{}'.format( info.get_name() ) )
		else:
			print( '\t\t\tfile:{}'.format( info.get_name() ) )

class Handler:
	def MountAdded( self, volume_monitor, mount ):
		print( 'new mount {} was added'.format( mount.get_name() ) )
		PrintMountInfo( mount )

	def MountRemoved( self, volume_monitor, mount ):
		print( 'mount {} was removed'.format( mount.get_name() ) )
		#PrintMountInfo( mount )
	
gobject.threads_init()

if __name__ == '__main__':
	#Test
	f = gio.File( 'smb://homepc/cartoons' )
	print( 'scheme of {} is {}'.format( f.get_parse_name(), f.get_uri_scheme() ) )
	print( 'f.has_uri_scheme( smb )={}'.format( f.has_uri_scheme( 'smb' ) ) )
	#import sys; sys.exit(1)
	
	monitor = gio.volume_monitor_get()
	h = Handler()
	monitor.connect( "mount-added", h.MountAdded )
	monitor.connect( "mount-removed", h.MountRemoved )

	print( '--------------' )
	print( 'Drives:' )
	ds = monitor.get_connected_drives()
	for d in ds:
		pprint.pprint( d )
		
	print( '--------------' )
	print( 'Volumes:' )
	vs = monitor.get_volumes()
	for v in vs:
		pprint.pprint( v )
		
	del monitor
		
	print( '--------------' )
	print( 'Mounts:' )	
	#mos = monitor.get_mounts()
	mos = MountDetector.GetMounts()
	for m in mos:
		#pprint.pprint( m )
		PrintMountInfo( m )
		
	glib.MainLoop().run()


