#!/usr/bin/python

import sys
import dbus

class Pbap:
	def __init__( self, device ):
		print( 'device:{}'.format( device ) )
		self._device = device
		
	def GetPhonebook( self ):
		bus = dbus.SessionBus()
		client = dbus.Interface(bus.get_object("org.openobex.client", "/"),	"org.openobex.Client")

		print "Creating Session"
		session_path = client.CreateSession({"Destination": self._device, "Target": "PBAP"})
		pbap = dbus.Interface(bus.get_object("org.openobex.client", session_path),
								"org.openobex.PhonebookAccess")
		session = dbus.Interface(bus.get_object("org.openobex.client", session_path),
									"org.openobex.Session")

		#paths = ["PB", "ICH", "OCH", "MCH", "CCH"]
		pbap.Select("int", "PB")
		pbap.SetFormat("vcard30")
		#pbap.SetFilter(["VERSION", "FN", "TEL"]);
		return pbap.PullAll()
#cards = pb.split( "END:VCARD\r\n" ) ;
#print( "{} cards".format( len( cards ) ) )
#import pprint
#for card in cards:
	#pprint.pprint( card )
#pprint.pprint( pb )
#for path in paths:
	#print "\n--- Select Phonebook %s ---\n" % (path)
	#pbap.Select("int", path)
#
	#print "\n--- GetSize ---\n"
	#ret = pbap.GetSize()
	#print "Size = %d\n" % (ret)
#
	#print "\n--- List vCard ---\n"
	#ret = pbap.List()
	#for item in ret:
		#print "%s : %s" % (item[0], item[1])
		#pbap.SetFormat("vcard30")
		#pbap.SetFilter(["VERSION", "FN", "TEL"]);
		#ret = pbap.Pull(item[0])
		#print "%s" % (ret)
#
	#print "\n--- PullAll ---\n"
	#pbap.SetFormat("vcard30")
	#pbap.SetFilter(["VERSION", "FN", "TEL"]);
	#ret = pbap.PullAll()
	#print "%s" % (ret)

if __name__ == "__main__":
	pbap = Pbap( sys.argv[1] )
	pb = pbap.GetPhonebook()
	import pprint #; pprint.pprint( pb )
	cards = pb.split( "END:VCARD" )
	i = 1
	for card in cards:
		print( '{}:'.format( i ) )
		i += 1
		pprint.pprint( card )
		print()
	print( '{} vcards found'.format( len( cards ) ) )
	f = file( "pb.vcf", "w" )
	f.write( pb.encode('UTF-8') )
	f.close()
