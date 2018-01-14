#!/usr/bin/python
# -*- coding: utf-8 -*-

# gui.py

import wx
import sys
import os
import operator
import time
import pprint
import wx.lib.platebtn as platebtn
import wx.lib.buttons as libButtons
import wx.lib.scrolledpanel as scrolled
from threading import *
import logging
logging.basicConfig( level = logging.DEBUG ) #, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' )

from state import *
from settings import *
from device_builder import *
from devices_list import *
#from radio import *
from sounds import *
from wx.lib.pubsub import Publisher
from custom_controls import *
from usb import *
from track_hash_observer import *
from mount_detector import *

from speeddial_popup import *
from settings_control import *

from samba_settings_dlg import *
from a2dp import *

#import traceback

class MediaButton():
	def __init__( self, function_name, order, wx_button, unpressed_image, pressed_image, 
			is_pressed = False, is_navigation = False, callback_functions = None, 
			requires_loaded_media = True ):
		self.function_name = function_name
		self.order = order
		self.wx_button = wx_button
		self.pressed_image = pressed_image
		self.unpressed_image = unpressed_image
		self.is_pressed = is_pressed
		self.is_navigation = is_navigation
		self.callback_functions = callback_functions
		self.requires_loaded_media = requires_loaded_media
		
	def IsToggle( self ):
		return self.unpressed_image != self.pressed_image
		
	@staticmethod
	def ToDevMediaFunction( media_buttons ):
		'''
		Returns a dictionary that only contains the media functio name as key
		and the callback as value
		'''
		dev_media_functions = {}
		for function, media_button in media_buttons.iteritems():
			dev_media_functions[function] = [True, [media_button.callback_functions]]
			print( 'added {} to dev_media_functions'.format( function ) )
		return dev_media_functions
		
