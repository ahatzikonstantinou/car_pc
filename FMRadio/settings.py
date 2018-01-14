#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import wx
import pprint

class FontSettings:
	def __init__( self ):
		self.Size = 20
		self.Family = wx.FONTFAMILY_DEFAULT
		self.Style = wx.FONTSTYLE_NORMAL
		self.Weight = wx.FONTWEIGHT_NORMAL
		self.Underline = False
		self.Facename = 'Verdana'
		self.Encoding = wx.FONTENCODING_SYSTEM

		self.Color = '#AAAA00'

		#~ def __repr__(self):
		#~ return json.dumps(self.__dict__ ) #, cls=MyEncoder)
		
	def GetFont( self ):
		return wx.Font(
				self.Size, 
				self.Family,
				self.Style,
				self.Weight,
				self.Underline,
				self.Facename,
				self.Encoding 
			)
                
	def FromDict( self, fontDict ):
		if( type( fontDict ) is not dict ):
			return False
		if( len( set( self.__dict__.keys() ).difference( fontDict.keys() ) ) == 0 ):
			self.__dict__ = fontDict
			return True
			
		return False

class Settings:
	'''These are the settings of the radio'''

	Filename = 'settings.radio' #the file were the settings are saved

	def __init__( self ):
		self.RDSFont = FontSettings()        
		self.RDSFont.Size = 20
		self.RDSFont.Family = wx.FONTFAMILY_DEFAULT
		self.RDSFont.Style = wx.FONTSTYLE_NORMAL
		self.RDSFont.Weight = wx.FONTWEIGHT_NORMAL
		self.RDSFont.Underline = False
		self.RDSFont.Facename = 'Verdana'
		self.RDSFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.RDSFont.Color = '#AAAA00'

		self.StationNameFont = FontSettings()
		self.StationNameFont.Size = 20
		self.StationNameFont.Family = wx.FONTFAMILY_DEFAULT
		self.StationNameFont.Style = wx.FONTSTYLE_NORMAL
		self.StationNameFont.Weight = wx.FONTWEIGHT_BOLD 
		self.StationNameFont.Underline = False
		self.StationNameFont.Facename = 'Arial'
		self.StationNameFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.StationNameFont.Color = '#AAAA00'

		self.StationFreqFont = FontSettings()
		self.StationFreqFont.Size = 55
		self.StationFreqFont.Family = wx.FONTFAMILY_DEFAULT
		self.StationFreqFont.Style = wx.FONTSTYLE_NORMAL
		self.StationFreqFont.Weight = wx.FONTWEIGHT_BOLD 
		self.StationFreqFont.Underline = False
		self.StationFreqFont.Facename = 'Arial'
		self.StationFreqFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.StationFreqFont.Color = '#FFFF00'
		
		self.NumericFreqFont = FontSettings()
		self.NumericFreqFont.Size = 25
		self.NumericFreqFont.Family = wx.FONTFAMILY_DEFAULT
		self.NumericFreqFont.Style = wx.FONTSTYLE_NORMAL
		self.NumericFreqFont.Weight = wx.FONTWEIGHT_BOLD 
		self.NumericFreqFont.Underline = False
		self.NumericFreqFont.Facename = 'Arial'
		self.NumericFreqFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.NumericFreqFont.Color = '#FFFFFF'
		
		self.NumericFreqFontBackgroundColor = '#AAAAAA'

		self.SpeedDialUnassignedFont = FontSettings()
		self.SpeedDialUnassignedFont.Size = 11
		self.SpeedDialUnassignedFont.Family = wx.FONTFAMILY_DEFAULT
		self.SpeedDialUnassignedFont.Style = wx.FONTSTYLE_NORMAL
		self.SpeedDialUnassignedFont.Weight = wx.FONTWEIGHT_NORMAL
		self.SpeedDialUnassignedFont.Underline = False
		self.SpeedDialUnassignedFont.Facename = 'Arial'
		self.SpeedDialUnassignedFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.SpeedDialUnassignedFont.Color = '#888888'
		
		self.SpeedDialAssignedFont = FontSettings()
		self.SpeedDialAssignedFont.Size = 12
		self.SpeedDialAssignedFont.Family = wx.FONTFAMILY_DEFAULT
		self.SpeedDialAssignedFont.Style = wx.FONTSTYLE_NORMAL
		self.SpeedDialAssignedFont.Weight = wx.FONTWEIGHT_BOLD  
		self.SpeedDialAssignedFont.Underline = True
		self.SpeedDialAssignedFont.Facename = 'Arial'
		self.SpeedDialAssignedFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.SpeedDialAssignedFont.Color = '#333333'
		
		self.StationListFont = FontSettings()
		self.StationListFont.Size = 15
		self.StationListFont.Family = wx.FONTFAMILY_DEFAULT
		self.StationListFont.Style = wx.FONTSTYLE_NORMAL
		self.StationListFont.Weight = wx.FONTWEIGHT_NORMAL  
		self.StationListFont.Underline = True
		self.StationListFont.Facename = 'Arial'
		self.StationListFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.StationListFont.Color = '#FFFFFF'
		self.StationListPressColor = [120,120,120]
		self.StationListBackgroundColour = '#DDDDDD'
		self.StationListSelectedBackgroundColour = '#5555FF'
		self.StationListSelectedForegroundColour = '#FFFFFF'
		
		self.StereoMonoBrightColor = '#FFFFFF'
		self.StereoMonoDimColor = '#666666'
		
		self.SignalBarBrightColor = '#FFFF55'
		self.SignalBarDimColor = '#555500'
		
		self.SpeedDialRows = 3
		self.StationsPerSpeedDialRow = 10
		
		self.MinAcceptableStationSignalStrength = 40
		self.ScanStepKHz = 50
		self.ScanFrequencySeparationThresholdMHz = 0.25
		
		self.SetSpeedDialPressTimeSecs = 1
		# self.UnSetSpeedDialPressTimeSecs = 10
		self.CancelSpeedDialPressTimeSecs = 4
		#self.RefreshDisplayMillisecs = 1000
		
		self.offVolumeBackgroundColour = '#555555'
		self.onVolumeBackgroundColour = '#FFFF55'
		
		self.pulseaudioRadioSourceName = 'FM_Radio'
		
		self.radioDevice = '/dev/radio0'
		
		self.zappTimerMSecs = 5000
		
		self.ScanWaitTimeMSecs = 100

	def Load( self ):
		with open( Settings.Filename, mode='r' ) as f:
			settingsDict = {}
			dict = json.load( f )
			#pprint.pprint( dict )
			for key, value in dict.items():
				fs = FontSettings()
				if( fs.FromDict( value ) ):
					settingsDict[key] = fs
				else:
					settingsDict[key] = value
			self.__dict__ = settingsDict

	def Save(self):
		with open( Settings.Filename, mode='w' ) as f:
			json.dump( self.__dict__, f, indent=2, cls=MyEncoder )

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, FontSettings):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__        
        
if __name__ == "__main__":
    s = Settings()
    #s.Load()
    #json.dumps( s.__dict__, indent=2, cls=MyEncoder )
    # pprint.pprint( s.RDSFont.Size )
    # pprint.pprint( s.StationNameFont )
    # pprint.pprint( s.StationFreqFont )
    # pprint.pprint( s.NumericFreqFont )
    # pprint.pprint( s.SpeedDialUnassignedFont )
    # pprint.pprint( s.SpeedDialAssignedFont )
    # pprint.pprint( s.StationListFont )
    s.Save()
