#!/usr/bin/python
# -*- coding: utf-8 -*-

#import pynotify
import sys
import os
from threading import *
import time
import pyinotify
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes

__all__ = [ 'USBDetector' ]
class MountEvents( ProcessEvent ):
	def __init__( self, MountDetectedCallback, UnmountDetectedCallback ):
		self.MountDetectedCallback = MountDetectedCallback
		self.UnmountDetectedCallback = UnmountDetectedCallback
		
	def process_default( self, event ):
		print( 'process_default was called with event: {}'.format( event ) )
		
	def process_IN_CREATE( self, event ):
		#print( 'MountEvents processing event: {}'.format( event ) )
		#Note: I used to test also for os.path.ismount( event.pathname ) but mounting cdroms
		#returned false so I took this check out
		if( os.path.isdir( event.pathname ) ):
			print( 'mount of {} was detected by event {}'.format( event.pathname, event ) )
			#print( '{} ismount: {}, isdir: {}'.format( event.pathname, os.path.ismount( event.pathname ), os.path.isdir( event.pathname ) ) )
			self.MountDetectedCallback( event.pathname )
		
	def process_IN_DELETE( self, event ):
		self.UnmountDetectedCallback( event.pathname )
		
class USBDetector:
	def __init__( self, path, MountDetectedCallback, UnmountDetectedCallback ):
		wm = WatchManager()
		notifier = Notifier( wm, MountEvents( MountDetectedCallback, UnmountDetectedCallback ) )
		wm.add_watch(path, pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_ISDIR )
		while( True ):
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
			time.sleep( 0.1 )
			
if __name__ == '__main__':
	def MountTest( fs ):
		print( 'I was just told {} was just mounted'.format( fs ) )
		
	def UnmountTest( fs ):
		print( 'I was just told {} was just unmounted'.format( fs ) )
	
	try:
		path = sys.argv[1]
	except IndexError:
		print 'use: %s dir' % sys.argv[0]
	else:
		import wx
		app = wx.App()
		wx.Frame( None, title='Test' )
		USBDetector( path, MountTest, UnmountTest )
		app.MainLoop()