class MMediaGui(wx.Frame):
	PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME = 'update_text_display_message'
	PUBLISHER_REFRESH_MEDIA_BUTTON = 'refresh_media_button'
	
	#A list containing playlist functions
	_playlist_functions = [ 'new', 'clear', 'save', 'add', 'edit', 'delete', 'scan', 'cd_to_dir' ]
	
	#A list containing filelist functions
	_filelist_functions = [ 'move_up_folder', 'play_all', 'play_selected', 'refresh' ]
	
	#A list containing system playlist functions
	_system_playlist_functions = [ 'delete' ]
		
	def __init__(self, parent, title):	
		super(MMediaGui, self).__init__(parent, title=title, size=(750, 420))

		self._media_buttons = {
			'zap': MediaButton( 'zap', 0, None, 'no_flash.png', 'flash.png', callback_functions = [wx.EVT_BUTTON, self.ToggleZapp] ),
			'play': MediaButton( 'play', 1, None, 'play.png', 'pause.png' ),
			'rewind': MediaButton( 'rewind', 2, None, 'previous.png', 'previous.png' ),
			'forward': MediaButton( 'forward', 3, None, 'next.png', 'next.png' ),
			'previous': MediaButton( 'previous', 4, None, 'first.png', 'first.png', is_navigation = True ),
			'next': MediaButton( 'next', 5, None, 'last.png', 'last.png', is_navigation = True ),
			'step_back': MediaButton( 'step_back', 6, None, 'media_step_back.png', 'media_step_back.png', is_navigation = True ),
			'step_forward': MediaButton( 'step_forward', 7, None, 'media_step_forward.png', 'media_step_forward.png', is_navigation = True ),
			'speeddial_previous': MediaButton( 'speeddial_previous', 8, None, 'media_step_back.png', 'media_step_back.png', is_navigation = True, callback_functions = [wx.EVT_BUTTON, self.SpeedDialBack] ),
			'speeddial_next': MediaButton( 'speeddial_next', 9, None, 'media_step_forward.png', 'media_step_forward.png', is_navigation = True, callback_functions = [wx.EVT_BUTTON, self.SpeedDialForward] ),
			'playlist_previous': MediaButton( 'playlist_previous', 10, None, 'media_step_back.png', 'media_step_back.png', is_navigation = True, callback_functions = [wx.EVT_BUTTON, self.PlayTrackPreviousListStation] ),
			'playlist_next': MediaButton( 'playlist_next', 11, None, 'media_step_forward.png', 'media_step_forward.png', is_navigation = True, callback_functions = [wx.EVT_BUTTON, self.PlayTrackNextListStation] ),
			'subtitles': MediaButton( 'subtitles', 12, None, 'text.png', 'text.png', callback_functions = [wx.EVT_BUTTON, self.OnSubtitles] ),
			'shuffle': MediaButton( 'shuffle', 13, None, 'no_shuffle.png', 'shuffle.png' ),
			'repeat': MediaButton( 'repeat', 14, None, 'no_repeat.png', 'repeat.png' ),
			'eject': MediaButton( 'eject', 15, None, 'open.png', 'open.png', requires_loaded_media = False )
		}

		self.numPadKeys = {}
		self.speeddial_buttons = []
		
		self._current_device= None
		self.playing = False
		
		self.playerLock = RLock()	#this lock is required in order to use the libvlc player
		
		#load the settings
		self.Settings = Settings()
		self.Settings.Load()
		
		#build the devices
		dl = DeviceList( 
			dev_media_functions = MediaButton.ToDevMediaFunction( self._media_buttons ), 
			mmedia_gui = self, 
			error_reporter = ErrorReporter( MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME ), 
			message_reporter = MessageReporter( MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME ),
			GetSelectedSystemPlaylistItemsCallback = self.GetSelectedSystemPlaylistItems,
			playerLock = self.playerLock
		)#, playlist_select_callback = self._ListSelectTrack,  )
		dl.Load()
		abstract_devices = dl.devices
		print( 'abstract_devices:' )
		for d in abstract_devices:
			print( d.Hash() )

		self.a2dp_provider = A2DPProvider()
		
		#dev_builder = TestDeviceBuilder( MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME )
		self.dev_builder = DeviceBuilder( 
				MediaButton.ToDevMediaFunction( self._media_buttons ), 
				self, 
				error_reporter=ErrorReporter( MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME ),
				message_reporter = MessageReporter ( MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME ),
				publisher_text_display_message_name = MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME,
				GetSelectedListFilesCallback = self.GetSelectedListFiles,
				SetPlaylistLabelTextCallback = self.SetPlaylistLabelText,
				GetSelectePlaylistItemsCallback = self.GetSelectePlaylistItems,
				GetSelectedSystemPlaylistItemsCallback = self.GetSelectedSystemPlaylistItems,
				playerLock = self.playerLock,
				a2dp_provider = self.a2dp_provider #,
				#DeviceAddedCallback = self.DeviceAddedCallback, 
				#DeviceRemovedCallback = self.DeviceRemovedCallback
			)
		# Set up event handler for any DeviceBuilder thread events
		EVT_DEVICE_ADD( self, self.DeviceAddedCallback )
		EVT_DEVICE_DELETE( self, self.DeviceRemovedCallback )
		
		self.devices = {}
		#first add devices from device_list file
		dev_index = 0
		for dev in abstract_devices:
			device = self.dev_builder.Build( dev )
			device.index = dev_index
			dev_index += 1			
			self.devices[ device.Hash() ] = device
			print( 'added list device: {} (index:{})'.format( device.Hash(), device.index ) )
		#then add discovered removable usb devices
		#for disk in usb_discover.USBDiscoverer.GetMountedUSBDisks():
			#device = self.dev_builder.UsbFromUSBDisk( disk )
		logging.debug( 'mounts: {}'.format( str( len( MountDetector.GetMounts() ) ) ) )
		for mount in MountDetector.GetMounts():
			device = self.dev_builder.GetDeviceFromMount( mount )
			device.index = dev_index
			dev_index += 1
			self.devices[ device.Hash() ] = device
			logging.debug( 'added auto discovered mount: {} (index:{})'.format( device.Hash(), device.index ) )	
			
		for a2dp_device in self.dev_builder.GetA2DPDevices():
			a2dp_device.index = dev_index
			dev_index += 1
			self.devices[ a2dp_device.Hash() ] = a2dp_device
			logging.debug( 'a2dp source: {} (index:{})'.format( a2dp_device.Hash(), a2dp_device.index ) )	
			
		self.device_buttons = {} #a dictionary storing wx.buttons that activate a device, key: device.Hash()
			
		self.current_active_list = None

		#load the last saved state
		self.State = State()
		self.State.Load()		

		self.zapp_is_on = False
		self.ZappTimer = wx.Timer( self )
		self.zappCallback = None
		self.zapp_media_button = None

		self.video_only = False
		
		self.trackHashObservers_threadProxy = TrackHashObserversThreadProxy()

		#start a samba provider to be used with the network settings dialog
		#and also start a samba monitor thread that automounts any predefined smanba shares
		self.samba_provider = SambaProvider( self.Settings.samba_domain, self.Settings.samba_username, self.Settings.samba_password )
		SambaAutomountThread( self.samba_provider )
		
		self.InitUI()
		self.Centre()
		self.Show()
		
		#Give a chance to any device that requires to initialize stuff after the parent is Shown
		for key, device in self.devices.iteritems():
			device.MainFrameInitUIFinished()
			self._HideDeviceVideoControlPanels( device )
			
		if( self.State.current_device_hash and
			self.devices.has_key( self.State.current_device_hash )
		):
			self._SetCurrentDeviceByHash( self.State.current_device_hash, True )
		else:
			for h in self.devices.keys():
				self._SetCurrentDeviceByHash( h, True )
				break
				
		self.__sounds = Sounds()
		
		self.setSpeedDialTimer = wx.Timer( self )
		self.Bind( wx.EVT_TIMER, self.SetSpeedDialTimerFinished, self.setSpeedDialTimer )
		# self.unsetSpeedDialTimer = wx.Timer( self )
		# self.Bind( wx.EVT_TIMER, self.ResetUnsetSpeedDialTimer, self.unsetSpeedDialTimer )
		#self.cancelSpeedDialTimer = wx.Timer( self )
		#self.Bind( wx.EVT_TIMER, self.CancelSpeedDialTimerFinished, self.cancelSpeedDialTimer )
		
		Publisher().subscribe( self.UpdateTextDisplay, MMediaGui.PUBLISHER_TEXT_DISPLAY_MESSAGE_NAME )
		Publisher().subscribe( self._OnRefreshMediaButton, MMediaGui.PUBLISHER_REFRESH_MEDIA_BUTTON )	
				
	def ReLayoutUI( self ):
		self.ShowHideScrollDevButtons()
		self.rootSizer.Layout()
		self.Fit()
		
	def ShowHideScrollDevButtons( self ):
		'''
		Show/hide the left/right scroll buttons for the device button list
		'''
		client_size_x, client_size_y = self.devPanel.GetClientSize()
		virtual_size_x, virtual_size_y = self.devPanel.GetVirtualSize()
		#logging.debug( 'virtual_size: ({},{}), client_size: ({},{})'.format( virtual_size_x, virtual_size_y, client_size_x, client_size_y ) )
		if( client_size_x >= virtual_size_x ):
			self.rightDevScrollButton.Hide()
			self.leftDevScrollButton.Hide()
		else:
			self.rightDevScrollButton.Show()
			self.leftDevScrollButton.Show()
			
	def InitUI(self):
		self.rootPanel = wx.Panel(self)
		
		self.rootSizer = wx.BoxSizer( wx.VERTICAL )
		self.rootPanel.SetSizer( self.rootSizer )

		#top buttons strip
		self.topPanel = wx.Panel( self.rootPanel )
		topSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.topPanel.SetSizer( topSizer )
		
		#Add devices buttons strip
		dev_container_panel = wx.Panel( self.topPanel )
		dev_container_sizer = wx.BoxSizer( wx.HORIZONTAL )
		dev_container_panel.SetSizer( dev_container_sizer )
		
		self.devPanel = scrolled.ScrolledPanel( dev_container_panel )
		self.devSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.devPanel.SetSizer( self.devSizer )
		self.devPanel.SetAutoLayout(1)
		self.devPanel.SetupScrolling()
		self._AddDeviceButtons( self.devPanel, self.devSizer )
		
		self.leftDevScrollButton = wx.BitmapButton( dev_container_panel, bitmap = GetImage( 'navigate_left.png', '16x16' ) )
		def OnLeftScroll( event ):
			x,y = self.devPanel.GetViewStart()
			self.devPanel.Scroll( x-1, -1 )	
		self.leftDevScrollButton.Bind( wx.EVT_LEFT_UP, OnLeftScroll )
		self.rightDevScrollButton = wx.BitmapButton( dev_container_panel, bitmap = GetImage( 'navigate_right.png', '16x16' ) )
		def OnRightScroll( event ):
			x,y = self.devPanel.GetViewStart()
			self.devPanel.Scroll( x+1, -1 )	
		self.rightDevScrollButton.Bind( wx.EVT_LEFT_UP, OnRightScroll )
		dev_container_sizer.Add( self.leftDevScrollButton, 0, wx.EXPAND )
		dev_container_sizer.Add( self.devPanel, 1, wx.EXPAND )
		dev_container_sizer.Add( self.rightDevScrollButton, 0, wx.EXPAND )
		
		#Add settings button
		rtPanel = wx.Panel( self.topPanel )
		rtSizer = wx.BoxSizer( wx.HORIZONTAL )
		rtPanel.SetSizer( rtSizer )
		self._settings_button = self._AddSettingsButton( rtPanel, rtSizer )
		self._network_button = wx.ToggleButton( rtPanel, label = 'Network' )
		self._network_button.Bind(  wx.EVT_TOGGLEBUTTON, self.ToggleNetworkSettings )
		rtSizer.Add( self._network_button )
		
		#topSizer.Add( self.devPanel, 1, wx.EXPAND | wx.BOTTOM, border = 0 )
		topSizer.Add( dev_container_panel, 1, wx.EXPAND | wx.BOTTOM, border = 0 )
		#topSizer.Add( (1,1), 1, wx.EXPAND )
		topSizer.Add( rtPanel, 0, wx.EXPAND )
				
		self.rootSizer.Add( self.topPanel, 0, wx.EXPAND|wx.BOTTOM, border = 0 )
		
		#Add the rest
		self.samba_settings_panel = SambaSettingsPanel( self.rootPanel, samba_provider = self.samba_provider )
		self.rootSizer.Add( self.samba_settings_panel, 1, wx.EXPAND | wx.TOP, border = 0 )
		self.samba_settings_panel.Hide()
		
		self.media_widgets_panel = wx.Panel( self.rootPanel )
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.media_widgets_panel.SetSizer( sizer )
		self.rootSizer.Add( self.media_widgets_panel, 1, wx.EXPAND | wx.TOP, border = 0 )
		
		lbox = wx.BoxSizer( wx.VERTICAL )
		sizer.Add( lbox, 5, wx.EXPAND, 2 )		

		#rbox will contain the tracklists (tracks/files/etc)
		self.rbox = wx.BoxSizer(wx.VERTICAL)
		sizer.Add( self.rbox, 2, wx.EXPAND, 2 )		
		#demo
		#rt = wx.Button( self.media_widgets_panel, label='rbox' )
		#self.rbox.Add( rt, 1, wx.EXPAND )
		self.list_buttons_panel = wx.Panel( self.media_widgets_panel )
		lbpSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.list_buttons_panel.SetSizer( lbpSizer )
		self.lists_panel = wx.Panel( self.media_widgets_panel )
		listsSizer = wx.BoxSizer( wx.VERTICAL )
		self.lists_panel.SetSizer( listsSizer )
		
		self._BuildLists( self.list_buttons_panel, self.lists_panel )
		self.rbox.Add( self.list_buttons_panel, 0, wx.EXPAND )
		self.rbox.Add( self.lists_panel, 1, wx.EXPAND )		

		displayPanel = wx.Panel( self.media_widgets_panel )
		displayPanel.SetBackgroundColour( '#000000' )
		displaySizer = wx.BoxSizer( wx.HORIZONTAL )
		displayPanel.SetSizer( displaySizer )
		lbox.Add( displayPanel, 10, wx.EXPAND | wx.TOP, border=0 )

		#lbox.Add( wx.StaticLine( self.media_widgets_panel ), 1, wx.EXPAND )
		#The media_controls_panel contains the scanpanel with forward, reverse etc
		#and the media control panel select mcp_select_panel which has one button
		#that shows/hides the media control buttons in 2 groups. The media control 
		#buttons are too many and there is not enough room for all to display at once
		#Each device specifies which buttons are displayed in each group
		self.media_buttons_panel = wx.Panel( self.media_widgets_panel )
		self.media_buttons_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.media_buttons_panel.SetSizer( self.media_buttons_sizer )
		
		self.scanPanel = wx.Panel( self.media_buttons_panel )
		#self.scanPanel.SetBackgroundColour( '#2244ff' )
		self.scanSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.scanPanel.SetSizer( self.scanSizer )
		self._BuildMediaButtonsPanel( self.scanPanel )
		self.mcp_select_panel = wx.Panel( self.media_buttons_panel )
		self._mcp_select_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.mcp_select_panel.SetSizer( self._mcp_select_sizer )
		self._mcp_button = wx.ToggleButton( self.mcp_select_panel, label='More' )
		self._mcp_button.Bind( wx.EVT_TOGGLEBUTTON, self.ToggleMediaButtonGroup )
		self._mcp_select_sizer.Add( self._mcp_button, 0, wx.EXPAND )
		self.media_buttons_sizer.Add( self.scanPanel, 0, wx.EXPAND )
		self.media_buttons_sizer.Add( (1,1), 1, wx.EXPAND )
		self.media_buttons_sizer.Add( self.mcp_select_panel, 0, wx.EXPAND )
		lbox.Add( self.media_buttons_panel, 4, wx.EXPAND|wx.ALL, 10 )
		
		#lbox.Add( wx.StaticLine( self.media_widgets_panel ), 1, wx.EXPAND )
		self.speedDialPanel = wx.Panel( self.media_widgets_panel )
		self.speedDialSizer = wx.BoxSizer( wx.VERTICAL )
		self.speedDialPanel.SetSizer( self.speedDialSizer )
		#demo
		#sdt = wx.Button( speedDialPanel, label='Speed Dial Panel' )
		#speedDialSizer.Add( sdt, 1, wx.EXPAND )
		
		self.speeddial_popup = SpeedDialPopup( self, self.speedDialPanel, 28 )		

		lbox.Add( self.speedDialPanel, 5, wx.EXPAND, 5 )
		
		self.settings_control = SettingsControl( self.media_widgets_panel, GetImage( 'button-minus.png' ), GetImage( 'button-plus.png' ) )
		lbox.Add( self.settings_control, 9, wx.EXPAND, 5 )
		self.settings_control.Hide()

		radioSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.radioPanel = wx.Panel( self.media_widgets_panel )
		self.radioPanel.SetBackgroundColour( '#000000' )
		self.radioPanel.SetForegroundColour( '#ffff00' )
		self.radioPanel.SetSizer( radioSizer )

		self.volumeControl = VolumeControl( self.media_widgets_panel, self.Settings, self.State, self._current_device )
		displaySizer.Add( self.volumeControl.GetControlPanel(), 0, wx.EXPAND, border=0 )
				
		rightDisplaySizer = wx.BoxSizer( wx.VERTICAL )
		displaySizer.Add( rightDisplaySizer, 4, wx.EXPAND, border=5 )
				
		rightDisplaySizer.Add( self.radioPanel, 6, wx.EXPAND | wx.ALIGN_CENTER )
		self.play_progress_bar = PlayProgress( self.media_widgets_panel )
		rightDisplaySizer.Add( self.play_progress_bar.GetWidget(), 0, wx.EXPAND | wx.RIGHT, border = 10 )
		#self.textDisplayPanel = self._BuildTextDisplay( self.media_widgets_panel )
		self.text_display = MarqueeText( self.media_widgets_panel, self.Settings.TXTFont )
		self.textDisplayPanel = self.text_display.GetPanel()		
		rightDisplaySizer.Add( self.textDisplayPanel, 2, wx.EXPAND | wx.RIGHT, border = 10 )
		
		#radioSizer.Add( self.BuildFrequencyDisplay( self.radioPanel ), 1, wx.EXPAND|wx.ALL, border=10 )
		self.numpad_observer = NumpadTrackHashObserver( self.numText )
		self.playlist_observer = PlaylistTrackHashObserver( self.playlist )
		self.trackHashObservers_threadProxy.AddTrackHashObserver( self.numpad_observer )
		self.trackHashObservers_threadProxy.AddTrackHashObserver( self.playlist_observer )

		for key, device in self.devices.iteritems():
			self._DeviceInitUI( device )
			
		self.ShowHideScrollDevButtons()
			
	def ToggleNetworkSettings( self, event ):
		if( event.GetEventObject().GetValue() ):	#pressed
			self.media_widgets_panel.Hide()
			self.samba_settings_panel.Refresh()
			self.samba_settings_panel.Show()
		else:
			self.media_widgets_panel.Show()
			self.samba_settings_panel.Hide()
		self.ReLayoutUI()
			
	def ToggleMediaButtonGroup( self, event ):
		if( not self._current_device ):
			return
			
		if( event.GetEventObject().GetValue() ):	#pressed
			self.DisplayMediaButtonGroup( 1 )			
		else:
			self.DisplayMediaButtonGroup( 0 )
			
	def DisplayMediaButtonGroup( self, media_button_group ):
		if( not self._current_device ):
			return
			
		group_buttons = self._current_device.GetMediaButtonsForGroup( media_button_group )
		for function_name, media_button in self._media_buttons.iteritems():
			button = media_button.wx_button
			if( function_name in group_buttons and self._current_device.SupportsMediaFunction( function_name ) ):
				button.Show()
			else:
				button.Hide()
		self.scanSizer.Layout()
			
	def SetPlayProgressDuration( self, duration ):
		'''
		This is expected to be a properly formated i.e. hh:mm:ss time string
		'''
		self.play_progress_bar.SetDuration( duration )
		
	def SetPlayProgressPosition( self, position, current_time ):
		'''
		position should be a an integer between [0 - 100]
		current_time should a properly formated i.e. hh:mm:ss time string
		'''
		self.play_progress_bar.SetTime( current_time )
		self.play_progress_bar.SetPosition( position )
		
	def DeviceAddedCallback( self, event ):
		try:
			print( 'received event {}'.format( event.__class__ ) )
			device = event.device
			if( self.devices.has_key( device.Hash() ) ):
				print( 'Cannot add a second device with hash: {}'.format( device.Hash() ) )
				#raise Exception( 'Cannot add a second device with hash: {}'.format( device.Hash() ) )
				return
			
			self.devices[ device.Hash() ] = device
			logging.debug( 'added device with hash {}'.format( device.Hash() ) )
			
			device.InitUI( self.radioPanel, self.media_widgets_panel, self.ToggleVideoOnly )
			device.MainFrameInitUIFinished()
			self._HideDeviceVideoControlPanels( device )
			print( 'about to add a button for device {}'.format( device.Hash() ) )
			button = self._BuildDevButton( self.devPanel, device )
			self.device_buttons[ device.Hash() ] = button	#will need this if the device is ever deleted, to also remove the button
			self.devSizer.Add( button )
			self.ReLayoutUI()
			print( 'added a button and refreshed self.devSizer for device {}'.format( device.name ) )
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
	def DeviceRemovedCallback( self, event ):
		try:
			print( 'received event {}'.format( event.__class__ ) )
			dev_key = None
			for k,d in self.devices.iteritems():
				if( event.device_path is not None ):
					#logging.debug( 'Removing device by path {}'.format( event.device_path ) )
					if( d.dev_path == event.device_path ):
						dev_key = k
						break
				else:
					#logging.debug( 'Removing device by name {}'.format( event.device_name ) )
					if( d.name == event.device_name ):
						dev_key = k
						break
			
			if( dev_key ):
				button = self.device_buttons[ dev_key ]
				button.Destroy()
				del self.device_buttons[ dev_key ]
				activate_another_device = False
				if( self._current_device and self._current_device == self.devices[ dev_key ] ):
					activate_another_device = True
				del self.devices[ dev_key ]
				if( activate_another_device ):
					if( len( self.devices.keys() ) > 0 ):
						key = self.devices.keys()[0]
						self._SetCurrentDeviceByDevice( self.devices[ key ] )
				self.ReLayoutUI()
				print( 'Found an associated device button, destroyed it, deleted it, and refreshed the sizer' )				
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
	def _DeviceInitUI( self, device ):
		device.InitUI( self.radioPanel, self.media_widgets_panel, self.ToggleVideoOnly )
		device.AddTrackHashObserver( self.trackHashObservers_threadProxy )
			
	def _HideDeviceVideoControlPanels( self, device ):
		dev_video_panel = device.GetVideoPanel()
		if( dev_video_panel ):
			dev_video_panel.Hide()
		dev_controls_panel = device.GetControlsPanel()
		if( dev_controls_panel ):
			dev_controls_panel.Hide()
			
	def ToggleVideoOnly( self, event = None ):
		'''Toggle show/hide all controls to leave only video full screen'''
		self.video_only = not self.video_only
		print( 'ToggleVideoOnly called. Now self.video_only: {}'.format( self.video_only ) )
		if( self.video_only ):
			self.topPanel.Hide() 
			self.list_buttons_panel.Hide()
			self.lists_panel.Hide() 
			self.media_buttons_panel.Hide()
			self.volumeControl.GetControlPanel().Hide() 
			self.textDisplayPanel.Hide()
			if( self._current_device.SupportsCapability( 'play_progress' ) ):
				self.play_progress_bar.Hide()
			if( self._current_device.SupportsCapability( 'speeddial' ) and self._current_device.settings.GetSpeedDialButtonTotal() > 0 ):
				self.speedDialPanel.Hide()
		else:
			self.topPanel.Show() 
			self.list_buttons_panel.Show()
			self.lists_panel.Show() 
			self.media_buttons_panel.Show()
			self.volumeControl.GetControlPanel().Show() 
			self.textDisplayPanel.Show()
			if( self._current_device.SupportsCapability( 'play_progress' ) ):
				self.play_progress_bar.Show()
			if( self._current_device.SupportsCapability( 'speeddial' ) ):
				self.speedDialPanel.Show()
		#self.rootSizer.Layout()
		self.ReLayoutUI()
		logging.debug( 'self.radioPanel size:{}'.format( self.radioPanel.GetClientSize() ) )

	def _SetCurrentDeviceByHash( self, device_hash, update_dev_buttons ):
		if( self.devices.has_key( device_hash ) ):
			self._SetCurrentDeviceByDevice( self.devices[ device_hash ] )
			
		if( update_dev_buttons ):
			for c in self.devPanel.GetChildren():
				#c.SetValue( False )
				if( c.device.Hash() == device_hash ):
					c.SetValue( True )
					break
			
	def _SetCurrentDeviceByDevice( self, device ):
		if( self._current_device is not None ):
			self._current_device.Deactivate()
			self._current_device.DelFilelistObserver( self.filelist )
			self._current_device.DelPlaylistObserver( self.playlist )
			self._current_device.DelSystemPlaylistsObserver( self.system_playlists )

		self.ClearTextDisplayMessage()
		
		self._current_device = device
		self._current_device.AddFilelistObserver( self.filelist )
		self._current_device.AddPlaylistObserver( self.playlist )
		self._current_device.AddSystemPlaylistsObserver( self.system_playlists )

		self.ZappReset()
		
		self.volumeControl.SetDevice( self._current_device )
			
		self._RefreshLists()
		
		self._current_device.Activate()
		self.device_buttons[ self._current_device.Hash() ].SetValue( True )
		
		#print( 'self._current_device is {}, and its state is {}'.format( self._current_device.__class__, self._current_device.state.__class__ ) )
		self._BuildSpeedDials( self._current_device.settings, self._current_device.state.speed_dials, 
			self.speedDialPanel )
						
		self._UpdateMediaButtons()
		self.DisplayMediaButtonGroup(0)
		self._mcp_button.SetValue( False )
		if( len( self._current_device.GetMediaButtonsForGroup( 1 ) ) == 0 ): #all media buttons are in one group
			self._mcp_button.Hide()
		else:
			self._mcp_button.Show()
		
		if( self._current_device.SupportsCapability( 'play_progress' ) ):
			self.play_progress_bar.Show()
			self.play_progress_bar.Reset()
		else:
			self.play_progress_bar.Hide()
		
		self.State.SetCurrentDeviceHash( self._current_device.Hash() )
		
		self.rootPanel.GetSizer().Layout()
			
	def _AddDeviceButtons( self, panel, sizer ):
		devices = sorted( self.devices.values(), key=lambda x: x.index ) 
		for d in devices:
			b = self._BuildDevButton( panel, d )
			self.device_buttons[ d.Hash() ] = b	#will need this if the device is ever deleted, to also remove the button
			sizer.Add( b, 0, border = 0 )
	
	def _AddSettingsButton( self, panel, sizer ):
		b = wx.ToggleButton( panel, label='Settings' )
		b.Bind( wx.EVT_TOGGLEBUTTON, self.OnSettings )
		sizer.Add( b )
		return b
		
	def OnSettings( self, event ):
		#ask the device for its settings control panel
		#hide the media_button and speeddial panels
		if( event.GetEventObject().GetValue() ):
			self.media_buttons_panel.Hide()
			self.speedDialPanel.Hide()
			self.settings_control.Show()
		else:
			self.media_buttons_panel.Show()
			self.speedDialPanel.Show()
			self.settings_control.Hide()
		self.ReLayoutUI()
		
	def _BuildDevButton( self, panel, device ):
		button = ToggleRadioButton( panel, label=device.name, 
			pressed_background_colour = self.Settings.device_button_pressed_background_colour,
			unpressed_background_colour = self.Settings.device_button_unpressed_background_colour,
			pressed_text_colour = self.Settings.device_button_pressed_text_colour,
			unpressed_text_colour = self.Settings.device_button_unpressed_text_colour
			 )#, callback=self._DeviceButtonCallback )
		button.device = device
		button.Bind( wx.EVT_TOGGLEBUTTON, self._DeviceButtonCallback )
		
		#if( device.NeedsMedia() ):
			#if( device.HasMedia() ):
				#button.SetForegroundColour( self.Settings.device_ready_loaded_color )
			#else:
				#button.SetForegroundColour( self.Settings.device_ready_not_loaded_color )
				##button.Disable()
		#else:
			#button.SetForegroundColour( self.Settings.device_ready_loaded_color )
			
		return button
		
	def _DeviceButtonCallback( self, event ):
		button = event.GetEventObject()
			
		self._SetCurrentDeviceByDevice( button.device )
		
		#Note: this is necessary because ToggleRadioButton also has a EVT_TOGGLEBUTTON handler
		event.Skip()	
	
	def _BuildLists( self, buttons_panel, lists_panel ):
		'''This function builds the gui with ToggleRadioButton controls and associates widgets with the buttons.
		   The ToggleRadioButton inherent functionality handles the sibling ToggleRadioButton and the 
		   hiding-showing of the associated widgets, so no event binding is necessary.
		'''
		buttons_sizer = buttons_panel.GetSizer()
		#lists_sizer = lists_panel.GetSizer()
		
		#self.filelist_button = wx.ToggleButton( buttons_panel, wx.ID_ANY, label='Files' )
		self.filelist_widget = self._BuildFilelist( lists_panel )
		self.filelist_button = ToggleRadioButton( 
			buttons_panel, 
			wx.ID_ANY, 
			label='Files', 
			associated_object = self.filelist,
			associated_widget = self.filelist_widget, 
			press_callback = self.SetCurrentActiveList 
		)
		#self.filelist_button.Bind( wx.EVT_TOGGLEBUTTON, self._ToggleListButtons )
		self.filelist_button.panel = self.filelist_widget
		buttons_sizer.Add( self.filelist_button )
		
		#self.playlist_button = wx.ToggleButton( buttons_panel, wx.ID_ANY, label='Playlist' )
		self.playlist_widget = self._BuildPlaylist( lists_panel )
		self.playlist_button = ToggleRadioButton( 
			buttons_panel, 
			wx.ID_ANY, 
			label='Now Playing', 
			associated_object = self.playlist,
			associated_widget = self.playlist_widget, 
			press_callback = self.SetCurrentActiveList 
		)
		#self.playlist_button.Bind( wx.EVT_TOGGLEBUTTON, self._ToggleListButtons )
		self.playlist_button.panel = self.playlist_widget
		buttons_sizer.Add( self.playlist_button )

		#self.system_playlists_button = wx.ToggleButton( buttons_panel, wx.ID_ANY, label='Playlist' )
		self.system_playlists_widget = self._BuildSystemPlaylists( lists_panel )
		self.system_playlists_button = ToggleRadioButton( 
			buttons_panel, 
			wx.ID_ANY, 
			label='Playlists', 
			associated_object = self.system_playlists,
			associated_widget = self.system_playlists_widget, 
			press_callback = self.SetCurrentActiveList 
		)
		#self.system_playlists_button.Bind( wx.EVT_TOGGLEBUTTON, self._ToggleListButtons )
		self.system_playlists_button.panel = self.system_playlists_widget
		buttons_sizer.Add( self.system_playlists_button )

		#self.numpad_button = wx.ToggleButton( buttons_panel, wx.ID_ANY, label='Numpad' )
		self.numpad_panel = self._BuildNumpad( lists_panel )
		self.numpad_button = ToggleRadioButton( buttons_panel, wx.ID_ANY, label='Numpad', associated_widget=self.numpad_panel )
		#self.numpad_button.Bind( wx.EVT_TOGGLEBUTTON, self._ToggleListButtons )
		self.numpad_button.panel = self.numpad_panel
		buttons_sizer.Add( self.numpad_button )		
		
	def _RefreshLists( self ):
		logging.debug( 'gui._RefreshLists starting for device {}...'.format( self._current_device.name ) )
		if( self._current_device.SupportsCapability( 'numpad' ) ):
			self.numpad_panel.Show()
			self.numpad_button.Show()
			if( self._current_device.SupportsCapability( 'numpad_decimal' ) ):
				self.numpad_decimal_key.Show()
				self.numpad_decimal_key_placeholder.Hide()
			else:
				self.numpad_decimal_key.Hide()
				self.numpad_decimal_key_placeholder.Show()
		else:
			logging.debug( '\tdoes not support numpad' )
			self.numpad_panel.Hide()
			self.numpad_button.Hide()

		if( self._current_device.SupportsCapability( 'filesystem' ) ):
			#print( 'in _RefreshLists GetFilelistItems: {}'.format( self._current_device.GetFilelistItems() ) )
			self.filelist.SetItems( self._current_device.GetFilelistItems() )
			self.filelist.BindActions( self._current_device.GetFilelistActionCallbacks() )
			for filelist_function_name in MMediaGui._filelist_functions:
				self.filelist.ShowHideAction( filelist_function_name, self._current_device.SupportsFilelistFunction( filelist_function_name ) )
			self.filelist_widget.Show() #self.filelist.GetWidget().Show()
			self.filelist_button.Show()
			self.current_active_list = self.filelist
			self.playlist.ShowTitle( True )
			print( 'showing the playlist title' )
		else:
			logging.debug( '\tdoes not support filesystem' )
			self.filelist_widget.Hide()
			self.filelist_button.Hide()
			self.playlist.ShowTitle( False )
			print( 'hiding the playlist title' )
			
		if( self._current_device.SupportsCapability( 'system_playlist' ) ):
			self.system_playlists.SetItems( self._current_device.GetSystemPlaylists() )
			self.system_playlists.BindActions( self._current_device.GetSystemPlaylistActionCallbacks() )
			self.system_playlists_widget.Show()
			self.system_playlists_button.Show()
			#no further setup. Only one action supported so far 'Del'
		else:
			logging.debug( '\tdoes not support system_playlist' )
			self.system_playlists_widget.Hide()
			self.system_playlists_button.Hide()
			
		if( self._current_device.SupportsCapability( 'playlist' ) ):
			self.playlist.SetTitle( self._current_device.GetCurrentPlaylistName() )
			self.playlist.SetItems( self._current_device.GetPlaylistItems() )
			self.playlist.BindActions( self._current_device.GetPlaylistActionCallbacks() )
			self.playlist_button.Show()
			if( self._current_device.SupportsCapability( 'playlist_reordering' ) ):
				self.playlist.ShowReordering( True )
			else:
				self.playlist.ShowReordering( False )
			for playlist_function_name in MMediaGui._playlist_functions:
				self.playlist.ShowHideAction( playlist_function_name, self._current_device.SupportsPlaylistFunction( playlist_function_name ) )
			if( ( not self.filelist_widget.IsShown() ) ):
				self.playlist.GetWidget().Show()
				self.current_active_list = self.playlist
			else:
				self.playlist_widget.Hide()
		else:
			logging.debug( '\tdoes not support playlist' )
			self.playlist_widget.Hide()
			self.playlist_button.Hide()
			
		widgets = [ self.filelist_widget, self.numpad_panel, self.system_playlists_widget, self.playlist_widget ]
		shown_widgets_count = len( [ w for w in widgets if w.IsShown() ] )
		if( shown_widgets_count == 0 ):
			self.lists_panel.Hide()
			self.list_buttons_panel.Hide()
		else:
			self.lists_panel.Show()
			if( shown_widgets_count == 1 ):
				self.list_buttons_panel.Hide()
			else:
				self.list_buttons_panel.Show()
				if( self.playlist_widget.IsShown() ):
					self.playlist_button.SetValue( True )
				elif( self.filelist_widget.IsShown() ):
					self.filelist_button.SetValue( True )			
		
		#print( 'numpad_panel_show:{}, filelist_panel_show:{}, playlist_panel_show:{}'.format(
				#self.numpad_panel.IsShown(), self.filelist_widget.IsShown(), self.playlist_widget.IsShown() )
			#)				

		#self.list_buttons_panel.GetSizer().Layout()
		#self.lists_panel.GetSizer().Layout()
		self.ReLayoutUI()

	def _BuildNumpad( self, parent_panel ):
		panel = parent_panel
		sizer = panel.GetSizer()
		
		self.numPanel = wx.Panel( panel )
		self.numSizer = wx.BoxSizer( wx.VERTICAL )
		self.numPanel.SetSizer( self.numSizer )
		sizer.Add( self.numPanel, 1, wx.EXPAND|wx.ALL )

		numTextPanel = wx.Panel( self.numPanel )
		numTextPanel.SetBackgroundColour( self.Settings.NumericFreqFontBackgroundColor )
		numTextPanelS = wx.BoxSizer( wx.VERTICAL )
		numTextInnerSizer = wx.BoxSizer( wx.HORIZONTAL )
		numTextPanel.SetSizer( numTextPanelS )

		self.numText = wx.StaticText( numTextPanel, label = '555.55' )# str( self.State.frequency ) )
		self.numText.SetFont( self.Settings.NumericFreqFont.GetFont() )
		self.numText.SetForegroundColour(self.Settings.NumericFreqFont.Color)
		numTextPanelS.Add( numTextInnerSizer, 1, wx.EXPAND|wx.CENTRE, border = 5 )

		self.numTextWarningImage = wx.StaticBitmap( numTextPanel, wx.ID_ANY, GetImage( 'warning.png', '32x32' ) )
		numTextInnerSizer.Add( self.numTextWarningImage, 0, wx.ALL, border = 2 )
		self.numTextWarningImage.Hide()
		numTextInnerSizer.Add( (0,0),1,wx.EXPAND)
		numTextInnerSizer.Add( self.numText, 0, wx.ALIGN_RIGHT|wx.RIGHT, border = 10 )		

		row1s = wx.BoxSizer( wx.HORIZONTAL )
		row1s.Add( self._CreateNumPadKey( str( '7' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row1s.Add( self._CreateNumPadKey( str( '8' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row1s.Add( self._CreateNumPadKey( str( '9' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s = wx.BoxSizer( wx.HORIZONTAL )
		row2s.Add( self._CreateNumPadKey( str( '4' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s.Add( self._CreateNumPadKey( str( '5' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row2s.Add( self._CreateNumPadKey( str( '6' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s = wx.BoxSizer( wx.HORIZONTAL )
		row3s.Add( self._CreateNumPadKey( str( '1' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s.Add( self._CreateNumPadKey( str( '2' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row3s.Add( self._CreateNumPadKey( str( '3' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row4s = wx.BoxSizer( wx.HORIZONTAL )
		row4s.Add( self._CreateNumPadKey( str( '0' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		self.numpad_decimal_key = self._CreateNumPadKey( str( '.' ) )
		self.numpad_decimal_key_placeholder = wx.Panel( self.numPanel )
		self.numpad_decimal_key_placeholder.SetSizer( wx.BoxSizer( wx.VERTICAL ) )
		self.numpad_decimal_key_placeholder.GetSizer().Add( (0,0) )
		self.numpad_decimal_key_placeholder.Hide()
		row4s.Add( self.numpad_decimal_key, 1, wx.EXPAND|wx.ALL, 5 )
		row4s.Add( self.numpad_decimal_key_placeholder, 1, wx.EXPAND|wx.ALL, 5 )
		row4s.Add( self._CreateNumPadKey( str( 'Del' ) ), 1, wx.EXPAND|wx.ALL, 5 )
		row5s = wx.BoxSizer( wx.HORIZONTAL )
		row5s.Add( self._CreateNumPadKey( str( 'Enter' ) ), 2, wx.EXPAND|wx.ALL, 5 )		
		row5s.Add( self._CreateNumPadKey( str( 'Clear' ) ), 1, wx.EXPAND|wx.ALL, 5 )		

		self.numSizer.Add( numTextPanel, 1, wx.EXPAND|wx.ALL, 10 )
		self.numSizer.Add( row1s, 1, wx.EXPAND )
		self.numSizer.Add( row2s, 1, wx.EXPAND )
		self.numSizer.Add( row3s, 1, wx.EXPAND )
		self.numSizer.Add( row4s, 1, wx.EXPAND )
		self.numSizer.Add( row5s, 1, wx.EXPAND )
		
		sizer.Layout()
		#print( 'numpad was built' )
		return self.numPanel
		
	def _BuildFilelist( self, parent_panel ):
		self.filelist = MMediaList( parent_panel, self.Settings, type = MMediaList.FILELIST, 
			select_list_item_callback = self.PlayTrackFromList, actions = MMediaGui._filelist_functions )
		#print( 'filelist was built' )
		return self.filelist.GetWidget()
		
	def _BuildPlaylist( self, parent_panel ):
		self.playlist = MMediaList( parent_panel, self.Settings, 
			type = MMediaList.PLAYLIST, with_list_title = True, select_list_item_callback = self.PlayTrackFromList, 
			click_list_item_callback = self.OnClickedNowPlayingItem, actions = MMediaGui._playlist_functions )
		#print( 'playlist was built' )
		return self.playlist.GetWidget()
		
	def _BuildSystemPlaylists( self, parent_panel ):
		self.system_playlists = MMediaList( parent_panel, self.Settings, 
			type = MMediaList.SYSTEM_PLAYLISTS, with_list_title = False, select_list_item_callback = self.PlayTrackFromList, 
			actions = MMediaGui._system_playlist_functions )
		#print( 'system_playlists was built' )
		return self.system_playlists.GetWidget()
		
	#def EjectMedia( self ):
		#if( self._current_device.HasMedia() and self._current_device.CanBeEjected() ):
			#self._current_device.Eject()
			
	def _BuildSpeedDials( self, deviceSettings, speeddials, speedDialPanel ):
		speedDialSizer = speedDialPanel.GetSizer()
		speedDialSizer.Clear( True )
		self.speeddial_buttons = []
		
		stationIndex = 1
		speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
		speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
				
		speed_dial_button_total_count = deviceSettings.GetSpeedDialButtonTotal()
		speed_dial_button_count = 0
		if( speed_dial_button_total_count > 0 ):
			for i in range( 0, deviceSettings.GetSpeedDialRows() ):
				stationSizer = wx.BoxSizer( wx.HORIZONTAL )
				for k in range( 0, deviceSettings.GetSpeedDialButtonsPerRow() ):
					#print( 'speed_dial_button_count:{}, speed_dial_button_total_count:{}'.format( speed_dial_button_count, speed_dial_button_total_count ) )
					if( speed_dial_button_count >= speed_dial_button_total_count ):
						#add empty spaces
						stationSizer.Add( (0,0), 1, wx.EXPAND|wx.ALL, 5 )
					else:
						stationButton = wx.ToggleButton( speedDialPanel, label=str( stationIndex ) )
						stationButton.SetFont( ( speedDialAssignedFont if speeddials.has_key( str( stationIndex ) )
							else speedDialUnassignedFont ) )
						stationButton.SetForegroundColour( self.Settings.SpeedDialAssignedFont.Color )
						stationButton.Bind( wx.EVT_TOGGLEBUTTON, self.ToggleSpeedDial )
						stationButton.Bind( wx.EVT_LEFT_DOWN, self.SetSpeedDialStart )
						stationButton.Bind( wx.EVT_LEFT_UP, self.SetSpeedDialStop )
						stationSizer.Add( stationButton, 1, wx.EXPAND|wx.ALL, 5 )
						self.speeddial_buttons.append( stationButton )
						stationIndex += 1
					speed_dial_button_count += 1
				speedDialSizer.Add( stationSizer, 1, wx.EXPAND )
			speedDialPanel.Show()
		else:
			speedDialPanel.Hide()
			
		speedDialSizer.Layout()

	def GetMediaButtonByFunctionName( self, function_name ):
		return self._media_buttons[ function_name ]
		
	def RefreshMediaButton( self, media_button ):
		'''
		Calls to this function are made from devices when user selects a track via the play function,
		to update the play media_button. However calls to play are also made from the media_player used 
		by filesystem_device when and endofsong event is fired. This comes from a separate thread
		and breaks wxWidgets. Therefore this is implemented with the Publisher library.
		Note to myself. Eventually, all calls to the gui should be made either with the Publisher library
		or with ex.PostEvent to make sure that they will not break wxWidgets if they ever originate
		from another thread
		'''
		wx.CallAfter(Publisher().sendMessage, MMediaGui.PUBLISHER_REFRESH_MEDIA_BUTTON, media_button )
		
	def _OnRefreshMediaButton( self, msg ):
		media_button = msg.data
		#media_button.wx_button.SetBitmapLabel( GetImage( media_button.pressed_image if media_button.is_pressed else media_button.unpressed_image ) )
		self._SetupMediaButton( media_button )
		self.scanSizer.Layout()
		
	def _BuildMediaButtonsPanel( self, panel ):
		scanSizer = panel.GetSizer()

		mbs = sorted( self._media_buttons.values(), key=lambda x: x.order )
		#print( 'mbs is {}'.format( mbs.__class__.__name__ ) )
		for value in mbs:			
			b = wx.BitmapButton( panel, bitmap=GetImage( value.unpressed_image ) )
			#leave local functions in place, assign only device functions
			b.function_name = value.function_name
			b.Bind( wx.EVT_LEFT_UP, self._PressMediaButton )
			scanSizer.Add( b, 0, wx.ALL, 0 )
			value.wx_button = b
		return
			
	def _UpdateMediaButtons( self ):
		for function_name, media_button in self._media_buttons.iteritems():
			self._SetupMediaButton( media_button )
			
		#special case: the 'subtitles' media button is enabled depending on whether a video item
		#is currently highlighted (cliked once) in the now_playing playlist
		self.OnClickedNowPlayingItem( self.playlist.GetSelectedItemHash() )
		
		self.scanSizer.Layout()
		
	def _SetupMediaButton( self, media_button ):
		button = media_button.wx_button
		media_button.is_pressed = self._current_device.MediaButtonIsPressed( media_button.function_name )
		button.SetBitmapLabel( GetImage( media_button.pressed_image if media_button.is_pressed else media_button.unpressed_image ) )
		if( self._current_device is None ):
			button.Hide()
			return
					
		if( self._current_device.SupportsMediaFunction( media_button.function_name ) ):
			#self._media_buttons[ function_name ].callback_function = self._current_device.ExecuteMediaFunction
			self._current_device.BindMediaButton( button )
			button.Show()
			
			if( media_button.requires_loaded_media and 
				self._current_device.NeedsMedia() and 
				( not self._current_device.HasMedia() )
			):
				button.Disable()
			else:
				button.Enable()
				
			if( button.IsEnabled() and not self._current_device.MediaButtonIsEnabled( media_button.function_name ) ):
				button.Disable()
				
		else:
			self._media_buttons[ button.function_name ].callback_function = None
			button.Hide()
		
	def _PressMediaButton( self, event ):
		button = event.GetEventObject()
		#logging.debug( 'media button {} was pressed'.format( button.GetLabel() ) )
		
		#strange and not uncommon bug: disabled buttons still click
		if( not button.IsEnabled() ):
			logging.debug( 'Disabled button {} was clicked!'.format( button.function_name ) )
			return
		
		media_button = self._media_buttons[ button.function_name ]
		
		#if it is a toggle button, toggle it
		if( media_button.IsToggle() ):
			media_button.is_pressed = not media_button.is_pressed
			#button.SetBitmap( GetImage( media_button.pressed_image if media_button.is_pressed else media_button.unpressed_image ) )
			logging.debug( 'media_button.is_pressed: {}, image: {}'.format( media_button.is_pressed, ( media_button.pressed_image if media_button.is_pressed else media_button.unpressed_image ) ) )
			button.SetBitmapLabel( GetImage( media_button.pressed_image if media_button.is_pressed else media_button.unpressed_image ) )
			
		#logging.debug( 'will _CallMediaButtonCallback for {}'.format( media_button.function_name ) )
		self._CallMediaButtonCallback( media_button )
		event.Skip() #this is required to allow other bindings on the event to run too
		
	def _CallMediaButtonCallback( self, media_button ):
		#update the function that ZappStart calls if zapp is on
		if( media_button.function_name != 'zap' ):
			if( media_button.is_navigation ):
				self.ZappStart( media_button=media_button )
			else:
				self.ZappReset()
				print( '_CallMediaButtonCallback set zapp_is_on: {}'.format( self.zapp_is_on ) )
				
	def _BuildTextDisplay( self, panel ):
		txtPanel = wx.Panel( panel )
		txtSizer = wx.BoxSizer( wx.HORIZONTAL )
		txtPanel.SetSizer( txtSizer )
		txtBkgPanel = wx.Panel( txtPanel )
		txtBkgPanel.SetBackgroundColour( '#111111' )
		txtPanelSV = wx.BoxSizer( wx.HORIZONTAL )
		txtPanelS = wx.BoxSizer( wx.VERTICAL )
		txtPanelSV.Add( txtPanelS, 1, wx.ALIGN_CENTER )
		txtBkgPanel.SetSizer( txtPanelSV )
		self.txtText = wx.StaticText( txtBkgPanel, label='bla bla bla bla bla bla bla bla' )
		self.txtText.SetFont( self.Settings.TXTFont.GetFont() )
		self.txtText.SetForegroundColour(self.Settings.TXTFont.Color)
		txtPanelS.Add( self.txtText, 1, wx.ALIGN_LEFT|wx.ALL, 10 )
		txtSizer.Add( txtBkgPanel, 1, wx.EXPAND )
		return txtPanel
		
	def GetSpeedDialButton( self, index ):
		for i in self.speeddial_buttons:
			if( i.GetLabel() == index ):
				return i
		
		return None
	
	def GetPushedSpeedDialButton( self ):
		for i in self.speeddial_buttons:
			if( i.GetValue() ):
				return i
		
		return None
		
	def FireSpeedDialButtonClick( self, button ):
		# print( 'Firing for button{} (id:{})'.format( button.GetLabel(), button.GetId() ) )
		cmd = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED)
		cmd.SetEventObject(button)
		cmd.SetId(button.GetId())
		button.SetValue( True )
		self.ToggleSpeedDial( cmd )
		
	def FindNextKey( self, sortedKeys, key, forward ):
		pos = sortedKeys.index( key )
		if( forward ):
			pos += 1
			if( pos >= len( sortedKeys ) ):
				pos = 0
		else:
			pos -= 1 
			if( pos < 0 ):
				pos = len( sortedKeys ) - 1
		
		return sortedKeys[pos]
					
	def PushNextSpeedDialButton( self, forward ):
		if( len( self._current_device.state.speed_dials ) == 0 ):
			# print( 'No speed dials' )
			return
			
		keys = sorted( self._current_device.state.speed_dials.keys(), key = int )
		if( len( self._current_device.state.speed_dials ) == 1 ):
			# print( '1 speed dial' )
			button = self.GetSpeedDialButton( keys[0] )
			if( button is not None and ( not button.GetValue() ) ):
				# print( 'Pushing speed dial button {}'.format( button.GetLabel() ) )
				self.FireSpeedDialButtonClick( button )
				return
			
		#more than 1 speeddials exist
		activeButton = self.GetPushedSpeedDialButton()
		
		# print( '{} speed dials'.format( len( self._current_device.state.speed_dials ) ) )
		#no active button
		if( activeButton is None ):
			activateKey = ( keys[0] if forward else keys[len(keys)-1] )
			# print( 'No speed dial pushed. Pushing speed dial button {}'.format( activateKey ) )
			self.FireSpeedDialButtonClick( self.GetSpeedDialButton( activateKey ) )
			return
			
		nextKey = self.FindNextKey( keys,  activeButton.GetLabel(), forward )
		nextButton = self.GetSpeedDialButton( nextKey )
		# print( 'Current button:{}, next button:{}. Pushing next button'.format( 
			# activeButton.GetLabel(), nextButton.GetLabel() 
			# )
		# )
		self.FireSpeedDialButtonClick( nextButton )
		
	def SpeedDialBack( self, event=None ):
		self.ZappStart( callback=self.SpeedDialBack )
		self.PushNextSpeedDialButton( False )
		
	def SpeedDialForward( self, event=None):
		self.ZappStart( callback=self.SpeedDialForward )
		self.PushNextSpeedDialButton( True )
		
	def SetCurrentActiveList( self, list ):
		self.current_active_list = list
		
	def PlayTrackFromList( self, list, track_hash ):
		self.current_active_list = list
		self.PlayTrack( track_hash )

	def PlayTrackPreviousListStation( self, event=None):
		self.ZappStart( callback=self.PlayTrackPreviousListStation )
		self._ListSelectNext( False )
		
	def PlayTrackNextListStation( self, event=None ):
		self.ZappStart( callback=self.PlayTrackNextListStation )
		self._ListSelectNext( True )

	def _ListSelectNext( self, forward ):
		print( 'self.current_active_list: {}'.format( self.current_active_list ) )
		if( self.current_active_list ):
			self.current_active_list.ListSelectNext( forward )
			self.ResetSpeedDials()
			
	def GetSelectedListFiles( self ):
		files = []
		if( self.filelist ):
			#print( 'got filelist' )
			files = self.filelist.GetSelectedItems()
			#print( 'got {} files'.format( len( files ) ) )
		return files
			
	def GetSelectePlaylistItems( self ):
		items = []
		if( self.playlist ):
			#print( 'got playlist' )
			items = self.playlist.GetSelectedItems()
			#print( 'got {} items'.format( len( items ) ) )
		return items
		
	def GetSelectedSystemPlaylistItems( self ):
		items = []
		if( self.system_playlists ):
			items = self.system_playlists.GetSelectedItems()
		return items
			
	def SetPlaylistLabelText( self, text ):
		if( self.playlist ):
			self.playlist.SetTitle( unicode( text ) )
			
	def _CreateNumPadKey( self, label ):
		button = wx.Button( self.numPanel, label=label )
		button.Bind( wx.EVT_BUTTON, self._NumPadKeyPress )
		self.numPadKeys[ label ] =  button
		return button
		
	def _NumPadKeyPress( self, event ):
		button = event.GetEventObject()
		buttonLabel = button.GetLabel()
		numText = self.numText.GetLabel()
		if( buttonLabel == 'Enter' ):
			track_hash = float( numText )
			if( not self._current_device.TrackHashIsValid( numText ) ):
				self.__sounds.PlayError()
				return
			try:
				self.PlayTrack( track_hash )
				self.ResetSpeedDials()
				self.numTextWarningImage.Hide()
			except Exception, e:
				import traceback, sys
				traceback.print_exc()
				e = sys.exc_info()[0]
			 	print( 'Exception %s', e )
				self.numTextWarningImage.Show()
				self.__sounds.PlayError()
				return
		elif( buttonLabel == 'Clear' ):
			numText = ''
		elif( buttonLabel == 'Del' ):
			if( len( numText ) > 0 ):
				numText = numText[:-1]
		else:
			#if( not self._current_device.TrackHashIsValid( numText + buttonLabel ) ):
				#self.__sounds.PlayError()
				#return
			numText += buttonLabel
						
		if( len( numText ) == 0 ):
			self.numTextWarningImage.Hide()
		else:
			if( not self._current_device.TrackHashIsValid( numText ) ):
				self.numTextWarningImage.Show()
			else:
				self.numTextWarningImage.Hide()

		self.numText.SetLabel( numText )
				
	def ToggleNumericStationList( self, event ):
		if self.State.selector == State.STATIONSELECTOR: #self.numListButton.GetValue():
			self.State.SetStationSelector( State.NUMERICSELECTOR )
			self.numPanel.Show()
			self.stationPanel.Hide()
		else:
			self.State.SetStationSelector( State.STATIONSELECTOR )
			self.numPanel.Hide()
			self.stationPanel.Show()
		self.rbox.Layout()
			
	def ResetSpeedDials( self, exceptButton = None ):
		for i in self.speeddial_buttons:
			if( exceptButton is not None and i == exceptButton ):
				#print( 'ResetSpeedDials skipped {}'.format( i.GetLabel() ) )
				continue
			#print( 'ResetSpeedDials reset {}'.format( i.GetLabel() ) )
			i.SetValue( False )
		
	def ToggleSpeedDial( self, event ):
		#print( 'ToggleSpeedDial...' )
		button = event.GetEventObject()
		index = button.GetLabel()
		dev_speed_dials = self._current_device.state.speed_dials
		if( dev_speed_dials.has_key( index ) ):
			self._current_device.PlayTrack( dev_speed_dials[ index ] )
			self.ResetSpeedDials( button )
			#self.scanUntilObserver.Stop() #stop any automatic scanning
		else:
			button.SetValue( False )

	def SetSpeedDialStart( self, event ):
		print( 'SetSpeedDialStart...' )
		self.StartSpeedDialTimers()
		event.Skip()
			
	def SetSpeedDialStop( self, event ):
		print( 'SetSpeedDialStop! IsRunning cancel:{}, set:{}'.format( 
			self.cancelSpeedDialTimer.IsRunning(),
			# self.unsetSpeedDialTimer.IsRunning(),
			self.setSpeedDialTimer.IsRunning()
			) 
		)		
									
		print( 'button position: {}, screen position: {}'.format( event.GetEventObject().GetPosition(), event.GetEventObject().ScreenToClient( event.GetEventObject().GetPosition() ) ) )
		print( 'event position: {}, screen position: {}'.format( event.GetPosition(), event.GetEventObject().ScreenToClient( event.GetPosition() ) ) )
				
		if( not self.setSpeedDialTimer.IsRunning() and self.cancelSpeedDialTimer.IsRunning() ):
			self.speeddial_popup.OnShowPopup( event )
			
		self.ResetSpeedDialTimers()
		event.Skip()
		
	def StartSpeedDialTimers( self ):		
		self.ResetSpeedDialTimers()
		if( not self.setSpeedDialTimer.Start( self.Settings.SetSpeedDialPressTimeSecs*1000, True ) ):
			print( 'Error! Could not start setSpeedDialTimer' )
		# if( not self.unsetSpeedDialTimer.Start( self.Settings.UnSetSpeedDialPressTimeSecs*1000, True ) ):
			# print( 'Error! Could not start unsetSpeedDialTimer' )
		#if( not self.cancelSpeedDialTimer.Start( self.Settings.CancelSpeedDialPressTimeSecs*1000, True ) ):
			#print( 'Error! Could not start cancelSpeedDialTimer' )
		print( 'Started timer to {} seconds'.format( 
			self.Settings.SetSpeedDialPressTimeSecs,
			# self.Settings.UnSetSpeedDialPressTimeSecs,
			#self.Settings.CancelSpeedDialPressTimeSecs 
			)
			)
		
	def ResetSpeedDialTimers( self, event = None ):
		self.ResetSetSpeedDialTimer()
		# self.ResetUnsetSpeedDialTimer()
		#self.ResetCancelSpeedDialTimer()
	
	def ResetSetSpeedDialTimer( self, event = None ):
		if( self.setSpeedDialTimer.IsRunning() ):
			print( 'setSpeedDialTimer stopped!' )
			self.setSpeedDialTimer.Stop()

	#def ResetCancelSpeedDialTimer( self, event = None ):
		#if( self.cancelSpeedDialTimer.IsRunning() ):
			#print( 'cancelSpeedDialTimer stopped!' )
			#self.cancelSpeedDialTimer.Stop()
			
	#def CancelSpeedDialTimerFinished( self, event ):
		#self.RequestUserAttention( flags = wx.USER_ATTENTION_ERROR )
		# soundFile = os.getcwd() + '/sounds/' + 'CancelSpeedDial.wav'
		# sound = wx.Sound( soundFile )
		# if sound.IsOk():
			# sound.Play(wx.SOUND_ASYNC)
		# else:
			# wx.Bell()
		#print( 'This is CancelSpeedDialTimerFinished' )
		#self.__sounds.PlayCancel()
		
	def SetSpeedDialTimerFinished( self, event ):
		#self.RequestUserAttention( flags = wx.USER_ATTENTION_INFO )
		# soundFile = os.getcwd() + '/sounds/' + 'SetSpeedDial.wav'
		# sound = wx.Sound( soundFile )
		# if sound.IsOk():
			# sound.Play(wx.SOUND_ASYNC)
		# else:
			# wx.Bell()
		print( 'This is SetSpeedDialTimerFinished' )
		#self.__sounds.PlayComplete()
		
	def SetSpeedDialTrack( self, button ):
		track_hash = self._current_device.CurrentTrackHash()
		if( track_hash is None ):
			raise Exception( 'SetSpeedDialTrack was called but there is no self._current_device.CurrentTrackHash()' )
		
		self._SetSpeedDialHash( button, track_hash )
		
	def SetSpeedDialDirectory( self, button ):
		directory_hash = self._current_device.GetCurrentDirectoryHash()
		if( directory_hash is None ):
			raise Exception( 'SetSpeedDialDirectory was called but there is no self._current_device.GetCurrentDirectoryHash()' )
		
		self._SetSpeedDialHash( button, directory_hash )
	
	def SetSpeedDialPlaylist( self, button ):
		playlist_hash = self._current_device.GetCurrentPlaylistHash()
		if( playlist_hash is None ):
			raise Exception( 'SetSpeedDialPlaylist was called but there is no self._current_device.GetCurrentPlaylistHash()' )
		
		self._SetSpeedDialHash( button, playlist_hash )
		
	def _SetSpeedDialHash( self, button, hash_to_set ):
		if( hash_to_set is None ):
			raise Exception( '_SetSpeedDialHash was called but hash_to_set is None' )
		
		index = button.GetLabel()
		
		speedDialAssignedFont = self.Settings.SpeedDialAssignedFont.GetFont()
		button.SetFont( speedDialAssignedFont )
		button.Refresh()

		self._current_device.state.SetSpeedDial( index, hash_to_set )
		print( 'Setting speed dial {} : {}'.format( index, hash_to_set ) )
				
	def ClearSpeedDialButton( self, button ):
		index = button.GetLabel()
		speedDialUnassignedFont = self.Settings.SpeedDialUnassignedFont.GetFont()
		button.SetFont( speedDialUnassignedFont )
		button.Refresh()

		self._current_device.state.DelSpeedDial( index )
		print( 'Cleared speed dial {}'.format( index ) )
		
	def PlayTrack( self, track_hash ):
		self._current_device.PlayTrack( track_hash )
					
	def EnableNumPadKeys( self, keys ):
		for k in keys:
			self.numPadKeys[k[0]].Enable( k[1] )

	def UpdateTextDisplay( self, msg ):
		txtText = msg.data
		#print( 'received txtText:{}'.format( txtText ) )
		try:
			self.SetTextDisplayMessage( txtText )
		except:
			#errors here involve non ascii character interpretation, no harm done, so pass
			pass
	
	def SetTextDisplayMessage( self, text ):
		#self.txtText.SetLabel( unicode( text ) )
		self.text_display.SetText( text )
		
	def ClearTextDisplayMessage( self ):
		self.text_display.SetText( ' ' )
		
	def ToggleZapp( self, event ):
		self.zapp_is_on = not self.zapp_is_on
		print( 'ToggleZapp set zapp_is_on:{}'.format( self.zapp_is_on ) )
		button = event.GetEventObject()
		if( self.zapp_is_on ):
			if( isinstance( button, wx.StaticBitmap ) ):
				button.SetBitmap( GetImage( 'flash.png' ) )
			else:
				button.SetBitmapLabel( GetImage( 'flash.png' ) )
		else:
			if( isinstance( button, wx.StaticBitmap ) ):
				button.SetBitmap( GetImage( 'no_flash.png' ) )
			else:
				button.SetBitmapLabel( GetImage( 'no_flash.png' ) )
			
	def ZappStart( self, media_button=None, callback=None ):	
		print( 'ZappStart called and zappIsOn: {}'.format( self.zapp_is_on ) )
		if( media_button is None and callback is None ):
			print ( 'media_button and callback is None' )
			return
			
		if( media_button is not None and callback is not None ):
			print ( 'Impossible media_button and callback are both not None' )
			return
			
		if( not self.zapp_is_on ):
			return
			
		if( media_button ):
			if( not media_button.IsToggle() and not media_button.is_pressed ):
				return
			else:
				self.zapp_media_button = media_button
				self.zappCallback = None
		else:
			self.zapp_media_button = None
			self.zappCallback = callback
				
		self.Bind( wx.EVT_TIMER, self.ZappCoordinate, self.ZappTimer )
		self.ZappTimer.Start( self.Settings.zappTimerMSecs, True )
		
	def ZappCoordinate( self, event ):
		print( 'ZappCoordinate called and zappIsOn: {}'.format( self.zapp_is_on ) )
		#if( self.zappCallback is not None and self.zapp_is_on ):
		if( self.zapp_media_button is not None and self.zapp_is_on ):			
			print( 'ZappCoordinate executes _CallMediaButtonCallback' )
			self._CallMediaButtonCallback( self.zapp_media_button )
		elif( self.zappCallback ):
			self.zappCallback()
			
	def ZappReset( self ):
		self.zapp_is_on = False
		self.zapp_media_button = None
		self.zappCallback = None
		wx_button = self._media_buttons['zap'].wx_button
		if( wx_button and wx_button.IsShown() ):
			self._media_buttons['zap'].is_pressed = False
			wx_button.SetBitmapLabel( GetImage( self._media_buttons['zap'].unpressed_image ) )
			
	def TogglePlay( self, event ):
		button = event.GetEventObject()
		self.playing = not self.playing
		if( self.playing ):
			button.SetBitmapLabel( GetImage( 'play.png' ) )
		else:
			button.SetBitmapLabel( GetImage( 'stop.png' ) )
			
		if( self._current_device and self._current_device.SupportsScanFunction( 'play' ) ):
			self._current_device.Play( self.playing )
		
	def SystemMute( self ):
		self.volumeControl.SetSystemMute( True )
		
	def SystemUnmute( self ):
		self.volumeControl.SetSystemMute( False )

	def OnClickedNowPlayingItem( self, clicked_item ):
		#Abandoned, will use the GU_IsPlaying callback
		#enable = False
		#if( clicked_item ):
			#enable = self._current_device.ItemSupportsSubtitles( clicked_item.Hash() )
		#subtitles_media_button = self._media_buttons['subtitles']
		#button = subtitles_media_button.wx_button
		#if( enable ):
			#button.Enable()
		#else:
			#button.Disable()
		pass
		
	def OnSubtitles( self, event ):
		logging.debug( 'OnSubtitles starting ...' )
		if( self._current_device ):
			if( self._current_device.SubtitlesAreAvailable() ):
				logging.debug( '\twill GetSubtitlesDialog from device {}'.format( self._current_device.name ) )
				dlg = self._current_device.GetSubtitlesDialog( dialog_parent = self, SelectedSubtitlesCallback = self.OnSelectedSubtitles )
				if( dlg is not None ):
					dlg.ShowDialog()
			else:
				logging.debug( '\tsubtitles are not available' )
		else:
			logging.debug( 'No current device' )
		logging.debug( 'OnSubtitles finished' )
		
	def OnSelectedSubtitles( self, ok, show_subtitles, subtitle ):
		'''
		TODO: This does not need to be here. This should be a function of MediaDevice
		'''
		logging.debug( 'ok: {}, show_subtitles: {}, subtitle: {}'.format( ok, show_subtitles, subtitle ) )
		if( ok and self._current_device ):
			self._current_device.SetSubtitle( show_subtitles, subtitle )
		
	#Gui functions to be called by devices or other code to update the GUI, idebtified by GU_prefix i.e. GUI Update
	def GU_IsPlaying( self ):
		media_button = self._media_buttons['play']
		media_button.is_pressed = True
		button = media_button.wx_button
		button.SetBitmapLabel( GetImage( media_button.pressed_image ) )
		
		#check to see of should enable the "select subtitles" button
		self._media_buttons['subtitles'].wx_button.Enable( self._current_device.SubtitlesAreAvailable() )
		
	def GU_IsPaused( self ):
		media_button = self._media_buttons['play']
		media_button.is_pressed = False
		button = media_button.wx_button
		button.SetBitmapLabel( GetImage( media_button.unpressed_image ) )
		
	#End of Gui functions
	
class MarqueeText:
	def __init__( self, parent_panel, app_font,  max_chars = 25 ):
		self.frame = parent_panel.GetParent()
		self.app_font = app_font
		self.max_chars = max_chars
		self.text = ''
		self.marquee_text = self.text
		self.marquee_text_pos = 0
		self.marquee_timer = wx.Timer( self.frame )
		self.frame.Bind( wx.EVT_TIMER, self._AdvanceMarquee, self.marquee_timer )
		
		self._panel = wx.Panel( parent_panel )
		self._BuildUI()
		
	def _BuildUI( self ):
		txtPanel = self._panel
		txtSizer = wx.BoxSizer( wx.HORIZONTAL )
		txtPanel.SetSizer( txtSizer )
		txtBkgPanel = wx.Panel( txtPanel )
		txtBkgPanel.SetBackgroundColour( '#111111' )
		txtPanelSV = wx.BoxSizer( wx.HORIZONTAL )
		txtPanelS = wx.BoxSizer( wx.VERTICAL )
		txtPanelSV.Add( txtPanelS, 1, wx.ALIGN_CENTER )
		txtBkgPanel.SetSizer( txtPanelSV )
		self.txtText = wx.StaticText( txtBkgPanel, label='bla bla bla bla bla bla bla bla' )
		self.txtText.SetFont( self.app_font.GetFont() )
		self.txtText.SetForegroundColour( self.app_font.Color) 
		txtPanelS.Add( self.txtText, 1, wx.ALIGN_LEFT|wx.ALL, 10 )
		txtSizer.Add( txtBkgPanel, 1, wx.EXPAND )		
		
	def GetPanel( self ):
		return self._panel
		
	def _AdvanceMarquee( self, event = None ):
		self.marquee_text = self.text[ self.marquee_text_pos : max( len( self.text ), self.max_chars ) ]
		self.marquee_text_pos = ( self.marquee_text_pos + 1 ) % ( ( len( self.text ) - 1 ) or 1 )
		self.txtText.SetLabel( self.marquee_text )
		
	def SetText( self, text ):
		self.text = unicode( text )
		self.marquee_text_pos = 0
		self._AdvanceMarquee()
		if( len( self.text ) > self.max_chars ):
			self.text = self.text.rjust( len( self.text ) + self.max_chars, ' ' )
			self.StartMarquee()
		else:
			self.StopMarquee()
			
	def StartMarquee( self ):
		self.StopMarquee()
		print( 'marquee_timer started!' )
		self.marquee_timer.Start( 150, False )
		
	def StopMarquee( self ):
		if( self.marquee_timer.IsRunning() ):
			print( 'marquee_timer stopped!' )
			self.marquee_timer.Stop()
		
class VolumeControl:
	def __init__( self, parentPanel, settings, state, device ):
		self._device = device
		self.settings = settings
		self.state = state
		self.maxVolume = 10
		self.volume =  self.state.GetVolume()
		self.step = 1
		self.userSetMuteOn = self.state.GetMute()
		self.stereoObserver = StereoMonoPanelObserver( self )
		
		self.parentPanel = wx.Panel( parentPanel )
		self.parentPanel.SetBackgroundColour( '#000000' )
				
		self.volumePanel = wx.Panel( self.parentPanel )
		self.volumePanel.SetBackgroundColour( '#000000' )
		self.volumeSizer = wx.BoxSizer( wx.VERTICAL )
		self.volumePanel.SetSizer( self.volumeSizer )

		#put them in a vertical sizer
		self.vbsizer = wx.BoxSizer( wx.VERTICAL )
		self.volumeBar = []
		for i in range( 0, self.maxVolume ):
			self.volumeBar.append( wx.Button( self.volumePanel, size=(15,-1) )  )#, style=wx.NO_BORDER ) )
			self.vbsizer.Add( self.volumeBar[i], 1, wx.ALL, 1 )

		#put the vertical sizer inside a horizontal sizer along with 
		#a left and right spacers
		hsizer = wx.BoxSizer( wx.HORIZONTAL )
		padding = 2
		hsizer.Add( (1,1), padding, wx.EXPAND, 0 )
		hsizer.Add( self.vbsizer, 0, wx.EXPAND, 0 )
		self.Text = wx.StaticText( self.volumePanel, label=str(self.volume*10) + '%' )
		textSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.Text.SetForegroundColour( self.settings.onVolumeBackgroundColour )
		textSizer.Add( self.Text, 0, wx.ALIGN_CENTRE )
		hsizer.Add( textSizer, padding, wx.EXPAND )
		
		volUpBitmap = wx.StaticBitmap( self.volumePanel, -1, GetImage( 'volume_up.png' ) )
		volUpBitmap.Bind( wx.EVT_LEFT_UP, self.IncreaseVolume )
		self.volumeSizer.Add( volUpBitmap, 0, wx.ALIGN_CENTRE|wx.TOP, 10 )
		self.volumeSizer.Add( hsizer, 1, wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL, 0 )
		volDownBitmap = wx.StaticBitmap( self.volumePanel, -1, GetImage( 'volume_down.png' ) )
		volDownBitmap.Bind( wx.EVT_LEFT_UP, self.DecreaseVolume )
		self.volumeSizer.Add( volDownBitmap, 0, wx.ALIGN_CENTRE|wx.BOTTOM, 10 )
		
		self.controlSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		#muteImage = GetImage("unmute.png")
		#if( self._device is not None and self._device.GetMute() ):
			#muteImage = GetImage("mute.png")
		#self.muteButton = wx.StaticBitmap( self.parentPanel,	bitmap=muteImage )
		#self.muteButton.Bind( wx.EVT_LEFT_UP, self.ToggleMute )
		#
		#self.controlSizer.Add( self.muteButton, 1, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE, border=0 )
		
		self.stereoMonoPanel = self.BuildStereoMonoControl( self.parentPanel )
		self.controlSizer.Add( self.stereoMonoPanel, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=10 )
		self.controlSizer.Add( self.volumePanel, 0, wx.EXPAND, border = 0 )

		self.parentPanel.SetSizer( self.controlSizer )
		
		self.SetVolume( self.volume )
		
	def SetDevice( self, device ):
		if( device is None ):
			return
			
		#cleanup from the previous device
		if( self._device is not None ):
			if( self._device.SupportsStereoMono() ):
				self._device.DelStereoMonoObserver( self.stereoObserver )

		self._device = device
		self._device.SetVolume( self.volume )
		self._device.SetMute( self.userSetMuteOn )
		#self.SetVolume( int( self._device.GetVolume()/10 ) )
		#self.muteButton.SetBitmap( GetImage( "mute.png" ) if self._device.GetMute() else GetImage( "unmute.png" ) )
		
		#print( 'Device {} {} supports Stereo/Mono'.format( self._device.name,
			#( '' if self._device.SupportsStereoMono() else 'NOT' ) ) )
		if( self._device.SupportsStereoMono() ):
			#print( 'will show self.stereoMonoPanel' )
			self._device.AddStereoMonoObserver( self.stereoObserver )
			#print( 'just shown self.stereoMonoPanel' )
			self.SetStereo( self._device.IsStereo() )
		else:
			#print( 'will hide self.stereoMonoPanel' )
			self.StereoMonoHide()
			#print( 'just hid self.stereoMonoPanel' )
					
		#self._ShowStereoUI( True )
		#self._ShowMonoUI( True )

		self.controlSizer.Layout()

	def SetStereo( self, stereo ):
		if( stereo ):
			# self.whiteBorderPanel.SetBackgroundColour( self.settings.StereoMonoBrightColor )
			# self.stereoText.SetForegroundColour( self.settings.StereoMonoBrightColor )
			# self.monoText.SetForegroundColour( '#000000' )
			self._ShowStereoUI( True )
			self._ShowMonoUI( False )
		else:
			# self.whiteBorderPanel.SetBackgroundColour( '#000000' )
			# self.stereoText.SetForegroundColour( '#000000' )
			# self.monoText.SetForegroundColour( self.settings.StereoMonoBrightColor )
			self._ShowStereoUI( False )
			self._ShowMonoUI( True )

	def _ShowStereoUI( self, show ):
		if( show ):
			self.whiteBorderPanel.SetBackgroundColour( self.settings.StereoMonoBrightColor )
			self.stereoText.SetForegroundColour( self.settings.StereoMonoBrightColor )			
		else:
			self.whiteBorderPanel.SetBackgroundColour( '#000000' )
			self.stereoText.SetForegroundColour( '#000000' )

	def _ShowMonoUI( self, show ):
		if( show ):
			self.monoText.SetForegroundColour( self.settings.StereoMonoBrightColor )
		else:
			self.monoText.SetForegroundColour( '#000000' )

	def StereoMonoHide( self ):
		self._ShowStereoUI( False )
		self._ShowMonoUI( False )
			
	def GetControlPanel( self ):
		return self.parentPanel
	
	def IncreaseVolume( self, event ):
		self.ChangeVolume( self.step )
		
	def DecreaseVolume( self, event ):
		self.ChangeVolume( -self.step )
		
	def SetVolume( self, volume ):
		self.volume = volume
		if( self.volume > self.maxVolume ):
			self.volume = self.maxVolume
		elif( self.volume < 0 ):
			self.volume = 0
			
		#print( 'volume:{}, self.volume:{}'.format( volume, self.volume ) )
		if( self._device ):
			self._device.SetVolume( volume )
		
		for i in range( 0, self.maxVolume ):
			color = self.settings.onVolumeBackgroundColour if i <= self.volume-1 else self.settings.offVolumeBackgroundColour
			self.volumeBar[ self.maxVolume - i - 1 ].SetBackgroundColour( color )
			self.volumeBar[ self.maxVolume - i - 1 ].Refresh()
		self.Text.SetLabel( str( self.volume*10 ) + '%' )
		self.state.SetVolume( volume )
		
	def ChangeVolume( self, step ):
		volume = step + self.volume
		if( volume > self.maxVolume ):
			volume = self.maxVolume
		elif( volume < 0 ):
			volume = 0
			
		self.SetVolume( volume )
		
	def SetSystemMute( self, mute ):
		#print( 'volume.SetSystemMute called with mute: {}'.format( mute ) )
		#print( 'self.userSetMuteOn : {} so ...'.format( self.userSetMuteOn ) )
		if( not self.userSetMuteOn ):			
			self._device.SetMute( mute )
		
	def ToggleMute( self, event ):
		if( self._device is None ):
			return
			
		button = event.GetEventObject()
		if self._device.GetMute():
			self._device.SetMute( False )
			self.userSetMuteOn = False
			#self.MuteButton.SetBitmapLabel( GetImage( "unmute.png" ) )
			button.SetBitmap( GetImage( "unmute.png" ) )
		else:
			self._device.SetMute( True )
			self.userSetMuteOn = True
			#self.MuteButton.SetBitmapLabel( GetImage( "mute.png" ) )
			button.SetBitmap( GetImage( "mute.png" ) )
		self.state.SetMute( self.userSetMuteOn )

	def BuildStereoMonoControl( self, panel ):
		controlPanel = wx.Panel( panel )
		controlPanel.SetBackgroundColour( '#000000' )
		
		self.audioSizer = wx.BoxSizer( wx.VERTICAL )
		controlPanel.SetSizer( self.audioSizer )
		self.stereoPanel = wx.Panel( controlPanel )
		self.stereoPanel.SetBackgroundColour( '#000000' )
		stereoSizer = wx.BoxSizer( wx.VERTICAL )
		self.stereoPanel.SetSizer( stereoSizer )

		#a white text inside a black panel that has a border and is inside a white panel
		#results in a white text with white border over a black background
		self.whiteBorderPanel = wx.Panel( self.stereoPanel )
		self.whiteBorderPanel.SetBackgroundColour( self.settings.StereoMonoBrightColor )
		whiteBorderSizer = wx.BoxSizer( wx.VERTICAL )
		self.whiteBorderPanel.SetSizer( whiteBorderSizer )
		whiteBorderBlackPanel = wx.Panel( self.whiteBorderPanel )
		whiteBorderSizer.Add( whiteBorderBlackPanel, 0, wx.ALIGN_CENTRE | wx.ALL, 1 )
		whiteBorderBlackPanel.SetBackgroundColour( '#000000' )
		wbbps = wx.BoxSizer( wx.VERTICAL )
		whiteBorderBlackPanel.SetSizer( wbbps )
		self.stereoText = wx.StaticText( whiteBorderBlackPanel, label='STEREO' )
		wbbps.Add( self.stereoText, 1, wx.ALL|wx.ALIGN_CENTRE, 2 )
		self.stereoText.SetForegroundColour( self.settings.StereoMonoBrightColor )
		stereoSizer.Add( self.whiteBorderPanel, 0, wx.ALIGN_CENTRE )
		
		muteImage = GetImage("unmute.png")
		if( self._device is not None and self._device.GetMute() ):
			muteImage = GetImage("mute.png")
		self.muteButton = wx.StaticBitmap( controlPanel,	bitmap=muteImage )
		self.muteButton.Bind( wx.EVT_LEFT_UP, self.ToggleMute )
		
		self.monoPanel = wx.Panel( controlPanel )
		self.monoPanel.SetBackgroundColour( '#000000' )
		monoSizer = wx.BoxSizer( wx.HORIZONTAL )
		self.monoPanel.SetSizer( monoSizer )
		self.monoText = wx.StaticText( self.monoPanel, label='MONO' )
		self.monoText.SetForegroundColour( self.settings.StereoMonoBrightColor )
		monoSizer.Add( self.monoText, 1, wx.ALIGN_CENTRE )

		self.audioSizer.Add( self.stereoPanel, 1, wx.ALIGN_CENTRE )#, border=15 )
		#self.audioSizer.Add( (1,1),1,wx.EXPAND ) #add spacer
		self.audioSizer.Add( self.muteButton, 0, wx.ALIGN_CENTRE )
		#self.audioSizer.Add( (1,1),1,wx.EXPAND ) #add spacer
		self.audioSizer.Add( self.monoPanel, 1, wx.ALIGN_CENTRE )#, border=15 )
		
		return controlPanel
		
def GetImage( imageFile, size = '48x48' ):
	imageDir = os.getcwd() + '/images/' + size + '/'
	imageFile = imageDir + imageFile
	image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	
	return image
		
class StereoMonoPanelObserver:
	def __init__( self, volume_control ):
		self.volume_control = volume_control
		
	def IsStereo( self, isStereo ):
		self.volume_control.SetStereo( isStereo )
		
class NumpadTrackHashObserver:
	def __init__( self, numText ):
		self.numText = numText
		
	def CurrentTrackHashIs( self, track_hash ):
		print( 'NumpadTrackHashObserver updated with track_hash: {}'.format( track_hash ) )
		self.numText.SetLabel( track_hash )
		
class PlaylistTrackHashObserver:
	def __init__( self, playlist ):
		self.playlist = playlist
	
	def CurrentTrackHashIs( self, track_hash ):
		#print( 'PlaylistTrackHashObserver updated with track_hash: {}'.format( track_hash ) )
		print( '\twill try to select track {} in list'.format( track_hash ) )
		if( self.playlist ):
			print( '\t\twill definitely select track {} in list'.format( track_hash ) )
			self.playlist.SelectListTrack( track_hash )

		
if __name__ == '__main__':
  
	app = wx.App()
	MMediaGui(None, title="MMedia")
	app.MainLoop()
