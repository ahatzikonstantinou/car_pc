#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import pprint
from media_track import MediaTrack
from custom_controls import MMediaListItem

class Channel( MediaTrack ):
	def __init__( self, name='' ):
		MediaTrack.__init__( self )
		self.name = name
		self.frequency = 0 #number, usually in kHz
		self.polarisation = 'h' #'v' or 'h'
		self.sat_no = 0 #unsigned long, usually 0
		self.sym_rate = 0 #symbol rate in MSyms/sec
		self.inversion = 'INVERSION_AUTO' #INVERSION_ON, INVERSION_OFF, INVERSION_AUTO
		self.fec = 'FEC_AUTO' #FEC_1_2, FEC_2_3, FEC_3_4 ... FEC_8_9, FEC_AUTO, FEC_NONE
		self.fec_hp = -1
		self.fec_lp = -1
		self.qam = 'QAM_AUTO' #QPSK, QAM_128, QAM_16 ...
		self.bw = 'BANDWIDTH_8_MHZ' #BANDWIDTH_6_MHZ, BANDWIDTH_7_MHZ, BANDWIDTH_8_MHZ
		self.transmission_mode = 'TRANSMISSION_MODE_AUTO' #TRANSMISSION_MODE_2K, TRANSMISSION_MODE_8K
		self.guardlist = 'GUARD_INTERVAL_AUTO' #GUARD_INTERVAL_1_4, GUARD_INTERVAL_1_8, GUARD_INTERVAL_1_16, GUARD_INTERVAL_1_32,
		self.hierarchy_info = 'HIERARCHY_AUTO' #HIERARCHY_1, HIERARCHY_2, HIERARCHY_4, HIERARCHY_NONE
		self.vpid = 0 #video program ID
		self.apid = 0 #audio program ID
		self.service_id = 0 #service ID (needed for now/next information etc.)
		
	def Hash( self ):
		return self.frequency + '_' + self.service_id.strip()
		
	def Text( self ):
		return self.name

	@staticmethod
	def FindInList( channels_list, hash ):
		channel = None
		
	@staticmethod
	def Parse( line ):
		#print( 'parsing line:{}'.format( line ) )
		p = line.split( ':' )
		channel = Channel()
		channel.name = p[0]
		channel.frequency = p[1]
		channel.inversion = p[2]
		channel.bw = p[3]
		channel.fec_hp = p[4]
		channel.fec_lp = p[5]
		channel.qam = p[6]
		channel.transmission_mode = p[7]
		channel.guardlist = p[8]
		channel.hierarchy_info = p[9]
		channel.vpid = p[10]
		channel.apid = p[11]
		channel.service_id = p[12].strip()
		#print( 'returning channel:' )
		#channel.Dump()
		return channel
		
	def Dump( self ):
		d = 'name:' + self.name #+ \
			#'\nf:' + self.frequency + \
			#'\np:' + self.polarisation + \
			#'\nsn:' + str( self.sat_no ) +\
			#'\nsr:' + str( self.sym_rate ) +\
			#'\ni:' + self.inversion +\
			#'\nfe:' + str( self.fec ) +\
			#'\nfh:' + str( self.fec_hp ) +\
			#'\nfl:' + str( self.fec_lp ) +\
			#'\nq:' + self.qam +\
			#'\nb:' + self.bw +\
			#'\ntm:' + self.transmission_mode +\
			#'\ng:' + self.guardlist +\
			#'\nh:' + self.hierarchy_info +\
			#'\nv:' + str( self.vpid ) +\
			#'\na:' + str( self.apid ) +\
			#'\ns:' + str( self.service_id )
		print( d )		

	@staticmethod
	def SaveList( channels, filename ):
		f = open( filename, 'w' )
		keys = sorted( channels.keys() )
		for c, value in channels.iteritems():
		#for k in keys:
			#print( k )
			f.write( json.dumps( value, default = JsonExport, indent=2 ) )
		f.close()
		
	@staticmethod
	def LoadList( filename ):
		'''
		Load the file as a string, split it to get strings that represent dictionary objects,
		and pass each string to be json decoded as a channel. For some reason an extra 
		element "}" appears at the end and this is dicarded
		'''
		if( not os.path.isfile( filename ) ):
			return []
		f = open( filename, 'r' )
		s = f.read()
		f.close()
		c = [ x+'}' for x in s.split( '}' ) ] #split dict objects and put back '}' delimit
		channels = [JsonImport( eval( ch ) ) for ch in c if ch != c[-1]]
		return channels
		
	@staticmethod
	def ToMediaListItems( channels ):
		media_list_items = []
		keys = sorted( channels.keys(), key=str )
		for k in keys:
			media_list_items.append( MMediaListItem( k, channels[k].name ) )

		return media_list_items
		
def JsonExport( obj ):
	# Convert objects to a dictionary of their representation
	d = { '__class__':obj.__class__.__name__,
		'__module__':obj.__module__,
		}
	d.update(obj.__dict__)
	return d
	
def JsonImport(d):
	#print( 'doing {}'.format( d ) )
	if '__class__' in d:
		class_name = d.pop('__class__')
		module_name = d.pop('__module__')
		module = __import__( module_name)
		#print 'MODULE:', module
		class_ = getattr(module, class_name)
		#print 'CLASS:', class_
		args = dict( (key.encode('ascii'), value) for key, value in d.items())
		#print 'INSTANCE ARGS:', args
		#inst = class_(**args)
		inst = class_()
		inst.__dict__ = d
	else:
		inst = d
	return inst
