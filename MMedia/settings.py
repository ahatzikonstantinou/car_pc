#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
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
	'''These are the settings of the mmedia'''

	Filename = 'settings.mmedia' #the file were the settings are saved

	def __init__( self ):
		#self.device_ready_loaded_color = '#00FF00'
		#self.device_ready_not_loaded_color = '#FF0000'
		self.device_button_pressed_background_colour = 'black'
		self.device_button_unpressed_background_colour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND )
		self.device_button_pressed_text_colour = '#00FF00'
		self.device_button_unpressed_text_colour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) 
		
		self.TXTFont = FontSettings()        
		self.TXTFont.Size = 20
		self.TXTFont.Family = wx.FONTFAMILY_DEFAULT
		self.TXTFont.Style = wx.FONTSTYLE_NORMAL
		self.TXTFont.Weight = wx.FONTWEIGHT_NORMAL
		self.TXTFont.Underline = False
		self.TXTFont.Facename = 'Verdana'
		self.TXTFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.TXTFont.Color = '#AAAA00'
		
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
		
		self.StereoMonoBrightColor = '#FFFFFF'
		self.StereoMonoDimColor = '#666666'

		self.SetSpeedDialPressTimeSecs = 1
		# self.UnSetSpeedDialPressTimeSecs = 10
		self.CancelSpeedDialPressTimeSecs = 4
		#self.RefreshDisplayMillisecs = 1000
		
		self.offVolumeBackgroundColour = '#555555'
		self.onVolumeBackgroundColour = '#FFFF55'

		self.zappTimerMSecs = 5000

		self.FilelistFont = FontSettings()
		self.FilelistFont.Size = 12
		self.FilelistFont.Family = wx.FONTFAMILY_DEFAULT
		self.FilelistFont.Style = wx.FONTSTYLE_NORMAL
		self.FilelistFont.Weight = wx.FONTWEIGHT_NORMAL  
		self.FilelistFont.Underline = False
		self.FilelistFont.Facename = 'Arial'
		self.FilelistFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.FilelistFont.Color = '#334455'
		self.FilelistDisabledFontColor = '#777788'
		self.FilelistPressColor = [120,120,120]
		self.FilelistBackgroundColour = '#DDDDDD'
		self.FilelistSelectedBackgroundColour = '#5555FF'
		self.FilelistSelectedForegroundColour = '#FFFFFF'
		
		self.FilelistFileIsPlaylistFont = FontSettings()
		self.FilelistFileIsPlaylistFont.Size = 12
		self.FilelistFileIsPlaylistFont.Family = wx.FONTFAMILY_DEFAULT
		self.FilelistFileIsPlaylistFont.Style = wx.FONTSTYLE_NORMAL
		self.FilelistFileIsPlaylistFont.Weight = wx.FONTWEIGHT_BOLD  
		self.FilelistFileIsPlaylistFont.Underline = False
		self.FilelistFileIsPlaylistFont.Facename = 'Arial'
		self.FilelistFileIsPlaylistFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.FilelistFileIsPlaylistFont.Color = '#334455'
		
		self.PlaylistFont = FontSettings()
		self.PlaylistFont.Size = 12
		self.PlaylistFont.Family = wx.FONTFAMILY_DEFAULT
		self.PlaylistFont.Style = wx.FONTSTYLE_NORMAL
		self.PlaylistFont.Weight = wx.FONTWEIGHT_NORMAL  
		self.PlaylistFont.Underline = False
		self.PlaylistFont.Facename = 'Arial'
		self.PlaylistFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.PlaylistFont.Color = '#334455'
		self.PlaylistDisabledFontColor = '#AAAAAA'
		self.PlaylistPressColor = [120,120,120]
		self.PlaylistBackgroundColour = '#DDDDDD'
		self.PlaylistSelectedBackgroundColour = '#5555FF'
		self.PlaylistSelectedForegroundColour = '#FFFFFF'
		
		self.PlaylistTitleFont = FontSettings()
		self.PlaylistTitleFont.Size = 14
		self.PlaylistTitleFont.Family = wx.FONTFAMILY_ROMAN #wx.FONTFAMILY_DEFAULT
		self.PlaylistTitleFont.Style = wx.FONTSTYLE_NORMAL
		self.PlaylistTitleFont.Weight = wx.FONTWEIGHT_BOLD #wx.FONTWEIGHT_NORMAL  
		self.PlaylistTitleFont.Underline = False
		self.PlaylistTitleFont.Facename = 'Times'
		self.PlaylistTitleFont.Encoding = wx.FONTENCODING_SYSTEM        
		self.PlaylistTitleFont.Color = '#FFFFFF'
		self.PlaylistTitleBackgroundColour = '#9999AA'
		
		self.samba_domain = 'WORKGROUP'
		self.samba_username = 'antonis'
		self.samba_password = '312ggp12'
		
	def Load( self ):
		if( not os.path.isfile( Settings.Filename ) ):
			return
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
    # pprint.pprint( s.TXTFont.Size )
    # pprint.pprint( s.StationNameFont )
    # pprint.pprint( s.StationFreqFont )
    # pprint.pprint( s.NumericFreqFont )
    # pprint.pprint( s.SpeedDialUnassignedFont )
    # pprint.pprint( s.SpeedDialAssignedFont )
    # pprint.pprint( s.StationListFont )
    s.Save()
