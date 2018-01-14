#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import logging
from lxml import etree

from lib.miranda import *
#from et import parse_xml as et_parse_xml
import lib.DIDLLite as DIDLLite

class UPnPObserver:
	ON_ADD = 0
	ON_REMOVE = 1
	def __init__( self, device, callback, on_action ):
		if( on_action not in [ UPnPObserver.ON_ADD, UPnPObserver.ON_REMOVE ] ):
			raise Exception( 'Invalid on_action {} for UPnPObserver. Allowed values ON_ADD:{}, ON_REMOVE:{}'.format( UPnPObserver.ON_ADD, UPnPObserver.ON_REMOVE ) )
		self.device = device
		self.callback = callback
		self.on_action = on_action
			
class UPnPProvider:
	'''
	Note: It looks like media servers and other UPNP devices send Notifications (Gateway devices) 
	or 200 ok responses (MediaServer devices) every ~33 seconds
	'''
	DEBUG = False
	REMOVE_HOST_NORESPONSSECS = 60
	NORESPONSE_TICKSECS = 10
	SEARCH_SECS = 15
	
	def __init__( self, search_secs = SEARCH_SECS, noresponse_ticksecs = NORESPONSE_TICKSECS, remove_host_noresponssecs = REMOVE_HOST_NORESPONSSECS ):
		self._upnp = upnp( 
			False, 
			False, 
			None,
			HostAddedCallback = self.HostAdded,
			HostRemovedCallback = self.HostRemoved,
			DeviceAddedCallback = self.DeviceAdded,
			DeviceRemovedCallback = self.DeviceRemoved,
			acceptable_devices = [ 'MediaServer' ],
			#knownHeaders = { 'HTTP/1.1 200 OK' : 'reply' }, #only replies to our request are acceptable
			max_noresponse_secs = remove_host_noresponssecs
		)
		self._search_secs = search_secs
		self._noresponse_ticksecs = noresponse_ticksecs
		
		self.hosts = {}
		
		self._observers = []
		
		#prepare request and server 
		st = 'urn:schemas-upnp-org:device:MediaServer:{}'.format( self._upnp.UPNP_VERSION.split('.')[0] )
		#Build the request
		self._request = 	"M-SEARCH * HTTP/1.1\r\n"\
				"HOST:%s:%d\r\n"\
				"ST:%s\r\n" % ( self._upnp.ip, self._upnp.port, st )
		for header,value in self._upnp.msearchHeaders.iteritems():
				self._request += header + ':' + value + "\r\n"	
		self._request += "\r\n" 

		logging.info( "Entering discovery mode for '{}'.".format( st ) )
			
		#Have to create a new socket since replies will be sent directly to our IP, not the multicast IP
		self._server = self._upnp.createNewListener( '', self._upnp.port )
		if self._server == False:
			logging.error( 'Failed to bind port {}'.format( self._upnp.port ) )
			return
		
	def Start( self ):
		MSearchShoutThread( self._upnp, self._server, self._search_secs, self._request )
		MSearchListenThread( self._upnp, self._server )
		NoResponseThread( self._upnp, self._noresponse_ticksecs )
		
	def HostAdded( self, hostname ):
		if( self.DEBUG ):
			logging.info( 'Host: {} was added to the list of active hosts'.format( hostname ) )
		
	def HostRemoved( self, hostname ):		
		if( self.DEBUG ):
			logging.info( 'Host: {} was removed from the list of active hosts'.format( hostname ) )
		
	def DeviceRemoved( self, hostname, device_name ):
		for o in [ x for x in self._observers if x.on_action == UPnPObserver.ON_REMOVE and x.device == device_name ]:
			o.callback( hostname, device_name )
		
	def DeviceAdded( self, hostInfo, device_name ):
		for o in [ x for x in self._observers if x.on_action == UPnPObserver.ON_ADD and x.device == device_name ]:
			o.callback( self._upnp, hostInfo, device_name )
		
	def AddDeviceAddedObserver( self, device, UpdateCallback ):
		self._observers.append( UPnPObserver( device, UpdateCallback, UPnPObserver.ON_ADD ) )
		
	def AddDeviceRemovedObserver( self, device, UpdateCallback ):
		self._observers.append( UPnPObserver( device, UpdateCallback, UPnPObserver.ON_REMOVE ) )
		
class NoResponseThread( threading.Thread ):
	DEBUG = False
	def __init__( self, upnp, no_response_tick_secs ):
		self._upnp = upnp
		self._no_response_tick_secs = no_response_tick_secs
		threading.Thread.__init__( self )
		self.setDaemon( True )
		self.start()
		
	def run( self ):
		while True:
			time.sleep( self._no_response_tick_secs )
			if( self.DEBUG ):
				logging.debug( 'calling NoResponseTick' )
			self._upnp.NoResponseTick()

class MSearchListenThread( threading.Thread ):
	def __init__( self, upnp, server ):
		self._upnp = upnp
		self._server = server
		threading.Thread.__init__( self )
		self.setDaemon( True )
		self.start()
		
	def run( self ):
		while True:
			try:
				if( self._upnp.parseSSDPInfo( self._upnp.recv( 1024, self._server ), False, False ) ):
					if( self.DEBUG ):
						logging.debug( 'Got a host' )
				#else:
					#logging.debug( 'Got something unacceptable' )
				time.sleep( 0.1 )					
			except Exception, e:
				pass

