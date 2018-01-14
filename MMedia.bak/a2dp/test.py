#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import os
import logging

logging.basicConfig( level=logging.DEBUG )

def connect():
	if 'PULSE_DBUS_SERVER' in os.environ:
		address = os.environ['PULSE_DBUS_SERVER']
		logging.debug( "Found os.environ['PULSE_DBUS_SERVER']" )
	else:
		bus = dbus.SessionBus()
		server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
		address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface="org.freedesktop.DBus.Properties")
		logging.debug( 'Could not find os.environ[PULSE_DBUS_SERVER]' )

	return dbus.connection.Connection(address)

def my_func( source ):
	try:
		print "source: ", source, "(", type( source ), ")"
		get_src_props( source )
	except:
		import traceback; traceback.print_exc()
	
def get_src_props( source ):
	src_obj = conn.get_object( object_path = source )
	properties_manager = dbus.Interface( src_obj, 'org.freedesktop.DBus.Properties' )
	#properties_manager.Set('org.PulseAudio.Core1.Device', 'xxx', 100.0 )
	props = properties_manager.Get('org.PulseAudio.Core1.Device', 'PropertyList')
	logging.debug( "Properties:" )
	for k,v in props.iteritems():
		logging.debug( '\t{}: {}'.format( k, ''.join( [ chr(c) for c in v ] ) ) )
	
import gobject
from dbus.mainloop.glib import DBusGMainLoop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
						
conn = connect()
core = conn.get_object(object_path="/org/pulseaudio/core1")

logging.debug( "Successfully connected to " + core.Get("org.PulseAudio.Core1", "Name", dbus_interface="org.freedesktop.DBus.Properties") + "!" )

conn.add_signal_receiver(my_func,
						dbus_interface="org.PulseAudio.Core1",
						signal_name="NewSource")
						
conn.add_signal_receiver(my_func,
						dbus_interface="org.PulseAudio.Core1",
						signal_name="SourceRemoved")

#core.ListenForSignal( 'org.PulseAudio.Core1.NewSource', dbus.Array(signature='o') )
#core.ListenForSignal( 'org.PulseAudio.Core1.SourceRemoved', dbus.Array(signature='o') )
core.ListenForSignal( '', dbus.Array(signature='o') )

loop = gobject.MainLoop()
loop.run()
