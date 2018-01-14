#!/usr/bin/python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from coherence.base import Coherence
from coherence.upnp.core import DIDLLite
from coherence.upnp.devices.media_server_client import MediaServerClient

# browse callback
def process_media_server_browse(result, client):
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
			
def check_device(device):
	print "found device %s of type %s - %r" %(device.get_friendly_name(),
											  device.get_device_type(),
											  device.client)
	return
	if( device.get_device_type() == 'urn:schemas-upnp-org:device:MediaServer:1' ):
		client = MediaServerClient( device )
		
		d = client.content_directory.browse(0,
			browse_flag='BrowseDirectChildren', process_result=False,
			backward_compatibility=False)
		d.addCallback(process_media_server_browse, client)
											  
def media_server_found(client, udn):
	print "media_server_found", udn
	print "media_server_found", client
	print "media_server_found", client.device.get_friendly_name()
	
def media_server_removed(udn):
	print "media_server_removed", udn

def completed(self, client, udn):
	print 'sending signal Coherence.UPnP.ControlPoint.%s.detected %r' % (client.device_type, udn)
	
def remove_client(self, udn, client):
	print "remove %s" % (udn)
	
def start():
	config = {'logmode':'warning'}
	c = Coherence(config)
	c.connect( check_device, 'Coherence.UPnP.Device.detection_completed' )
	c.connect( completed, 'Coherence.UPnP.DeviceClient.detection_completed' )
	c.connect( remove_client, 'Coherence.UPnP.Device.remove_client' )
	#c.connect( media_server_found, 'Coherence.UPnP.ControlPoint.MediaServer.detected' )
	#c.connect( media_server_removed, 'Coherence.UPnP.ControlPoint.MediaServer.removed' )

reactor.callWhenRunning(start)
reactor.run()