class MSearchShoutThread( threading.Thread ):
	def __init__( self, upnp, server, search_interval_secs, request ):
		threading.Thread.__init__( self )
		self._upnp = upnp
		self._server = server
		self._search_interval_secs = search_interval_secs
		self._request = request
		self.setDaemon( True )
		self.start()
		
	#Actively search for UPNP devices
	def run( self ):
		while True:
			try:
				self._upnp.send( self._request, self._server )
				if( self.DEBUG ):
					logging.debug( 'Shouting for hosts...' )
				time.sleep( self._search_interval_secs )
			except Exception, e:
				logging.info( '\nDiscover mode halted...' )
				break

def BrowseMediaServer( upnp_proxy, hostInfo, device_name, item_id = '0' ):
	return MediaServerContentDirectory( upnp_proxy, hostInfo, device_name, item_id, browse_flag = 'BrowseDirectChildren', requested_count = '0' )
	
def GetMetadata( upnp_proxy, hostInfo, device_name, item_id ):
	return MediaServerContentDirectory( upnp_proxy, hostInfo, device_name, item_id, browse_flag = 'BrowseMetadata', requested_count = '1' )
	
def MediaServerContentDirectory( upnp_proxy, hostInfo, device_name, item_id, browse_flag = 'BrowseDirectChildren', requested_count = 0 ):
	'''
	If successfull returs a list of DIDLLite.DIDLElement objects else returns None
	'''
	logging.debug( 'will browse {} - {}, item_id:{} for {}'.format( hostInfo['name'], device_name, item_id, browse_flag ) )
	try:
		if( not hostInfo['deviceList'][device_name]['services'].has_key( 'ContentDirectory' ) ):
			logging.error( 'This should be a MediaServer but it has no "ContentDirectory" service' )
			return None
		
		if( not hostInfo['deviceList'][device_name]['services']['ContentDirectory'].has_key( 'controlURL' ) ):
			logging.error( 'This should be a MediaServer but the "ContentDirectory" service has no controlURL' )
			return None
			
		#fullServiceName = 'urn:schemas-upnp-org:service:ContentDirectory:1'
		fullServiceName = hostInfo['deviceList'][device_name]['services']['ContentDirectory']['fullName']
		actionName = 'Browse'
		sendArgs = { 
			'ObjectID': ( item_id, 'string', 0 ),
			'BrowseFlag': ( browse_flag, 'string', 1 ),
			'Filter': ( '*', 'string', 2 ),
			'StartingIndex': ( 0, 'ui4', 3 ),
			'RequestedCount': ( requested_count, 'ui4', 4 ),
			'SortCriteria': ( '', 'string', 5 )
		}
		controlURL = hostInfo['proto'] + hostInfo['name']
		controlURL2 = hostInfo['deviceList'][device_name]['services']['ContentDirectory']['controlURL']
		if not controlURL.endswith('/') and not controlURL2.startswith('/'):
			controlURL += '/'
		controlURL += controlURL2
		response = upnp_proxy.sendSOAP( hostInfo['name'], fullServiceName, controlURL, actionName, sendArgs )
		
		def got_result(results):
			items = []
			if results is not None:
				elt = DIDLLite.DIDLElement.fromString(results['Result'])
				items = elt.getItems()
			return items

		def got_process_result(result):
			#print result
			#return
			
			r = {}
			r['number_returned'] = result['NumberReturned']
			r['total_matches'] = result['TotalMatches']
			r['update_id'] = result['UpdateID']
			r['items'] = {}
			elt = DIDLLite.DIDLElement.fromString(result['Result'])
			for item in elt.getItems():
				#print "process_result", item
				i = {}
				i['upnp_class'] = item.upnp_class
				i['id'] =  item.id
				i['title'] =  item.title
				i['parent_id'] =  item.parentID
				if hasattr(item,'childCount'):
					i['child_count'] =  str(item.childCount)
				if hasattr(item,'date') and item.date:
					i['date'] =  item.date
				if hasattr(item,'album') and item.album:
					i['album'] =  item.album
				if hasattr(item,'artist') and item.artist:
					i['artist'] =  item.artist
				if hasattr(item,'albumArtURI') and item.albumArtURI:
					i['album_art_uri'] = item.albumArtURI
				if hasattr(item,'res'):
					resources = {}
					for res in item.res:
						url = res.data
						resources[url] = res.protocolInfo
					if len(resources):
						i['resources']= resources
				r['items'][item.id] = i
			return r
		
		def first_level_dict(t):
			#logging.debug( '----Printing etree-------' )
			d = {}
			for e in list( t ):
				d[e.tag] = e.text
				#logging.debug( '<{}>'.format( e.tag ) )
			#logging.debug( '----Finished printing etree-------' )
			return d
		
		result = got_result( first_level_dict( etree.fromstring( unicode( response ).encode( 'utf-8' ) ).find( '*//{urn:schemas-upnp-org:service:ContentDirectory:1}BrowseResponse' ) ) )
				
		#for l in result:
			#logging.debug( 'class:{}\n\tres:{}, id:{}, refID:{}, server_uuid:{}'.format( l.upnp_class, l.res, l.id, l.refID, l.server_uuid ) )
		return result
	except:
		import traceback, sys; traceback.print_exc()
		logging.error( 'Could not browse host {}'.format( hostInfo['name'] ) )
		return None
	
def RemoveMediaServer( hostname, device_name ):
	logging.debug( 'will remove {} - {}'.format( hostname, device_name ) )

if __name__ == '__main__':
	logging.basicConfig( level = logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' )
	d = UPnPProvider()
	
		
	d.AddDeviceAddedObserver( 'MediaServer', BrowseMediaServer )
	d.AddDeviceRemovedObserver( 'MediaServer', RemoveMediaServer )
	d.Start()
	while True:
		time.sleep( 1 )
