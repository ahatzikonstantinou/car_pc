#!/usr/bin/python

import sys
import dbus

bus = dbus.SessionBus()

client = dbus.Interface(bus.get_object("org.openobex.client", "/"),
						"org.openobex.Client")

print "Creating Session"
session_path = client.CreateSession({"Destination": sys.argv[1], "Target": "PBAP"})
pbap = dbus.Interface(bus.get_object("org.openobex.client", session_path),
						"org.openobex.PhonebookAccess")
session = dbus.Interface(bus.get_object("org.openobex.client", session_path),
							"org.openobex.Session")

paths = ["PB", "ICH", "OCH", "MCH", "CCH"]
pbap.Select("int", "PB")
pbap.SetFormat("vcard30")
#pbap.SetFilter(["VERSION", "FN", "TEL"]);
pb = pbap.PullAll()
cards = pb.split( "END:VCARD\r\n" ) ;
print( "{} cards".format( len( cards ) ) )
import pprint
for card in cards:
	pprint.pprint( card )
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
