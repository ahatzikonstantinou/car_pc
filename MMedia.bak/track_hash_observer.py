#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx.lib.pubsub import Publisher	

class TrackHashObserversThreadProxy:
	'''
	This class will be called for CurrentTrackHashIs by media devices
	It will respond with wx.CallAfter to cover the case that call to CurrentTrackHashIs
	is made from another thread. It will catch the message itself, and the update any registered
	observers.
	So to ensure that everything works fine with threads, add a TrackHashObserversThreadProxy
	with any device that maintains TrackHashObservers, and the TrackHashObservers that update 
	wx.Widget objects add them only to TrackHashObserversThreadProxy	 
	'''
	PUBLISHER_MESSAGE = 'update_track_hash'
	def __init__( self, message_name = PUBLISHER_MESSAGE ):
		self.message_name = message_name
		self.trackHashObservers = []
		Publisher().subscribe( self._OnCurrentTrackHashIs, TrackHashObserversThreadProxy.PUBLISHER_MESSAGE )	
	
	def CurrentTrackHashIs( self, track_hash ):
		#print( 'TrackHashObserversThreadProxy posting track_hash: {}'.format( track_hash ) )
		wx.CallAfter( Publisher().sendMessage, self.message_name, track_hash )		
		
	def _OnCurrentTrackHashIs( self, msg ):
		track_hash = msg.data
		#print( 'TrackHashObserversThreadProxy updating observer with track_hash: {}'.format( track_hash ) )
		self.UpdateTrackHashObservers( track_hash )
		
	def AddTrackHashObserver( self, observer ):
		self.trackHashObservers.append( observer )
		
	def DelTrackHashObserver( self, observer ):
		self.trackHashObservers.remove( observer )
		
	def UpdateTrackHashObservers( self, track_hash ):
		for i in self.trackHashObservers:
			i.CurrentTrackHashIs( track_hash )
		
