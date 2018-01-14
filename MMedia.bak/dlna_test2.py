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

# called for each media server found
def media_server_found(client, udn):
	print "media_server_found", udn
	print "media_server_found", client
	print "media_server_found", client.device.get_friendly_name()
	
	d = client.content_directory.browse(0,
			browse_flag='BrowseDirectChildren', process_result=False,
			backward_compatibility=False)
	d.addCallback(process_media_server_browse, client)

# sadly they sometimes get removed as well :(
def media_server_removed(udn):
	print "media_server_removed", udn

def start():
	control_point = ControlPoint(Coherence({'logmode':'warning'}),
			auto_client=['MediaServer'])
	control_point.connect(media_server_found,
			'Coherence.UPnP.ControlPoint.MediaServer.detected')
	control_point.connect(media_server_removed,
			'Coherence.UPnP.ControlPoint.MediaServer.removed')

if __name__ == "__main__":
	reactor.callWhenRunning(start)
	reactor.run()
