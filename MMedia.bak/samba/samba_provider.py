#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import glib, gio, gobject			
import os
import csv
import time
from threading import *

__all__ = [ 'SambaItem', 'SambaAuthentication', 'SambaProvider', 'SambaAutomountThread' ]

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

DOMAIN = 'WORKGROUP'
USERNAME = 'antonis'
PASSWORD = '312ggp12'

gobject.threads_init()

class SambaItem:
	UNKNOWN = 0
	SHORTCUT = 1
	SHARE = 2
	DIRECTORY = 3
	FILE = 4
	def __init__( self, name, uri, item_type, authentication, gio_file ):
		self.name = name
		self.uri = uri
		self.item_type = item_type
		self.authentication = authentication
		self.gio_file = gio_file
		
	@staticmethod
	def _Gio_To_SambaItemType( gio_file_type ):
		if( gio_file_type == gio.FILE_TYPE_SHORTCUT ):
			return SambaItem.SHORTCUT
		elif( gio_file_type == gio.FILE_TYPE_MOUNTABLE ):
			return SambaItem.SHARE
		elif( gio_file_type == gio.FILE_TYPE_DIRECTORY ):
			return SambaItem.DIRECTORY
		elif( gio_file_type == gio.FILE_TYPE_REGULAR ):
			return SambaItem.FILE
		else:
			return SambaItem.UNKNOWN
		
	def ToAutomount( self ):
		return SambaAutomount( path = self.uri, samba_authentication = self.authentication )
		
class SambaAuthentication:
	def __init__( self, domain = '', username = '', password = '' ):
		self.domain = domain
		self.username = username
		self.password = password
		
	def ToList( self ):
		return [ self.domain, self.username, self.password ]
		
class SambaAutomount:
	DEBUG = False
	Filename = "samba_automounts.csv"
	def __init__( self, path, samba_authentication ):
		self.path = path
		self.samba_authentication = samba_authentication
		
	@staticmethod
	def LoadList( filename = None ):
		automounts_list = {}
		if( filename is None ):
			filename = SambaAutomount.Filename
		if( os.path.isfile( filename ) ):
			with open( filename, "rb") as csv_file:
				reader_list = csv.reader( csv_file )
				mounts_list = []
				mounts_list.extend(reader_list)
				for data in mounts_list:
					if( SambaAutomount.DEBUG ):
						logging.debug( 'read {}'.format( data ) )
					am = SambaAutomount( data[0], SambaAuthentication( data[1], data[2], data[3] ) )
					automounts_list[ data[0] ] = am
			
		return automounts_list
	
	@staticmethod		
	def SaveList( automounts_list, filename = None ):
		if( filename is None ):
			filename = SambaAutomount.Filename
		#if( not os.path.isfile( filename ) ):
			#logging.debug( '{} is not a file, will not save'.format( filename ) )
			#return
			
		if( SambaAutomount.DEBUG ):
			logging.debug( 'will save automounts in {}'.format( filename ) )
		with open( filename, 'w' ) as csv_file:
			writer = csv.writer( csv_file )
			for key,item in automounts_list.iteritems():
				if( SambaAutomount.DEBUG ):
					logging.debug( 'saving automount {}'.format( item.path ) )
				writer.writerow( [ item.path ] + item.samba_authentication.ToList() )
		
