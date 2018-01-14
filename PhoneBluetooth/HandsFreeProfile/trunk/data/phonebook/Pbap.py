#!/usr/bin/python

import sys
import dbus

class Pbap:
	def __init__( self, device ):
		self.__device = device
		
	def SupportsPhonebook( self ):
		try:
			bus = dbus.SessionBus()
			client = dbus.Interface(bus.get_object("org.openobex.client", "/"),
									"org.openobex.Client")

			#print "Creating Session"
			session_path = client.CreateSession({"Destination": self.__device, "Target": "PBAP"})			
			print( 'Device "' + self.__device + '" does support PBAP' )
			client.RemoveSession( session_path )
			return True
		except dbus.exceptions.DBusException:
			print( 'Device "' + self.__device + '" does not support PBAP' )
			return False
					
	def GetPB( self ):
		'''Dbus will timeout for large phonebooks. Use GetPBPerVCard isntead'''
		bus = dbus.SessionBus()

		client = dbus.Interface(bus.get_object("org.openobex.client", "/"),
								"org.openobex.Client")

		#print "Creating Session"
		session_path = client.CreateSession({"Destination": self.__device, "Target": "PBAP"})
		pbap = dbus.Interface(bus.get_object("org.openobex.client", session_path),
								"org.openobex.PhonebookAccess")
		session = dbus.Interface(bus.get_object("org.openobex.client", session_path),
									"org.openobex.Session")

		print "\n--- Select Phonebook internal:pb ---\n"
		pbap.Select("int", "pb")
		
		print "\n--- PullAll ---\n"
		pbap.SetFormat("vcard30")
		pb = pbap.PullAll()
		client.RemoveSession( session_path )
		return pb
		
	def GetVCards_old( self ):
		'''Works with GetPB()'''
		pb = self.GetPB()
		cards = pb.split( "END:VCARD\r\n" )
		#i = 1
		for card in cards:
			#print( '{}:'.format( i ) )
			#i += 1
			#pprint.pprint( card )
			#print()
			card += ( "END:VCARD" )
		return cards

	def GetPBPerVCard( self ):
		bus = dbus.SessionBus()

		client = dbus.Interface(bus.get_object("org.openobex.client", "/"),
								"org.openobex.Client")

		#print "Creating Session"
		session_path = client.CreateSession({"Destination": self.__device, "Target": "PBAP"})
		pbap = dbus.Interface(bus.get_object("org.openobex.client", session_path),
								"org.openobex.PhonebookAccess")
		session = dbus.Interface(bus.get_object("org.openobex.client", session_path),
									"org.openobex.Session")


		print "\n--- Select Phonebook internal:pb ---\n"
		pbap.Select("int", "pb")
		
		print "\n--- GetPhonebook ---\n"
		pbap.SetFormat("vcard30")

		vl = pbap.List()
		cards = []
		for v in vl:
			#print( "Will pull {}".format( v[0] ) )
			c = pbap.Pull( v[0] )
			#print( "Got {}".format( c.encode('UTF-8') ) )
			cards.append( c )
			

		client.RemoveSession( session_path )
		return cards

	def GetVCards( self ):
		return self.GetPBPerVCard()

#print "%s" % (ret)
#
#print "\n--- GetSize ---\n"
#ret = pbap.GetSize()
#print "Size = %d\n" % (ret)
#
#print "\n--- List vCard ---\n"
#ret = pbap.List()
#for item in ret:
	#print "%s : %s" % (item[0], item[1])
#
#if len(ret) > 0:
	#print "\n--- Pull First Available vCard ---\n"
	#ret = pbap.Pull(ret[0][0])
	#print "%s" % (ret)
#
#print "\n--- List All Available Filter Fields ---\n"
#ret = pbap.ListFilterFields()
#for item in ret:
	#print "%s" % (item)
	
if __name__ == "__main__":
	client = Pbap( sys.argv[1] )
	if( client.SupportsPhonebook() ):
		if( len( sys.argv ) > 2 ):
			if( len( [ v for v in sys.argv if v == '-v' ] ) > 0 ):
				print( 'saving vcards...' )
				cards = client.GetVCards()
				i = 0
				for card in cards:
					i = i+1
					f = file( str(i)+'.vcf', "w" )
					f.write( card.encode('UTF-8') )
					f.close()
			else:
				#pb = client.GetPB()
				#pb = client.GetPBViaSynch()
				cards = client.GetPBPerVCard()
				card_text = "\n".join( cards )
				
				f = file( sys.argv[2], "w" )
				f.write( card_text.encode('UTF-8') )
				f.close()
		else:
			import pprint ; pprint.pprint( client )
