#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import wx
#~ from threading import Timer
from stationList import *
from CarPC_RDSDecoderListener import *
import v4l2radio
import sys
import signal
from mixer_pulseaudio import *

_PULSEAUDIO_SOURCENAME = 'alsa_input.usb-SILICON_LABORATORIES_INC._FM_Radio-00-Radio.analog-stereo'

class Radio:
	def __init__( self, radioDevice, RDSListener, frequency = 87.5 ):
		self.signalStrength = 0.0
		self.isStereo = False
		self.frequency = frequency
		self.MaxFrequency = 108.0
		self.MinFrequency = 87.5
		self.frequencyObservers = []
		self.signalStrengthObservers = []
		self.stereoMonoObservers = []
		self.mixer = PulseaudioMixer( _PULSEAUDIO_SOURCENAME )
		try:
			self.tuner = FMRadio()
			l,h = self.tuner.get_frequency_range()
			#print( '[{},{}]'.format( l, h ) )
			if( RDSListener is not None ):
				self.tuner.rds.add_listener( RDSListener )
			# keep the app running
			#while 1:
				#time.sleep(1000)
		except FMRadioUnavailableError:
			print "FM radio device is unavailable"
			sys.exit(1)
		
		# register signal handler for exiting
		def handler(signum, frame):
			self.tuner.close()
			sys.exit(0)
		#
		signal.signal(signal.SIGINT, handler)
		
	def Tune( self, frequency ):
		if( frequency > self.MaxFrequency or frequency < self.MinFrequency ):
			raise Exception( 'Cannot tune at {}. Range: [{} -{}]'.format( 
				frequency, self.MinFrequency, self.MaxFrequency )
				)
		self.frequency = frequency
		#print( 'Will tune to {}'.format( self.frequency ) )
		self.tuner.set_frequency( int( frequency * 1000 ) )
		#print( 'Finished setting frequency' )
		self.Refresh()
		self.UpdateObservers()

	def Refresh( self ):
		#Note that get_signal_strength reads multiple times the radio device
		#and refreshes the internal tuner info. So there is no further need
		#for refresh in order to get the sterero/mono mode
		self.signalStrength = self.tuner.get_signal_strength()
		self.isStereo = self.tuner.get_stereo()
		#self.isStereo = self.tuner.get_stereo()
		#print( 'Stereo:{}'.format( self.isStereo ) )		
		#self.UpdateSignalStrengthObservers()
		#self.UpdateStereoMonoObservers()
		#self.tuner.refresh_rds()
		pass
		
	def UpdateObservers( self ):
		self.UpdateFrequencyObservers()
		#print( 'Finished UpdateFrequencyObservers' )
		self.UpdateSignalStrengthObservers()
		#print( 'Finished UpdateSignalStrengthObservers' )
		self.UpdateStereoMonoObservers()
		#print( 'Finished UpdateStereoMonoObservers' )
		
	def AddFrequencyObserver( self, observer ):
		self.frequencyObservers.append( observer )
		
	def UpdateFrequencyObservers( self ):
		for i in self.frequencyObservers:
			i.FrequencyIs( self.frequency )
			
	def AddSignalStrengthObserver( self, observer ):
		self.signalStrengthObservers.append( observer )
		
	def UpdateSignalStrengthObservers( self ):
		for i in self.signalStrengthObservers:
			i.SignalStrengthIs( self.signalStrength )

	def AddStereoMonoObserver( self, observer ):
		self.stereoMonoObservers.append( observer )
		
	def UpdateStereoMonoObservers( self ):
		for i in self.stereoMonoObservers:
			i.IsStereo( self.isStereo )

	def IncreaseFrequency( self, kHz ):		
		self.frequency += ( kHz / 1000.0 )
		print( 'Increase by {0} to {1}'.format( str( kHz / 1000.0 ), self.frequency ) )
		if self.frequency > self.MaxFrequency:
			self.frequency = self.MinFrequency
		self.Tune( self.frequency )
		#~ self.Save()		
		
	def DecreaseFrequency( self, kHz ):
		self.frequency -= ( kHz / 1000.0 )
		print( 'Decrease by {0} to {1}'.format( str( kHz / 1000.0 ), self.frequency ) )
		if self.frequency < self.MinFrequency:
			self.frequency = self.MaxFrequency
		self.Tune( self.frequency )
		#~ self.Save()
		
	def GetVolume( self ):
		return self.mixer.GetVolume()
		
	def SetVolume( self, volume ):
		self.mixer.SetVolume( volume )
		
	def GetMute( self ):
		return self.mixer.GetMute()
		
	def SetMute( self, on ):
		self.mixer.SetMute( on )
		
	def GetSignalStrength( self ):
		return self.tuner.get_signal_strength()
	
	def GetMaxSignalStrength( self ):
		return self.tuner.MAX_SIGNAL_STRENGTH
			
	#def ScanNext( self ):
		#self.tuner.scan_next()
	#
	#def ScanPrevious( self ):
		#self.tuner.scan_previous()
	
