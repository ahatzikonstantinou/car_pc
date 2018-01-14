#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import pyinotify
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes

def Monitor(path):
	class PClose(ProcessEvent):
		def process_default(self, event):
			print( 'default processing event: {}'.format( event ) )
		
		def process_IN_CREATE( self, event ):
			print( 'process_IN_CREATE: processing event: {}'.format( event ) )
			
		def process_IN_DELETE( self, event ):
			print( 'process_IN_DELETE: processing event: {}'.format( event ) )
			
	wm = WatchManager()
	notifier = Notifier(wm, PClose())
	wm.add_watch(path, pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_ISDIR ) # | pyinotify.IN_UNMOUNT ) #|pyinotify.IN_CLOSE_NOWRITE)
	#wm.add_watch( path, pyinotify.ALL_EVENTS ) #, proc_fun=PClose() )
	try:
		while 1:
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
	except KeyboardInterrupt:
		notifier.stop()
		return


if __name__ == '__main__':
	try:
		path = sys.argv[1]
	except IndexError:
		print 'use: %s dir' % sys.argv[0]
	else:
		Monitor(path)