class SambaProvider:
	DEBUG = False
	def __init__( self, domain, username = None, password = None ):
		self.authentication = SambaAuthentication( domain, username, password )
		self.mount_finished_observers = []
		self.automount_list = SambaAutomount.LoadList()

	def Browse( self, directory = None ):
		samba_items = [] #list of SambaItem
		prefix =  'smb://'
		filename = prefix
		if( directory ):
			filename = '{}{}'.format( ( prefix if not directory.startswith( prefix ) else '' ), directory )
		#strange bug, I get uri's like smb:///
		filename = filename.replace( 'smb:///', 'smb://' )
		if( SambaProvider.DEBUG ):
			logging.debug( 'Browsing dir {}'.format( filename ) )			
		try:
			f = gio.File( filename )
			infos = f.enumerate_children('standard::name,standard::type, standard::size')
			
			for info in infos:
				child = f.get_child(info.get_name())
				child_type = info.get_file_type() #'other'
				si = SambaItem( info.get_name(), child.get_path(), SambaItem._Gio_To_SambaItemType( info.get_file_type() ), self.authentication, child )
				if info.get_file_type() == gio.FILE_TYPE_DIRECTORY:
					child_type = 'directory'
				elif( info.get_file_type() == gio.FILE_TYPE_MOUNTABLE ):
					child_type = 'mountable'
					si.uri = '{}/{}'.format( filename, info.get_name() )
				if( SambaProvider.DEBUG ):				
					logger.debug( '\t\t\t{}, uri:{} ({})'.format( si.name, si.uri, child_type ) )
				samba_items.append( si )
		except Exception as ex:
			if( hasattr( ex, 'code' ) and ex.code == gio.ERROR_NOT_MOUNTED ):
				#self.Mount( f )
				pass
			else:
				import traceback; traceback.print_exc()
			pass

		return samba_items
				
	def Mount( self, f ):
		if( SambaProvider.DEBUG ):
			logger.debug( 'will try to mount {}'.format( f.get_uri() ) )
		op = gio.MountOperation()
		op.connect( 'ask-password', self.AskPasswordCb )
		f.mount_enclosing_volume( op, self.MountDoneCb )

	def AskPasswordCb( self, op, message, default_user, default_domain, flags ):
		op.set_username( self.authentication.username )
		op.set_domain( self.authentication.domain )
		op.set_password( self.authentication.password )
		op.reply( gio.MOUNT_OPERATION_HANDLED )

	def MountDoneCb( self, obj, res ):
		#logger.debug( 'finished with res:{}'.format( dir( res ) ) )
		#import pprint; pprint.pprint( dir( res ) )
		#import pprint; pprint.pprint( obj )
		#return
		#print( dir( obj ) )
		#print( obj.get_parse_name() )
		#print( obj.get_uri() )
		#if( self.DEBUG ):
			#filename = obj.get_uri()
			#if( filename.startswith( 'smb://' ) ):
				#filename = filename[6:]
			#self.Browse( filename )
		#pass
		try:
			success = obj.mount_enclosing_volume_finish( res )
			self.UpdateMountFinishedObserver( success )
		except:
			#import traceback; traceback.print_exc()
			self.UpdateMountFinishedObserver( False )
		
	def AddMountFinishedObserver( self, observer ):
		self.mount_finished_observers.append( observer )
		
	def UpdateMountFinishedObserver( self, success ):
		for o in self.mount_finished_observers:
			o.MountFinished( success )
			
	def AddAutomount( self, samba_automount ):
		if( SambaProvider.DEBUG ):
			logging.debug( 'will add mount {}'.format( samba_automount.path ) )
		self.automount_list[ samba_automount.path ] = samba_automount
		SambaAutomount.SaveList( self.automount_list )
		
	def RemoveAutomount( self, samba_automount ):
		if( SambaProvider.DEBUG ):
			logging.debug( 'will remove mount {}'.format( samba_automount.path ) )
		if( self.automount_list.has_key( samba_automount.path ) ):
			del self.automount_list[ samba_automount.path ]
			SambaAutomount.SaveList( self.automount_list )
		
	def GetAutomount( self, path ):
		if( self.automount_list.has_key( path ) ):
			return self.automount_list[ path ]
		
		return None
		
	def _GetSharesRecursive( self, parent_dir = None ):
		shares = {}
		dir_name = ( parent_dir if parent_dir else '' )
		for si in self.Browse( dir_name ):
			if( SambaProvider.DEBUG ):
				logger.debug( si.name )
			if( si.item_type == SambaItem.SHARE ):
				shares[ si.uri ] = si
			new_shares = self._GetSharesRecursive( si.name )
			for key,sh in new_shares.iteritems():
				shares[ key ] = sh
		return shares
			
	def MonitorAutomounts( self ):
		while( True ):
			if( SambaProvider.DEBUG ):
				logging.debug( '------' ) 
				logging.debug( 'Will _GetSharesRecursive...' )
			shares = self._GetSharesRecursive()
			if( SambaProvider.DEBUG ):
				logging.debug( '\tgot {} shares'.format( len( shares ) ) )
			for key, sh in shares.iteritems():
				if( SambaProvider.DEBUG ):
					logging.debug( '\tGot share {}'.format( key ) )
				if( self.automount_list.has_key( key ) ):
					if( SambaProvider.DEBUG ):
						logging.debug( '\tFound automount share {}!'.format( key ) )
					automount = self.automount_list[ key ]
					try:
						f = gio.File( key )
						if( not f.query_exists() ):
							self.authentication = automount.samba_authentication
							self.Mount( f )
					except:
						if( SambaProvider.DEBUG ):
							logger.debug( 'Failed to mount automount {}'.format( key ) )
			time.sleep( 2 )
	
class SambaAutomountThread( Thread ):
	def __init__( self, samba_provider ):
		self.samba_provider = samba_provider
		Thread.__init__(self)
		self.setDaemon(1)
		self.start()
		
	def run( self ):
		self.samba_provider.MonitorAutomounts()
	
