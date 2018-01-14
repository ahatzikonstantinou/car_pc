#!/usr/bin/python
# -*- coding: utf-8 -*-

import glib
import gudev
#import pynotify
import sys
import subprocess
import os

def callback(client, action, device, user_data):
	device_vendor = device.get_property("ID_VENDOR_ENC")
	device_model = device.get_property("ID_MODEL_ENC")
	if action == "add":
		msg = "USB Device Added", "%s %s is now connected to your system" % ( device_vendor, device_model ) 
		print msg
		#n = pynotify.Notification( msg )
		#n.show()
		print device
		for device_key in device.get_property_keys():
			print "   property %s: %s" % (device_key, device.get_property(device_key))
			print "----------"
			
		if device.has_property("ID_CDROM"):
			print "Found CD/DVD drive at %s" % device.get_device_file()
		if device.has_property("ID_FS_LABEL"):
			print "Found disc: %s" % device.get_property("ID_FS_LABEL")
		elif device.has_property("ID_FS_TYPE"):
			print "Found disc"
		else:
			print "No disc"
			
		df_cmd = 'df -P | tr -s " " | cut -d " " -f 6 | tail -n +2'	#get all filesystems
		fs = subprocess.check_output( df_cmd, shell=True ).strip().split( '\n' )
		for f in fs:
			print( '{} is {}mount'.format( f, ( '' if os.path.ismount( f ) else 'NOT ' ) ) )
		
	elif action == "remove":
		msg = "USB Device Removed", "%s %s has been disconnected from your system" % ( device_vendor, device_model )
		print msg
		#n = pynotify.Notification()
		#n.show()


#if not pynotify.init( "USB Device Notifier" ):
	#sys.exit( "Couldn't connect to the notification daemon!" )

client = gudev.Client(["usb/usb_device"])
client.connect("uevent", callback, None)

loop = glib.MainLoop()
loop.run()
