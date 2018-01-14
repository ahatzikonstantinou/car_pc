# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006,2007,2008,2009 Frank Scholz <coherence@beebits.net>

from sets import Set

from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall
from twisted.python import failure

from coherence.upnp.core.soap_service import errorCode
from coherence.upnp.core import DIDLLite

import string
import os, platform
from StringIO import StringIO
import tokenize

#import pygst
#pygst.require('0.10')
#import gst

import coherence.extern.louie as louie

from coherence.extern.simple_plugin import Plugin

from coherence import log

import coherence.extern.louie as louie
from coherence.base import Coherence
from coherence.upnp.devices.media_renderer import MediaRenderer

import logging
logging.basicConfig( level = logging.DEBUG )

class PlayerState:
	PLAYING = 0
	PAUSED = 1
	OTHER = 2
	
class MediaRendererProxyPlayer(log.Loggable,Plugin):

	""" a backend with a vlc based audio player """

	logCategory = 'vlc_player'
	implements = ['MediaRenderer']
	vendor_value_defaults = {'RenderingControl': {'A_ARG_TYPE_Channel':'Master'},
							 'AVTransport': {'A_ARG_TYPE_SeekMode':('ABS_TIME','REL_TIME','TRACK_NR')}}
	vendor_range_defaults = {'RenderingControl': {'Volume': {'maximum':100}}}

	def __init__(self, device, **kwargs):
		logging.debug( 'MediaRendererProxyPlayer: starting initialization' )
		if(device.coherence.config.get('use_dbus','no') != 'yes' and
		   device.coherence.config.get('glib','no') != 'yes'):
			raise Exception, 'this media renderer needs use_dbus enabled in the configuration'
		logging.debug( '\tInitialization passed the coherence checks' )
		self.name = kwargs.get('name','CARPC Player')
		logging.debug( '\tgot name {}'.format( self.name ) )
		self.controller = kwargs['controller']	#ahat
		logging.debug( '\tgot controller {}'.format( self.controller ) )

		self.metadata = None
		self.duration = None

		self.view = []
		self.tags = {}
		logging.debug( '\tabout to get the server device' )
		self.server = device
		logging.debug( '\tgot the server device' )

		self.playcontainer = None

		self.dlna_caps = ['playcontainer-0-1']

		logging.debug( 'MediaRendererProxyPlayer: Finished initialization' )
		louie.send('Coherence.UPnP.Backend.init_completed', None, backend=self)
		

	def __repr__(self):
		return str(self.__class__).split('.')[-1]

	def update(self, message=None):
		"""
		TODO: This function was also called by gstreamer at end of song etc. (observe the usage of the message variable). Perhaps I need to do this too
		"""
		#_, current,_ = self.player.get_state()
		current = self.controller.GetPlayerState()
		self.debug("update current %r", current)
		connection_manager = self.server.connection_manager_server
		av_transport = self.server.av_transport_server
		conn_id = connection_manager.lookup_avt_id(self.current_connection_id)
		if current == PlayerState.PLAYING: # gst.STATE_PLAYING:
			state = 'playing'
			av_transport.set_variable(conn_id, 'TransportState', 'PLAYING')
		elif current == PlayerState.PAUSED: #gst.STATE_PAUSED:
			state = 'paused'
			av_transport.set_variable(conn_id, 'TransportState',
									  'PAUSED_PLAYBACK')
		elif self.playcontainer != None and message == gst.MESSAGE_EOS and \
			 self.playcontainer[0]+1 < len(self.playcontainer[2]):
			state = 'transitioning'
			av_transport.set_variable(conn_id, 'TransportState', 'TRANSITIONING')

			next_track = ()
			item = self.playcontainer[2][self.playcontainer[0]+1]
			infos = connection_manager.get_variable('SinkProtocolInfo')
			local_protocol_infos = infos.value.split(',')
			res = item.res.get_matching(local_protocol_infos,
										protocol_type='internal')
			if len(res) == 0:
				res = item.res.get_matching(local_protocol_infos)
			if len(res) > 0:
				res = res[0]
				infos = res.protocolInfo.split(':')
				remote_protocol, remote_network, remote_content_format, _ = infos
				didl = DIDLLite.DIDLElement()
				didl.addItem(item)
				next_track = (res.data, didl.toString(), remote_content_format)
				self.playcontainer[0] = self.playcontainer[0]+1

			if len(next_track) == 3:
				av_transport.set_variable(conn_id, 'CurrentTrack',
										  self.playcontainer[0]+1)
				self.load(next_track[0], next_track[1], next_track[2])
				self.play()
			else:
				state = 'idle'
				av_transport.set_variable(conn_id, 'TransportState', 'STOPPED')
		elif message == gst.MESSAGE_EOS and \
			 len(av_transport.get_variable('NextAVTransportURI').value) > 0:
			state = 'transitioning'
			av_transport.set_variable(conn_id, 'TransportState', 'TRANSITIONING')
			CurrentURI = av_transport.get_variable('NextAVTransportURI').value
			metadata = av_transport.get_variable('NextAVTransportURIMetaData')
			CurrentURIMetaData = metadata.value
			av_transport.set_variable(conn_id, 'NextAVTransportURI', '')
			av_transport.set_variable(conn_id, 'NextAVTransportURIMetaData', '')
			r = self.upnp_SetAVTransportURI(self, InstanceID=0,
											CurrentURI=CurrentURI,
											CurrentURIMetaData=CurrentURIMetaData)
			if r == {}:
				self.play()
			else:
				state = 'idle'
				av_transport.set_variable(conn_id, 'TransportState', 'STOPPED')
		else:
			state = 'idle'
			av_transport.set_variable(conn_id, 'TransportState', 'STOPPED')

		self.info("update %r" % state)
		self._update_transport_position(state)

	def _update_transport_position(self, state):
		connection_manager = self.server.connection_manager_server
		av_transport = self.server.av_transport_server
		conn_id = connection_manager.lookup_avt_id(self.current_connection_id)

		position = self.player.query_position()
		#print position

		#for view in self.view:
			#view.status(self.status(position))

		if position.has_key(u'raw'):

			if self.duration == None and 'duration' in position[u'raw']:
				self.duration = int(position[u'raw'][u'duration'])
				if self.metadata != None and len(self.metadata)>0:
					# FIXME: duration breaks client parsing MetaData?
					elt = DIDLLite.DIDLElement.fromString(self.metadata)
					for item in elt:
						for res in item.findall('res'):
							formatted_duration = self._format_time(self.duration)
							res.attrib['duration'] = formatted_duration

					self.metadata = elt.toString()
					#print self.metadata
					if self.server != None:
						av_transport.set_variable(conn_id,
												  'AVTransportURIMetaData',
												  self.metadata)
						av_transport.set_variable(conn_id,
												  'CurrentTrackMetaData',
												  self.metadata)


			self.info("%s %d/%d/%d - %d%%/%d%% - %s/%s/%s", state,
					  string.atol(position[u'raw'][u'position'])/1000000000,
					  string.atol(position[u'raw'][u'remaining'])/1000000000,
					  string.atol(position[u'raw'][u'duration'])/1000000000,
					  position[u'percent'][u'position'],
					  position[u'percent'][u'remaining'],
					  position[u'human'][u'position'],
					  position[u'human'][u'remaining'],
					  position[u'human'][u'duration'])

			duration = string.atol(position[u'raw'][u'duration'])
			formatted = self._format_time(duration)
			av_transport.set_variable(conn_id, 'CurrentTrackDuration', formatted)
			av_transport.set_variable(conn_id, 'CurrentMediaDuration', formatted)

			position = string.atol(position[u'raw'][u'position'])
			formatted = self._format_time(position)
			av_transport.set_variable(conn_id, 'RelativeTimePosition', formatted)
			av_transport.set_variable(conn_id, 'AbsoluteTimePosition', formatted)

	def _format_time(self, time):
		fmt = '%d:%02d:%02d'
		try:
			m, s = divmod(time / 1000000000, 60)
			h, m = divmod(m, 60)
		except:
			h = m = s = 0
			fmt = '%02d:%02d:%02d'
		formatted = fmt % (h, m, s)
		return formatted

	def load( self, uri,metadata, mimetype=None): #+
		self.info("loading: %r %r " % (uri, mimetype))
		state = self.controller.GetPlayerState() #_,state,_ = self.player.get_state()
		connection_id = self.server.connection_manager_server.lookup_avt_id(self.current_connection_id)
		self.stop(silent=True) # the check whether a stop is really needed is done inside stop

		if mimetype is None:
			_,ext =  os.path.splitext(uri)
			if ext == '.ogg':
				mimetype = 'application/ogg'
			else:
				mimetype = 'audio/mpeg'
				
		elt = DIDLLite.DIDLElement.fromString( metadata )
		items = elt.getItems()		
		self.controller.SetCurrentTrack( uri, items[0] ) #self.player.load( uri, mimetype)

		self.metadata = metadata
		self.mimetype = mimetype
		self.tags = {}

		if self.playcontainer == None:
			self.server.av_transport_server.set_variable(connection_id, 'AVTransportURI',uri)
			self.server.av_transport_server.set_variable(connection_id, 'AVTransportURIMetaData',metadata)
			self.server.av_transport_server.set_variable(connection_id, 'NumberOfTracks',1)
			self.server.av_transport_server.set_variable(connection_id, 'CurrentTrack',1)
		else:
			self.server.av_transport_server.set_variable(connection_id, 'AVTransportURI',self.playcontainer[1])
			self.server.av_transport_server.set_variable(connection_id, 'NumberOfTracks',len(self.playcontainer[2]))
			self.server.av_transport_server.set_variable(connection_id, 'CurrentTrack',self.playcontainer[0]+1)

		self.server.av_transport_server.set_variable(connection_id, 'CurrentTrackURI',uri)
		self.server.av_transport_server.set_variable(connection_id, 'CurrentTrackMetaData',metadata)

		#self.server.av_transport_server.set_variable(connection_id, 'TransportState', 'TRANSITIONING')
		#self.server.av_transport_server.set_variable(connection_id, 'CurrentTransportActions','PLAY,STOP,PAUSE,SEEK,NEXT,PREVIOUS')
		if uri.startswith('http://'):
			transport_actions = Set(['PLAY,STOP,PAUSE'])
		else:
			transport_actions = Set(['PLAY,STOP,PAUSE,SEEK'])

		if len(self.server.av_transport_server.get_variable('NextAVTransportURI').value) > 0:
			transport_actions.add('NEXT')

		if self.playcontainer != None:
			if len(self.playcontainer[2]) - (self.playcontainer[0]+1) > 0:
				transport_actions.add('NEXT')
			if self.playcontainer[0] > 0:
				transport_actions.add('PREVIOUS')

		self.server.av_transport_server.set_variable(connection_id, 'CurrentTransportActions',transport_actions)
		self.controller.RefreshMediaActions( transport_actions )

		if state == PlayerState.PLAYING: #gst.STATE_PLAYING:
			self.info("was playing...")
			self.play()
		#TODO: ahat fix update
		#self.update()


	#def status( self, position):
		#uri = self.player.get_uri()
		#if uri == None:
			#return {u'state':u'idle',u'uri':u''}
		#else:
			#r = {u'uri':unicode(uri),
				 #u'position':position}
			#if self.tags != {}:
				#try:
					#r[u'artist'] = unicode(self.tags['artist'])
				#except:
					#pass
				#try:
					#r[u'title'] = unicode(self.tags['title'])
				#except:
					#pass
				#try:
					#r[u'album'] = unicode(self.tags['album'])
				#except:
					#pass

			##if self.player.get_state()[1] == gst.STATE_PLAYING:
			#if self.controller.GetPlayerState() == PlayerState.PLAYING:
			#	r[u'state'] = u'playing'
			##elif self.player.get_state()[1] == gst.STATE_PAUSED:
			#elif self.controller.GetPlayerState() == PlayerState.PAUSED:
			#	r[u'state'] = u'paused'
			#else:
			#	r[u'state'] = u'idle'

			#return r

	#def start( self, uri):
		#self.load( uri, metadata = None)
		#self.play()

	def stop(self,silent=False): #+
		#self.info('Stopping: %r' % self.player.get_uri())
		#if self.player.get_uri() == None:
			#return
		#if self.player.get_state()[1] in [gst.STATE_PLAYING,gst.STATE_PAUSED]:
			#self.player.stop()
			#if silent is True:
				#self.server.av_transport_server.set_variable(self.server.connection_manager_server.lookup_avt_id(self.current_connection_id), 'TransportState', 'STOPPED')
		self.controller.Stop( silent )		

	def play( self ): #+
		self.controller.Play()		

	def pause( self ): #+
		self.controller.Pause()

	def seek(self, location, old_state): #+
		self.controller.Seek( location )
		if old_state != None:
			self.server.av_transport_server.set_variable(0, 'TransportState', old_state)

	def mute(self): #+
		self.controller.Mute()

	def unmute(self): #+
		self.controller.Unmute()

	def get_mute(self): #+
		return self.controller.GetMute()

	def get_volume(self): #+
		return self.controller.GetVolume()

	def set_volume(self, volume): #+
		self.controller.SetVolume(volume)

	def playcontainer_browse(self,uri): #+
		"""
		dlna-playcontainer://uuid%3Afe814e3e-5214-4c24-847b-383fb599ff01?sid=urn%3Aupnp-org%3AserviceId%3AContentDirectory&cid=1441&fid=1444&fii=0&sc=&md=0
		"""
		from urllib import unquote
		from cgi import parse_qs
		from coherence.extern.et import ET
		from coherence.upnp.core.utils import parse_xml

		def handle_reply(r,uri,action,kw):
			try:
				next_track = ()
				elt = DIDLLite.DIDLElement.fromString(r['Result'])
				item = elt.getItems()[0]
				local_protocol_infos=self.server.connection_manager_server.get_variable('SinkProtocolInfo').value.split(',')
				res = item.res.get_matching(local_protocol_infos, protocol_type='internal')
				if len(res) == 0:
					res = item.res.get_matching(local_protocol_infos)
				if len(res) > 0:
					res = res[0]
					remote_protocol,remote_network,remote_content_format,_ = res.protocolInfo.split(':')
					didl = DIDLLite.DIDLElement()
					didl.addItem(item)
					next_track = (res.data,didl.toString(),remote_content_format)
				""" a list with these elements:

					the current track index
					 - will change during playback of the container items
					the initial complete playcontainer-uri
					a list of all the items in the playcontainer
					the action methods to do the Browse call on the device
					the kwargs for the Browse call
					 - kwargs['StartingIndex'] will be modified during further Browse requests
				"""
				self.playcontainer = [int(kw['StartingIndex']),uri,elt.getItems()[:],action,kw]

				def browse_more(starting_index,number_returned,total_matches):
					self.info("browse_more", starting_index,number_returned,total_matches)
					try:

						def handle_error(r):
							pass

						def handle_reply(r,starting_index):
							elt = DIDLLite.DIDLElement.fromString(r['Result'])
							self.playcontainer[2] += elt.getItems()[:]
							browse_more(starting_index,int(r['NumberReturned']),int(r['TotalMatches']))

						if((number_returned != 5 or
						   number_returned < (total_matches-starting_index)) and
							(total_matches-number_returned) != starting_index):
							self.info("seems we have been returned only a part of the result")
							self.info("requested %d, starting at %d" % (5,starting_index))
							self.info("got %d out of %d" % (number_returned, total_matches))
							self.info("requesting more starting now at %d" % (starting_index+number_returned))
							self.playcontainer[4]['StartingIndex'] = str(starting_index+number_returned)
							d = self.playcontainer[3].call(**self.playcontainer[4])
							d.addCallback(handle_reply,starting_index+number_returned)
							d.addErrback(handle_error)
					except:
						import traceback
						traceback.print_exc()

				browse_more(int(kw['StartingIndex']),int(r['NumberReturned']),int(r['TotalMatches']))

				if len(next_track) == 3:
					return next_track
			except:
				import traceback
				traceback.print_exc()

			return failure.Failure(errorCode(714))

		def handle_error(r):
			return failure.Failure(errorCode(714))

		try:
			udn,args =  uri[21:].split('?')
			udn = unquote(udn)
			args = parse_qs(args)

			type = args['sid'][0].split(':')[-1]

			try:
				sc = args['sc'][0]
			except:
				sc = ''

			device = self.server.coherence.get_device_with_id(udn)
			service = device.get_service_by_type(type)
			action = service.get_action('Browse')

			kw = {'ObjectID':args['cid'][0],
				  'BrowseFlag':'BrowseDirectChildren',
				  'StartingIndex':args['fii'][0],
				  'RequestedCount':str(5),
				  'Filter':'*',
				  'SortCriteria':sc}

			d = action.call(**kw)
			d.addCallback(handle_reply,uri,action,kw)
			d.addErrback(handle_error)
			return d
		except:
			return failure.Failure(errorCode(714))


	def upnp_init(self): #+
		self.current_connection_id = None
		self.server.connection_manager_server.set_variable(0, 'SinkProtocolInfo',
							['internal:%s:audio/mpeg:*' % self.server.coherence.hostname,
							 'http-get:*:audio/mpeg:*',
							 'internal:%s:audio/mp4:*' % self.server.coherence.hostname,
							 'http-get:*:audio/mp4:*',
							 'internal:%s:application/ogg:*' % self.server.coherence.hostname,
							 'http-get:*:application/ogg:*',
							 'internal:%s:audio/ogg:*' % self.server.coherence.hostname,
							 'http-get:*:audio/ogg:*',
							 'internal:%s:video/ogg:*' % self.server.coherence.hostname,
							 'http-get:*:video/ogg:*',
							 'internal:%s:video/x-msvideo:*' % self.server.coherence.hostname,
							 'http-get:*:video/x-msvideo:*',
							 'internal:%s:video/mp4:*' % self.server.coherence.hostname,
							 'http-get:*:video/mp4:*',
							 'internal:%s:video/quicktime:*' % self.server.coherence.hostname,
							 'http-get:*:video/quicktime:*',
							 'internal:%s:image/gif:*' % self.server.coherence.hostname,
							 'http-get:*:image/gif:*',
							 'internal:%s:image/jpeg:*' % self.server.coherence.hostname,
							 'http-get:*:image/jpeg:*',
							 'internal:%s:image/png:*' % self.server.coherence.hostname,
							 'http-get:*:image/png:*',
							 'http-get:*:*:*'],
							default=True)
		self.server.av_transport_server.set_variable(0, 'TransportState', 'NO_MEDIA_PRESENT', default=True)
		self.server.av_transport_server.set_variable(0, 'TransportStatus', 'OK', default=True)
		self.server.av_transport_server.set_variable(0, 'CurrentPlayMode', 'NORMAL', default=True)
		self.server.av_transport_server.set_variable(0, 'CurrentTransportActions', '', default=True)
		self.server.rendering_control_server.set_variable(0, 'Volume', self.get_volume())
		self.server.rendering_control_server.set_variable(0, 'Mute', self.get_mute())

	def upnp_Play(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		Speed = int(kwargs['Speed'])
		self.play()
		return {}

	def upnp_Pause(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		self.pause()
		return {}

	def upnp_Stop(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		self.stop()
		return {}

	def upnp_Seek(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		Unit = kwargs['Unit']
		Target = kwargs['Target']
		if InstanceID != 0:
			return failure.Failure(errorCode(718))
		if Unit in ['ABS_TIME','REL_TIME']:
			old_state = self.server.av_transport_server.get_variable('TransportState').value
			self.server.av_transport_server.set_variable(InstanceID, 'TransportState', 'TRANSITIONING')

			sign = ''
			if Target[0] == '+':
				Target = Target[1:]
				sign = '+'
			if Target[0] == '-':
				Target = Target[1:]
				sign = '-'

			h,m,s = Target.split(':')
			seconds = int(h)*3600 + int(m)*60 + int(s)
			self.seek(sign+str(seconds), old_state)
		if Unit in ['TRACK_NR']:
			if self.playcontainer == None:
				NextURI = self.server.av_transport_server.get_variable('NextAVTransportURI',InstanceID).value
				if NextURI != '':
					self.server.av_transport_server.set_variable(InstanceID, 'TransportState', 'TRANSITIONING')
					NextURIMetaData = self.server.av_transport_server.get_variable('NextAVTransportURIMetaData').value
					self.server.av_transport_server.set_variable(InstanceID, 'NextAVTransportURI', '')
					self.server.av_transport_server.set_variable(InstanceID, 'NextAVTransportURIMetaData', '')
					r = self.upnp_SetAVTransportURI(self, InstanceID=InstanceID,CurrentURI=NextURI,CurrentURIMetaData=NextURIMetaData)
					return r
			else:
				Target = int(Target)
				if 0 < Target <= len(self.playcontainer[2]):
					self.server.av_transport_server.set_variable(InstanceID, 'TransportState', 'TRANSITIONING')
					next_track = ()
					item = self.playcontainer[2][Target-1]
					local_protocol_infos=self.server.connection_manager_server.get_variable('SinkProtocolInfo').value.split(',')
					res = item.res.get_matching(local_protocol_infos, protocol_type='internal')
					if len(res) == 0:
						res = item.res.get_matching(local_protocol_infos)
					if len(res) > 0:
						res = res[0]
						remote_protocol,remote_network,remote_content_format,_ = res.protocolInfo.split(':')
						didl = DIDLLite.DIDLElement()
						didl.addItem(item)
						next_track = (res.data,didl.toString(),remote_content_format)
						self.playcontainer[0] = Target-1

					if len(next_track) == 3:
						self.server.av_transport_server.set_variable(self.server.connection_manager_server.lookup_avt_id(self.current_connection_id), 'CurrentTrack',Target)
						self.load(next_track[0],next_track[1],next_track[2])
						self.play()
						return {}
			return failure.Failure(errorCode(711))

		return {}

	def upnp_Next(self,*args,**kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		track_nr = self.server.av_transport_server.get_variable('CurrentTrack')
		return self.upnp_Seek(self,InstanceID=InstanceID,Unit='TRACK_NR',Target=str(int(track_nr.value)+1))

	def upnp_Previous(self,*args,**kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		track_nr = self.server.av_transport_server.get_variable('CurrentTrack')
		return self.upnp_Seek(self,InstanceID=InstanceID,Unit='TRACK_NR',Target=str(int(track_nr.value)-1))

	def upnp_SetNextAVTransportURI(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		NextURI = kwargs['NextURI']
		current_connection_id = self.server.connection_manager_server.lookup_avt_id(self.current_connection_id)
		NextMetaData = kwargs['NextURIMetaData']
		self.server.av_transport_server.set_variable(current_connection_id, 'NextAVTransportURI',NextURI)
		self.server.av_transport_server.set_variable(current_connection_id, 'NextAVTransportURIMetaData',NextMetaData)
		if len(NextURI) == 0  and self.playcontainer == None:
			transport_actions = self.server.av_transport_server.get_variable('CurrentTransportActions').value
			transport_actions = Set(transport_actions.split(','))
			try:
				transport_actions.remove('NEXT')
				self.server.av_transport_server.set_variable(current_connection_id, 'CurrentTransportActions',transport_actions)
			except KeyError:
				pass
			return {}
		transport_actions = self.server.av_transport_server.get_variable('CurrentTransportActions').value
		transport_actions = Set(transport_actions.split(','))
		transport_actions.add('NEXT')
		self.server.av_transport_server.set_variable(current_connection_id, 'CurrentTransportActions',transport_actions)
		return {}

	def upnp_SetAVTransportURI(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		CurrentURI = kwargs['CurrentURI']
		CurrentURIMetaData = kwargs['CurrentURIMetaData']
		#print "upnp_SetAVTransportURI",InstanceID, CurrentURI, CurrentURIMetaData
		if CurrentURI.startswith('dlna-playcontainer://'):
			def handle_result(r):
				self.load(r[0],r[1],mimetype=r[2])
				return {}

			def pass_error(r):
				return r

			d = defer.maybeDeferred(self.playcontainer_browse,CurrentURI)
			d.addCallback(handle_result)
			d.addErrback(pass_error)
			return d
		elif len(CurrentURIMetaData)==0:
			self.playcontainer = None
			self.load(CurrentURI,CurrentURIMetaData)
			return {}
		else:
			local_protocol_infos=self.server.connection_manager_server.get_variable('SinkProtocolInfo').value.split(',')
			#print local_protocol_infos
			elt = DIDLLite.DIDLElement.fromString(CurrentURIMetaData)
			if elt.numItems() == 1:
				item = elt.getItems()[0]
				res = item.res.get_matching(local_protocol_infos, protocol_type='internal')
				if len(res) == 0:
					res = item.res.get_matching(local_protocol_infos)
				if len(res) > 0:
					res = res[0]
					remote_protocol,remote_network,remote_content_format,_ = res.protocolInfo.split(':')
					self.playcontainer = None
					self.load(res.data,CurrentURIMetaData,mimetype=remote_content_format)
					return {}
		return failure.Failure(errorCode(714))

	def upnp_SetMute(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		Channel = kwargs['Channel']
		DesiredMute = kwargs['DesiredMute']
		if DesiredMute in ['TRUE', 'True', 'true', '1','Yes','yes']:
			self.mute()
		else:
			self.unmute()
		return {}

	def upnp_SetVolume(self, *args, **kwargs): #+
		InstanceID = int(kwargs['InstanceID'])
		Channel = kwargs['Channel']
		DesiredVolume = int(kwargs['DesiredVolume'])
		self.set_volume(DesiredVolume)
		return {}

	def SetRCSVariable( self, variable_name, variable_value ):
		'''
		This function will be called by the controller because the controller also needs to update
		the rendering_control_server but it has no connection_id
		'''
   		rcs_id = self.server.connection_manager_server.lookup_rcs_id( self.current_connection_id )
		self.server.rendering_control_server.set_variable( rcs_id, variable_name, variable_value )

	def SetAVTVariable( self, variable_name, variable_value ):
		'''
		This function will be called by the controller because the controller also needs to update
		the av_transport_server but it has no connection_id
		'''
   		self.server.av_transport_server.set_variable( self.server.connection_manager_server.lookup_avt_id(self.current_connection_id), variable_name, variable_value )

if __name__ == '__main__':

	import sys

	#p = Player(None)
	#p = GStreamerPlayer(None)
	#from coherence.upnp.devices.media_renderer import MediaRenderer
	#from coherence.base import Coherence
	#p = GStreamerPlayer( MediaRenderer( coherence = Coherence({'unittest':'no','logmode':'error','use_dbus':'yes','controlpoint':'yes'}), backend = None) )
	renderer = MediaRenderer(coherence = Coherence({'unittest':'no','logmode':'error','use_dbus':'yes','controlpoint':'yes'}), backend = MediaRendererProxyPlayer, kwargs = { 'controller': None } )
	#if len(sys.argv) > 1:
		#reactor.callWhenRunning( p.start, sys.argv[1])

	reactor.run()
