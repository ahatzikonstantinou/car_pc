#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import csv
from custom_controls import MMediaListItem
from radio_station_media_list_item import RadioStationMediaListItem

class StationList:
	
	Filename = "stations_list.csv"
	def __init__( self ):
		self.stations = {}

	def StationAt( self, frequency ):
		for i in self.stations.keys():
			# print( 'Testing {} - {} = {}'.format( float( i ), frequency, math.fabs( frequency - float( i ) ) ) )
			if( math.fabs( frequency - float( i ) ) < 0.01 ):
				return self.stations[ i ]
		
		return None
		
	def Load( self, filename = None ):
		if( filename is None ):
			filename = StationList.Filename
		reader_list = csv.reader(open( filename, "rb"))
		station_list = []
		station_list.extend(reader_list)
		for data in station_list:
			self.stations[ data[0] ] = data[1].strip().strip( '\'"')
			#print( data[0] + ' - ' + data[1].strip().strip( '\'"') )
		#keys = sorted( self.stations.keys(), key = float )
		
	def Save( self, filename = None ):
		if( filename is None ):
			filename = StationList.Filename
		with open( filename, 'w' ) as file:
			for f,n in self.stations.iteritems():
				file.write( '"{}", \'{}\'\n'.format( f, n ) )

	def DeleteStation( self, frequency ):
		del self.stations[ str( frequency ) ]
		self.Save()

	def AddStation( self, frequency, stationName ):
		self.stations[ str( frequency ) ] = stationName
		self.Save()

	def EditStation( self, frequency, stationName ):
		self.stations[ str( frequency ) ] = stationName
		self.Save()

	def ToMediaListItems( self ):
		media_list_items = []
		keys = sorted( self.stations.keys(), key=float )
		for k in keys:
			frequency = k
			name = self.stations[k]
			media_list_items.append( RadioStationMediaListItem( frequency, name ) )

		return media_list_items
		
class DemoStationList( StationList ):

	demoStations = {
		'87.7': 'Εν λευκώ',
		'88.0': 'Oasis fm',
		'88.3': 'V fm',
		'88.6': 'Fresh 88.6',
		'88.9': 'Freedom',
		'89.2': 'MTV RADIO',
		'89.5': 'Εκκλησία της Ελλάδος',
		'89.8': 'Δρόμος',
		'90.1': 'Αριστερά στα fm',
		'90.4': 'Κανάλι 1',
		'91.2': 'Πειραική εκκλησία',
		'91.6': 'ΝΕΤ 105,8',
		'92.0': 'Galaxy 92',
		'92.3': 'Λάμψη',
		'92.6': 'Best radio',
		'92.9': 'Kiss',
		'93.2': 'Orange',
		'93.6': 'Κόσμος',
		'93.9': 'Χριστιανισμός',
		'94.0': 'Επικοινωνία fm',
		'94.3': 'Xenios fm',
		'94.6': 'ΝOVA Sport fm',
		'94.9': 'Ρυθμός',
		'95.2': 'Ράδιο DeeJay',
		'96.0': 'Flash 96',
		'96.3': 'Red',
		'96.6': 'Δίφωνο',
		'96.8': 'Rock fm',
		'97.2': 'Antenna Radio',
		'97.5': 'Love Radio',
		'97.8': 'Real fm',
		'98': '98fm',
		'98.3': 'Aθήνα 9,84',
		'98.6': 'Derti',
		'98.9': 'Θέμα 989',
		'99.2': 'Μελωδία fm',
		'99.5': 'BHMA fm',
		'100.3': 'ΣΚΑΪ 100,3',
		'101.3': 'Δίεση',
		'101.8': 'ΕΡΑ sport',
		'102.2': 'Sfera',
		'102.5': 'Νitro radio',
		'103.7': 'ΕΡΑ Δεύτερο Πρόγραμμα',
		'104.4': 'Athens International Radio Air',
		'105.8': 'ΝΕΤ 105,8',
		'107.7': 'Tρίτο πρόγραμμα',
		'105.8': 'Atlantis',
		'106.7': 'Digital fm',
		'102.7': 'Radio City fm',
		'104.0': 'Παρέα fm',
		'105.5': 'Στο Κόκκινο',
		'104.75': 'Hot fm',
		'103.3': 'Sentra fm' }		
		
	def __init__( self ):
		self.stations = DemoStationList.demoStations

if __name__ == '__main__':
	l = StationList()
	l.Load()
