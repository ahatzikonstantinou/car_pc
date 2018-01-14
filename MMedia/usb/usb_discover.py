#!/usr/bin/python
# -*- coding: utf-8 -*-

#discovers usb mounted devices

import subprocess
import os

class USBDisk:
	def __init__( self, label, dev_path ):
		self.label = label
		self.dev_path = dev_path
		self.mount_path = None
		
	@staticmethod
	def FromLabelPathLine( line ):
		parts = line.split( ' ' )
		return USBDisk( parts[0].strip(), os.path.join( '/dev', os.path.basename( parts[1].strip() ) ) )
		
	def __repr__( self ):
		return 'Label: {}, Dev: {}{}'.format( self.label, self.dev_path, ( ', Path:{}'.format(self.mount_path) if self.mount_path else '' ) )
		
class USBDiscoverer:
	'''
	This class disovers mounted usb disk and is based on bash shell calls. Tested
	with Ubuntu 12.04
	'''
	
	#In the examples given for the following two commands 
	#Elements and Elements-ext3 are a vfat and ext3 partition
	#of an external usb hard disk, KINGSTON is a usb memory stick
	#'/' is the root of the internal scsi hard disk (ext3 filesystem)
	
	#The DEV_CMD returns a table containing all dev/disks in two columns: 
	# 1) label, 2) /dev path e.g. 
	#Elements ../../sdg1
	#Elements-ext3 ../../sdg2
	#KINGSTON ../../sdh1
	#We assume that all external disks, usb sticks etc will have a label and
	#can be found in /dev/disk/by-label/
	DEV_DISK_CMD = 'ls -l /dev/disk/by-label/ | tail -n +2 | tr -s " " | cut -d " " -f 9,11'
	
	#The DEV_MOUNT_CMD returns a table containing all mounted devices in two columns:
	#1) /dev path, 2) mount_point e.g.
	#/dev/sda1 /
	#/dev/sdg1 /media/Elements
	#/dev/sdg2 /media/Elements-ext3

	MOUNT_CMD = 'cat /etc/mtab | cut -d " " -f 1,2 | grep "^/dev/"'
	def __init__( self ):
		pass
		
	@staticmethod
	def GetMountedUSBDisks():
		dev_disks_lines = subprocess.check_output( USBDiscoverer.DEV_DISK_CMD, shell=True ).strip().split( '\n' )
		#print( dev_disks_lines )
		dev_disks = [ USBDisk.FromLabelPathLine( l ) for l in dev_disks_lines ]
		#print( dev_disks )
		
		mount_devs = subprocess.check_output( USBDiscoverer.MOUNT_CMD, shell=True ).strip().split( '\n' )
		#print( mount_devs )
		
		mounted_disks = []
		for d in dev_disks:
			for m in mount_devs:
				parts = m.split( ' ' )
				#print( 'comparing {} against {}'.format( parts[0].strip(), d.dev_path ) )
				if( parts[0].strip() == d.dev_path ):
					d.mount_path = parts[1].strip()
					mounted_disks.append( d )
					#print( '\tMatch' )
					break
				#print( '\tNo Match' )
			
		return mounted_disks
				
if __name__ == '__main__':
	import pprint; pprint.pprint( USBDiscoverer.GetMountedUSBDisks() )
		
		
		
