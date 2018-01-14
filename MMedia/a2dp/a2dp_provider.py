#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import os
import logging

logging.basicConfig( level=logging.DEBUG )

__all__ = [ 'A2DPSource', 'A2DPProvider' ]

class A2DPSource:
	A2DP_PREFIX = 'a2dp_' #prefix required to make a2dp dbus source_paths unique
	
	def __init__( self, source_path, name, address, pulseaudio_name ):
		self.source_path = source_path
		self.name = name
		self.address = address
		self.pulseaudio_name = pulseaudio_name
		
	def Hash( self ):
		return A2DPSource.A2DPHash( self.source_path )
		
	def PulseaudioId( self ):
		return A2DPSource.A2DPPulseaudioId( self.source_path )
		
	@staticmethod
	def A2DPPulseaudioId( source_path ):
		return os.path.basename( source_path )[6:]
		
	@staticmethod
	def A2DPHash( source_path ):
		return A2DPSource.A2DP_PREFIX + source_path.replace( '/', '_' )
		
	def __repr__( self ):
		return str( self.source_path )
		
class A2DPProvider:
	DEBUG = True
	def __init__( self ):
		self._a2dp_sources = {}
		self._source_added_observers = []
		self._source_removed_observers = []
		
		try:
			os.system( 'pacmd load-module module-dbus-protocol' )
		except:
			import traceback; traceback.print_exc()

		from dbus.mainloop.glib import DBusGMainLoop
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
				
		self.conn = A2DPProvider.Connect()
		self.core = self.conn.get_object(object_path="/org/pulseaudio/core1")

		if( A2DPProvider.DEBUG ):
			logging.debug( "Successfully connected to " + self.core.Get("org.PulseAudio.Core1", "Name", dbus_interface="org.freedesktop.DBus.Properties") + "!" )

		self.LoadAllSources()

		self.conn.add_signal_receiver( 
			self.SourceAdded,
			dbus_interface="org.PulseAudio.Core1",
			signal_name="NewSource" )
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Added receiver for signal NewSource' )
								
		self.conn.add_signal_receiver( 
			self.SourceRemoved,
			dbus_interface="org.PulseAudio.Core1",
			signal_name="SourceRemoved" )
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Added receiver for signal SourceRemoved' )

		#I need to listen to this signal in order to remove module-loopback so that
		#a2dp sources are audible only via the A2DPMediaPlayer of the corresponding
		#A2DPDevice
		self.conn.add_signal_receiver( 
			self.ModuleAdded,
			dbus_interface="org.PulseAudio.Core1",
			signal_name="NewModule" )
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Added receiver for signal NewModule' )
								
		#core.ListenForSignal( 'org.PulseAudio.Core1.NewSource', dbus.Array(signature='o') )
		#core.ListenForSignal( 'org.PulseAudio.Core1.SourceRemoved', dbus.Array(signature='o') )
		self.core.ListenForSignal( '', dbus.Array(signature='o') )
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Started listening for all signals' )
		
	def AddSourceAddedObserver( self, observer ):
		self._source_added_observers.append( observer )
		
	def UpdateSourceAddedObservers( self, a2dp_source ):
		for o in self._source_added_observers:
			if( A2DPProvider.DEBUG ):
				logging.debug( 'UpdateSourceAddedObservers updating {} that {} was added'.format( o, a2dp_source.Hash() ) )
			o.A2DPSourceAdded( a2dp_source )
			
	def AddSourceRemovedObserver( self, observer ):
		self._source_removed_observers.append( observer )

	def UpdateSourceRemovedObservers( self, a2dp_source_hash ):
		for o in self._source_added_observers:
			if( A2DPProvider.DEBUG ):
				logging.debug( 'UpdateSourceRemovedObservers updating {} that {} was removed'.format( o, a2dp_source_hash ) )
			o.A2DPSourceRemoved( a2dp_source_hash )
		
	@staticmethod
	def Connect():
		if 'PULSE_DBUS_SERVER' in os.environ:
			address = os.environ['PULSE_DBUS_SERVER']
			if( A2DPProvider.DEBUG ):
				logging.debug( "Found os.environ['PULSE_DBUS_SERVER']" )
		else:
			bus = dbus.SessionBus()
			server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
			address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface="org.freedesktop.DBus.Properties")
			if( A2DPProvider.DEBUG ):
				logging.debug( 'Could not find os.environ[PULSE_DBUS_SERVER]' )

		return dbus.connection.Connection(address)

	def ModuleAdded( self, module_path ):
		if( A2DPProvider.DEBUG ):
				logging.debug( 'module {} added, will try to remove loopback'.format( module_path ) )
		try:
			self._TryRemoveModuleLoopback( module_path )
		except:
			logging.debug( 'Could not remove module loopback' )
			pass
		
	def SourceAdded( self, source ):
		if( A2DPProvider.DEBUG ):
			logging.debug( "New source: {}".format( source ) )
		a2dp_source = self._GetA2DPSource( source )
		if( a2dp_source is not None ):
			if( A2DPProvider.DEBUG ):
				logging.debug( 'will add {} to my sources dict'.format( a2dp_source.Hash() ) )
			self._a2dp_sources[ a2dp_source.Hash() ] = a2dp_source
			self._RemoveRecordingLoopBack( a2dp_source )
			if( A2DPProvider.DEBUG ):
				logging.debug( 'will update observers...' )
			self.UpdateSourceAddedObservers( a2dp_source )
			if( A2DPProvider.DEBUG ):
				logging.debug( 'finished updating observers' )
				
	def SourceRemoved( self, source ):
		'''
		The source is the object path, but the object does not exist, only the path is available now.
		Note, all pulseaudio sources that are removed will be reported here
		'''
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Source {} removed'.format( source ) )
		source_hash = A2DPSource.A2DPHash( source )
		if( self._a2dp_sources.has_key( source_hash ) ):
			self.UpdateSourceRemovedObservers( source_hash )
			del self._a2dp_sources[ source_hash ]
		
	def GetSrcProps( self, properties_manager ):
		properties = {}		
		props = properties_manager.Get('org.PulseAudio.Core1.Device', 'PropertyList')
		#if( A2DPProvider.DEBUG ):
			#logging.debug( "Properties:" )
		for k,v in props.iteritems():
			value = ''.join( [ chr(c) for c in v ] )
			#if( A2DPProvider.DEBUG ):
				#logging.debug( '\t{}: {}'.format( k, value ) )
			properties[ k ] = value
		return properties
			
	def LoadAllSources( self ):
		self._a2dp_sources = {}
		srcs = self.core.Get("org.PulseAudio.Core1", "Sources", dbus_interface="org.freedesktop.DBus.Properties")
		for s in srcs:
			if( A2DPProvider.DEBUG ):
				logging.debug( 'source: {}'.format( os.path.basename( s )[6:] ) )
			a2dp_source = self._GetA2DPSource( s )
			if( a2dp_source is not None ):
				self._a2dp_sources[ a2dp_source.Hash() ] = a2dp_source
				self._RemoveRecordingLoopBack( a2dp_source )
	
	def GetAllSources( self ):
		return self._a2dp_sources.values()
		
	def _GetA2DPSource( self, source_path ):
		src_obj = self.conn.get_object( object_path = source_path )
		properties_manager = dbus.Interface( src_obj, 'org.freedesktop.DBus.Properties' )
		#properties_manager.Set('org.PulseAudio.Core1.Device', 'xxx', 100.0 )
		pulseaudio_name = properties_manager.Get('org.PulseAudio.Core1.Device', 'Name')
		props = self.GetSrcProps( src_obj )
		if( props.has_key( dbus.String( u'bluetooth.protocol' ) ) and props[ dbus.String( u'bluetooth.protocol' ) ] == 'a2dp_source\x00' ):
			name = str( props[ dbus.String( u'device.description' ) ] )
			address = str( props[ dbus.String( u'device.string' ) ] )
			if( A2DPProvider.DEBUG ):
				logging.debug( 'Found an a2dp source: {} ({}, {})'.format( name, source_path, address ) )
			return A2DPSource( source_path = source_path, name = name, address = address, pulseaudio_name = pulseaudio_name )
		return None
		
	def _RemoveRecordingLoopBack( self, a2dp_source ):
		'''
		Must find and terminate any Recording Loopback to the default sink
		so that audio is controlled only via the a2dp media player that the corresponding
		a2dp device wil use
		See the "Recording" tab in pavucontrol
		'''
		if( A2DPProvider.DEBUG ):
			logging.debug( 'Will try to remove module-loopback for {}'.format( a2dp_source ) )
		modules = self.core.Get("org.PulseAudio.Core1", "Modules", dbus_interface="org.freedesktop.DBus.Properties")
		#if( A2DPProvider.DEBUG ):
			#logging.debug( '\tmodules:\n\t{}'.format( modules ) )
		for m in modules:
			self._TryRemoveModuleLoopback( m, a2dp_source )
			
	def _TryRemoveModuleLoopback( self, module_path, a2dp_source = None ):
			m_obj = self.conn.get_object( object_path = module_path )
			properties_manager = dbus.Interface( m_obj, 'org.freedesktop.DBus.Properties' )
			m_name = properties_manager.Get('org.PulseAudio.Core1.Module', 'Name')
			m_arguments = properties_manager.Get('org.PulseAudio.Core1.Module', 'Arguments')
			if( A2DPProvider.DEBUG and m_name == 'module-loopback' ):
				logging.debug( '\tthis is module-loopback' )
				
			source_ids = []
			if( a2dp_source is None ):
				source_ids = [ u'{}'.format( s.PulseaudioId() ) for s in self._a2dp_sources.values() ]
			else:
				source_ids = [ a2dp_source.PulseaudioId() ]
				
			if( m_name == 'module-loopback' and
				m_arguments.has_key( dbus.String( u'source' ) ) and 
				m_arguments[ dbus.String( u'source' ) ] in source_ids ):
				if( A2DPProvider.DEBUG ):
					logging.debug( '\tfound the loopback of my source {} and will remove it'.format( m_arguments[ dbus.String( u'source' ) ] ) )
				m_obj.Unload()
				if( A2DPProvider.DEBUG ):
					logging.debug( '\tunloaded module-loopback of source {}'.format( m_arguments[ dbus.String( u'source' ) ] ) )
	
if __name__ == '__main__':
	try:
		import gobject
		from dbus.mainloop.glib import DBusGMainLoop

		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
								
		ap = A2DPProvider()
		#ap.LoadAllSources()
		for k,v in ap._a2dp_sources.iteritems():
			#if( A2DPProvider.DEBUG ):
				#logging.debug( '{} ({}): {} ({})'.format( k, type(k), v, type(v) ) )
			ap._RemoveRecordingLoopBack( v )
		
		loop = gobject.MainLoop()
		loop.run()
	except:
		import traceback; traceback.print_exc()