class RandomRadio( Radio ):
	def __init__( self, frequency = 87.5 ):
		Radio.__init__( self, frequency )
		#super( RandomRadio, self ).__init__()
		
	def Tune( self, frequency ):
		self.signalStrength = random.randrange( 0, 100 )
		time.sleep( random.randrange( 5, 10 )/10.0 )
		Radio.Tune( self, frequency )
	
class DemoRadio( Radio ):	
		
	def __init__( self, frequency = 87.5, minAcceptableStationSignalStrength = 30 ):
		#Radio.__init__( self, None, frequency )
		self.MinAcceptableStationSignalStrength = minAcceptableStationSignalStrength
		self.stationList = DemoStationList()	
		
	def Tune( self, frequency ):	
		time.sleep( 0.1 )
		self.TuneStop( frequency )
		#Timer( random.randrange( 5, 10 )/10.0, self.TuneStop, [frequency] ).start()
		#d = DemoTimer( lambda: self.TuneStop( frequency ) )
		#d.Start( 1 ) 
	
	def TuneStop( self, frequency ):
		print( 'Testing {0}Mhz'.format( frequency ) )
		station = self.stationList.StationAt( frequency )
		if( station is not None ):
			# print( '{} at {}Mhz'.format( station, frequency ) )
			self.signalStrength = random.randrange( self.MinAcceptableStationSignalStrength, 100 )
			self.isStereo = ( random.randrange( 0.0, 10.0 ) > 0.1 )
		else:
			# print( 'No station at {}MHz'.format( frequency ) )
			self.signalStrength = random.randrange( 0, self.MinAcceptableStationSignalStrength - 1 )
			self.isStereo = False
		#Radio.Tune( self, frequency )

class DemoTimer( wx.Timer ):
	def __init__( self, notifyMethod ):
		wx.Timer.__init__( self )
		self.notifyMethod = notifyMethod
		
	def Notify( self ):
		print( 'Calling notify' )
		self.notifyMethod()

_DEFAULT_FREQUENCY = 102.5
def main():
    
	try:
		tuner = FMRadio(enable_rds=False)
		#pass
	except FMRadioUnavailableError:
		print "FM radio device is unavailable"
		sys.exit(1)

	# register signal handler for exiting
	def handler(signum, frame):
		tuner.close()
		sys.exit(0)

	signal.signal(signal.SIGINT, handler)

	# tune to a radio service
	frequency = float(sys.argv[1]) if len(sys.argv) is 2 else _DEFAULT_FREQUENCY
	print "Tuning to %0.2f Mhz" % frequency

	tuner.set_frequency(frequency*1000 )
	print( 'Actually tuned to {}'.format( tuner.get_frequency() ) )
	print( 'Signal strength:{}'.format( tuner.get_signal_strength() ) )
	#tuner.rds.add_listener( CarPC_RDSDecoderListener() )

	# keep the app running
	keep_running = True
	while keep_running:
		newFreq = input( 'Enter new frequency to tune at (e.g. 102.5):' )
		if( newFreq == 0 ):
			keep_running = False
			break
		else:
			tuner.set_frequency(newFreq*1000 )
			#print( 'Will check actual frequency' )
			#print( 'Actually tuned to {}'.format( tuner.get_frequency() ) )
			#print( 'Signal strength:{}'.format( tuner.get_signal_strength() ) )
		#time.sleep(1000)


if __name__ == "__main__":
	main()
