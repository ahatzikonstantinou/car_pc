#!/usr/bin/python
# -*- coding: utf-8 -*-

#VERY IMPORTANT NOTE:
#python package coherence has a bug that needs to be fixed (a missing attribute in class HeaderAwareHTTPClientFactory)
#file /usr/share/pyshared/coherence/upnp/core/utils.py 
#needs to have the following lines inserted in line 546
#        # Fixes Twisted 11.1.0+ support as HTTPClientFactory is expected
#        # to have _disconnectedDeferred. See Twisted r32329.
#        # As Scrapy implements it's own logic to handle redirects is not
#        # needed to add the callback _waitForDisconnect.
#        # Specifically this avoids the AttributeError exception when
#        # clientConnectionFailed method is called.
#        self._disconnectedDeferred = defer.Deferred()

from twisted.internet import reactor

from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
from coherence.upnp.core import DIDLLite
from coherence.upnp.devices.media_server_client import MediaServerClient

import time

class DLNADetector:
	'''
	After trying the dlna_tests I found out that coherence does not generate proper
	'Coherence.UPnP.ControlPoint.MediaServer.detected' messages. Instead the only reliable
	way is to use Coherence.connect( f, 'Coherence.UPnP.Device.detection_completed' )
	to detect new media servers. This event fires twice. The first time the client arg is None, 
	and the second time it is an actual object.
	Use ControlPoint.connect(f,'Coherence.UPnP.ControlPoint.MediaServer.removed') to
	detect removal of a media server (which gets a 400, 412 or 404 error when trying 'unsubscribe')
	'''
	def __init__( self ):
		self._config = {'logmode':'warning'}
		self._coherence = Coherence( self._config )
		self._control_point = ControlPoint( self._coherence, auto_client=['MediaServer'] )
		
	def Start( self ):
		reactor.callWhenRunning( self.start )
		reactor.run()
	
	# browse callback
	def process_media_server_browse(self, result, client):
		print "browsing root of", client.device.get_friendly_name()
		print "result contains %d out of %d total matches" % \
				(int(result['NumberReturned']), int(result['TotalMatches']))

		elt = DIDLLite.DIDLElement.fromString(result['Result'])
		for item in elt.getItems():

			if item.upnp_class.startswith("object.container"):
				print "  container %s (%s) with %d items" % \
						(item.title,item.id, item.childCount)

			if item.upnp_class.startswith("object.item"):
				print "  item %s (%s)" % (item.title, item.id)

	# called for each media server found
	def media_server_found(self, client, udn):
		print "media_server_found", udn
		print "media_server_found", client
		print "media_server_found", client.device.get_friendly_name()
		#return
		d = client.content_directory.browse(0,
				browse_flag='BrowseDirectChildren', process_result=True,
				backward_compatibility=True)
		d.addCallback( self.process_media_server_browse, client )

	def check_device( self, device):
		print "found device %s of type %s - %r" %(device.get_friendly_name(),
												  device.get_device_type(),
												  device.client)
		client = device.client
		if( not client is None and type( client ) ==  MediaServerClient ):
			d = client.content_directory.browse(0,
				browse_flag='BrowseDirectChildren', process_result=False,
				backward_compatibility=False)
			d.addCallback( self.process_media_server_browse, client )
												  
	# sadly they sometimes get removed as well :(
	def media_server_removed( self, udn ):
		print "media_server_removed", udn
		#print( 'Due to buggy coherence behaviour I will reset DLNADetector' )
		#self.reset()

	def start( self ):
		#pass
		#self._coherence.connect( self.check_device, 'Coherence.UPnP.Device.detection_completed' )
		self._control_point.connect( self.media_server_found, 'Coherence.UPnP.ControlPoint.MediaServer.detected' )
		#self._control_point.connect( self.media_server_removed, 'Coherence.UPnP.ControlPoint.MediaServer.removed' )
	
	def reset( self, results ):
		if( self._control_point ):
			try:
				self._control_point.disconnect( self.media_server_removed, 'Coherence.UPnP.ControlPoint.MediaServer.removed' )
			except:
				print( "Error disconnecting 'Coherence.UPnP.ControlPoint.MediaServer.removed'" )
			try:
				del self._control_point
			except:
				print( 'Error deleting self._control_point' )
				
		if( self._coherence ):
			try:
				self._coherence.disconnect( self.check_device, 'Coherence.UPnP.Device.detection_completed' )
			except:
				print( "Error disconnecting 'CCoherence.UPnP.Device.detection_completed'" )
			try:
				del self._coherence
			except:
				print( 'Error deleting self._coherence' )
		
		self.__init__()
		self.Start()
		print( 're-inited DLNADetector' )

if __name__ == "__main__":
	#reactor.callWhenRunning(start)
	#reactor.run()

	d = DLNADetector()
	d.Start()
	#print( 'will reset DLNADetector' )
	#dl = d._coherence.shutdown()
	#dl.addCallback( d.reset )
