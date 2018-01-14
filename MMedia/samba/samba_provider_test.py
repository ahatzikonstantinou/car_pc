#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import smbc
import glib, gio, gobject			

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

DOMAIN = 'WORKGROUP'
USERNAME = 'antonis'
PASSWORD = '312ggp12'

def mount(f):
	op = gio.MountOperation()
	op.connect('ask-password', ask_password_cb)
	f.mount_enclosing_volume(op, mount_done_cb)
	
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

def ask_password_cb(op, message, default_user, default_domain, flags):
	op.set_username(USERNAME)
	op.set_domain(DOMAIN)
	op.set_password(PASSWORD)
	op.reply(gio.MOUNT_OPERATION_HANDLED)

def mount_done_cb(obj, res):
	#logger.debug( 'finished with res:{}'.format( dir( res ) ) )
	#import pprint; pprint.pprint( dir( res ) )
	#import pprint; pprint.pprint( obj )
	#return
	#obj.mount_enclosing_volume_finish(res)
	browse( obj )
	pass
	
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
				
def long2net(arg):
	if (arg <= 0 or arg >= 0xFFFFFFFF):
		raise ValueError("illegal netmask value", hex(arg))
	return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

def to_CIDR_notation(bytes_network, bytes_netmask):
	network = scapy.utils.ltoa(bytes_network)
	netmask = long2net(bytes_netmask)
	net = "%s/%s" % (network, netmask)
	if netmask < 16:
		logger.warn("%s is too big. skipping" % net)
		return None

	return net

def scan_and_print_neighbors(net, interface):
	logger.info("arping %s on %s" % (net, interface))
	ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=1, verbose=True)
	for s, r in ans.res:
		line = r.sprintf("%Ether.src% %ARP.psrc%")
		try:
			hostname = socket.gethostbyaddr(r.psrc)
			line += " " + hostname[0]
		except socket.herror:
			# failed to resolve
			pass
		logger.info(line)

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

class SMBCProvider:
	DOMAIN = ''
	USERNAME = 'antonis'
	PASSWORD = '312ggp12'
	def __init__( self ):
		self.domain = DOMAIN
		self.username = USERNAME
		self.password = PASSWORD
		self.ctx = smbc.Context( auth_fn = self.my_auth_callback_fn, debug=0 )
		#self.ctx = smbc.Context()
		self.ctx.optionNoAutoAnonymousLogin = True
		
	def my_auth_callback_fn( self, server, share, workgroup, username, password ):
		logger.debug( 'server:{}, share:{}, workgroup:{}, username:{}, password:{}'.format( server, share, workgroup, username, password ) )
		logger.debug( 'returning ( {}, {}, {} )'.format( workgroup, self.username, self.password ) )
		return ( workgroup, self.username, self.password )
		
	def SMBCDir( self, ctx, samba_path, tabs ):
		try:
			logger.debug( 'will open path {}'.format( samba_path ) )
			entries = self.ctx.opendir( samba_path ).getdents()
			logger.debug( 'got {} entries'.format( len( entries ) ) )
			tabs = '{}{}'.format( tabs, '\t' )
			for entry in entries:
				#vlc_uri = 'smb://{}:{}@{}/{}/{}'.format( self.username, self.password, server, directory_path, entry.name )
				path = samba_path
				#logger.debug( 'smbc_type:{}, comment:{}, name:{}'.format( entry.smbc_type, entry.comment, entry.name ) )
				if( entry.smbc_type == 1 ):	#domain
					logger.debug( 'setting DOMAIN, was {}, is {}'.format( self.domain, entry.name ) )
					self.domain = entry.name
					path = 'smb://{}'.format( self.domain )
				if( entry.smbc_type == 2 ): #server
					logger.debug( 'setting server to {}'.format( entry.name ) )
					server = entry.name
					path = 'smb://{}'.format( server )
				if( entry.smbc_type in [ 3, 7 ] ): #dir
					path = '{}/{}'.format( samba_path, entry.name )
					#logger.debug( 'will go deeper to {}'.format( path ) )
				if( entry.smbc_type in [ 1, 2, 3 ] ):#, 7 ] ):
					self.SMBCDir( ctx, path, tabs )
				logger.debug( 'smbc_type:{}, path:{}, comment:{}, name:{}'.format( entry.smbc_type, path, entry.comment, entry.name ) )

		except:
			import traceback; traceback.print_exc()
			logger.error( 'Failed' )

	def Start( self ):
		try:
			logger.debug( '\n--- Now trying smbc ---' )
			
			path = "smb://"
			#path = 'smb://HOMEPC/movies-vfat'
			#path ='smb://HOMEPC/movies-vfat/Covert.One.The.Hades.Factor.DVDRip.XviD/CD1'
			#entries = ctx.opendir( samba_path ).getdents ()
			#for entry in entries:
				#logger.info( 'comment:{}, name:{}, smbc_type:{}'.format( entry.comment, entry.name, entry.smbc_type ) )
			self.SMBCDir( self.ctx, path, '' )
			logger.debug( '\n--- Finished smbc ---' )
		except:
			import sys, traceback; logger.error( traceback.format_exception( *sys.exc_info() ) )		

#sp = SMBCProvider()
#sp.Start()
import sys; 
TryGio( ( sys.argv[1] if len( sys.argv ) > 1 else None ) )
#print( len( sys.argv ) )
sys.exit(0)

for route in scapy.config.conf.route.routes:

	network = route[0]
	netmask = route[1]
	interface = route[3]
	logger.debug( 'Doing {}/{} on {} (route[4]:{})'.format( network, netmask, interface, route[4] ) )

	# skip loopback network and default gw
	if network == 0 or interface == 'lo' or route[4] == '127.0.0.1' or route[4] == '0.0.0.0' :
		continue

	if netmask <= 0 or netmask == 0xFFFFFFFF:
		continue

	net = to_CIDR_notation(network, netmask)
	
	if net == '169.254.0.0/16':
		logger.debug( "skipping microsoft's link-local IPv4 {} Automatic Private Internet Protocol Addressing (APIPA)".format( net ) )
		continue

	if interface != scapy.config.conf.iface:
		# see http://trac.secdev.org/scapy/ticket/537
		logger.warn("skipping %s because scapy currently doesn't support arping on non-primary network interfaces", net)
		continue

	if net:
		scan_and_print_neighbors(net, interface)