def mount_mountable(f):
	op = gio.MountOperation()
	op.connect('ask-password', ask_password_cb)
	f.mount_mountable( op, mount_mountable_done_cb )
	
def mount_mountable_done_cb(obj, res):
	try:
		f = obj.mount_mountable_finish( res )
		if( not f ):
			logger.error( 'An error occured mounting {}'.format( obj.get_basename() ) )
		else:
			logger.debug( 'finished mount_mountable for: {}'.format( f.get_basename() ) )		
			browse( obj )
	except gio.Error, e:
		logger.error( 'Error code:{}, {}'.format( e.code, e ) )
		if( e.code == gio.ERROR_ALREADY_MOUNTED ):
			logger.debug( '{} is already mounted and will eject'.format( obj.get_basename() ) )
			obj.eject_mountable( eject_done )
	except:
		import traceback; traceback.print_exc()
def eject_done( obj, res ):
	logger.log( 'Eject of {} finished {}'.format( obj.get_basename(), ( 'succesfully' if obj.eject_mountable_finish( res ) else 'unsuccessfully' ) ) )
	
def browse( f ):
	import pprint; pprint.pprint( f )
	#mnt = f.find_enclosing_mount()
	#if( not mnt ):
		#mount( f )
	try:
		infos = f.enumerate_children('standard::name,standard::type' )#,standard::size')
	except Exception as ex:
		logger.debug( '{} has no children'.format( f.get_basename() ) )
		logger.debug( 'The exception is {} (exception code: {}, gio.ERROR_NOT_MOUNTED:{}, code == ERROR_NOT_MOUNTED is {} )'.format( ex, ex.code, gio.ERROR_NOT_MOUNTED, ex.code == gio.ERROR_NOT_MOUNTED ) )
		if( ex.code == gio.ERROR_NOT_MOUNTED ):
			mount( f )
			return
		import traceback; traceback.print_exc()
		return
		
	for info in infos:
		logger.debug( '\t\t\t:{} ({})'.format( info.get_name(), info.get_file_type() ) )
		child = f.get_child(info.get_name())
		logger.debug( 'child: {}'.format( child ) )
		if info.get_file_type() == gio.FILE_TYPE_DIRECTORY:
			print( '\t\t\tdir:{} ({})'.format( info.get_name(), info.get_file_type() ) )
		elif( info.get_file_type() == gio.FILE_TYPE_MOUNTABLE ):
			logger.debug( '\tthis is a FILE_TYPE_MOUNTABLE' )
			continue
			try:
				mount_mountable( child )
				#mount( child )
				#browse( child )
			except Exception as e:
				logger.debug( 'got exception e: {}'.format( e ) )
				if( e.code == gio.ERROR_ALREADY_MOUNTED ):
					logger.debug( '{} is already mounted and will eject'.format( info.get_name() ) )
					child.eject_mountable( eject_done )
				else:
					import traceback; traceback.print_exc()
		else:
			print( '\t\t\tfile:{} ({})'.format( info.get_name(), info.get_file_type() ) )
				
def TryGio( arg = None ):
	gobject.threads_init()
	logger.debug( '\n--- Now trying gio for "{}"---'.format( arg ) )		
	#filename = "smb:///{}/".format( 'network' )
	#filename = "smb:///{}/".format( '192.168.1.4' )
	#filename = "smb://"
	#filename = "smb://WORKGROUP"
	#filename = "smb://HOMEPC"
	filename = "smb://"
	if( arg ):
		filename += arg
	logging.debug( 'Browsing dir {}'.format( filename ) )
	fh = gio.File( filename )
	#mount( fh )
	browse( fh )
	glib.MainLoop().run()

#import sys; 
#TryGio( ( sys.argv[1] if len( sys.argv ) > 1 else None ) )
#print( len( sys.argv ) )
#sys.exit(0)

if( __name__ == '__main__' ):
	import sys; 
	
	def BrowseAll( sp, parent_dir = None, current_dir = None ):
		dir_name = '{}{}{}'.format( ( parent_dir if parent_dir else '' ), ( '/' if parent_dir else '' ), ( current_dir.name if current_dir else '' ) )
		for si in sp.Browse( dir_name ):
			logger.debug( si.name )
			BrowseAll( sp, dir_name, si )
		
	sp = SambaProvider( DOMAIN, USERNAME, PASSWORD )
	filename = ( sys.argv[1] if len( sys.argv ) > 1 else None )
	#sp.Browse( filename )
	BrowseAll( sp, filename )
	glib.MainLoop().run()
