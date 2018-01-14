#! /usr/bin/python
# -*- coding: utf-8 -*-

# import external libraries
import wx # 2.8
import vlc

# import standard libraries
import os
import user
from threading import *
import time
import traceback

class VLCControlState:
	'''This is the state of the viewer'''
	
	def __init__( self ):
		self.brightness = 50
		self.contrast = 50
		self.device = 'v4l2:///dev/video0'		

class VLCControl():
	"""The main window has to deal with events.
	"""
	SetStep = 10
	SetMin = 0
	SetMax = 200

	def __init__(self, videoParentPanel, controlsParentPanel, state, stateSaveCallback, 
		videoPanelClickCallback, hideDevice = False ):
		'''Note: stateSaveCallback does not take any arguments. The parent object that maintains stateSaveCallback
		   should keep a reference to state in order to be able to access it when VLCControl calls stateSaveCallback
		'''		
		self.device = 'v4l2:///dev/video0'

		self.State = state #State()
		#self.State.Load()
		self.stateSaveCallback = stateSaveCallback
		self.videoPanelClickCallback = videoPanelClickCallback

		self.device = self.State.device

		# Panels
		# The first panel holds the video and it's all black
		self.videopanel = wx.Panel(videoParentPanel, -1)
		self.videopanel.SetBackgroundColour(wx.BLACK)

		# The second panel holds controls
		self.ctrlpanel = wx.Panel(controlsParentPanel, -1 )
		brightnessL = wx.StaticText(self.ctrlpanel, label="Brightness")
		minusBrightnessBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-minus.png' ) )
		plusBrightnessBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-plus.png' ) )
		self.brightnessSlider = wx.Slider(self.ctrlpanel, -1, self.State.brightness, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		contrastL = wx.StaticText(self.ctrlpanel, label="Contrast")
		minusContrastBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-minus.png' ) )
		plusContrastBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-plus.png' ) )
		self.contrastSlider = wx.Slider(self.ctrlpanel, -1, self.State.contrast, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		if( not hideDevice ):
			deviceL = wx.StaticText( self.ctrlpanel, label='Device:' )
			self.deviceTxt = wx.TextCtrl( self.ctrlpanel )
			self.deviceTxt.SetValue( self.device )
			deviceBtn = wx.Button( self.ctrlpanel, label='Ok' )
		#maxImageBtn = wx.ToggleButton( self.ctrlpanel, wx.ID_ANY, 'Maximize' )
		#maxImageBtn.SetValue( self.State.maxImage )
		#self.maxImage = self.State.maxImage

		# Bind controls to events
		self.videopanel.Bind( wx.EVT_LEFT_UP, self.VideopanelClicked )

		self.brightnessSlider.Bind(wx.EVT_SLIDER, self.OnSetBrightness )
		self.contrastSlider.Bind(wx.EVT_SLIDER, self.OnSetContrast )
		minusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseBrightness )
		plusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseBrightness )
		minusContrastBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseContrast )
		plusContrastBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseContrast )
		#maxImageBtn.Bind( wx.EVT_TOGGLEBUTTON, self.MaxImage )  
		if( not hideDevice ):
			deviceBtn.Bind( wx.EVT_BUTTON, self.SetDevice )   

		# Give a pretty layout to the controls
		ctrlbox = wx.BoxSizer(wx.VERTICAL)

		gridSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
		gridSizer.AddGrowableCol( 1 )

		bbox = wx.BoxSizer( wx.HORIZONTAL )
		bbox.Add( minusBrightnessBtn, 0, wx.CENTER )
		bbox.Add( self.brightnessSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		bbox.Add( plusBrightnessBtn, 0, wx.CENTER )

		cbox = wx.BoxSizer( wx.HORIZONTAL )
		cbox.Add( minusContrastBtn, 0, wx.CENTER )
		cbox.Add( self.contrastSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		cbox.Add( plusContrastBtn, 0, wx.CENTER )

		dbox = wx.BoxSizer( wx.HORIZONTAL )
		dbox.Add( self.deviceTxt, 1, wx.EXPAND )
		if( not hideDevice ):
			dbox.Add( deviceBtn, 0 )
			gridSizer.AddMany([
				( brightnessL,0,wx.ALIGN_CENTER_VERTICAL ), ( bbox, 1, wx.EXPAND ),
				( contrastL,0,wx.ALIGN_CENTER_VERTICAL ), ( cbox, 1, wx.EXPAND ),
				( deviceL, 0,wx.ALIGN_CENTER_VERTICAL ), ( dbox, 1, wx.EXPAND )
			])
		else:
			gridSizer.AddMany([
				( brightnessL,0,wx.ALIGN_CENTER_VERTICAL ), ( bbox, 1, wx.EXPAND ),
				( contrastL,0,wx.ALIGN_CENTER_VERTICAL ), ( cbox, 1, wx.EXPAND )
			])
		ctrlbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL )
		#ctrlbox.Add( maxImageBtn, 0, wx.TOP|wx.BOTTOM, border = 20 )

		self.ctrlpanel.SetSizer(ctrlbox)

		## Put everything together
		#self.sizer = wx.BoxSizer(wx.VERTICAL)
		#self.sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
		#self.sizer.Add(self.ctrlpanel, flag=wx.EXPAND | wx.ALL, border=10)
		#self.SetSizer(self.sizer)
		##self.SetMinSize((350, 300))

		#self.ctrlpanel.Hide()
		#self.ctrlPanelHidden = True

		# VLC player controls
		self.Instance = vlc.Instance( '--no-video-title-show --verbose -1 --sub-filter marq --sub-source marq' )
		self.player = self.Instance.media_player_new()
		self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
		self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Position,8)#vlc.Position.Bottom)
		self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout,0)
		self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 100)
		#self.player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, 'HELLO WORLD' )
		#m = self.Instance.media_new( self.device )
		#self.player.set_media( m )
		#self.SetTitle("Rear Camera")
		#EVT_ADJUSTIMAGE( self, self.AdjustImageSettings )
		self.playerLock = RLock()

	def Start( self ):
		#Make sure that before Start is called you show the main application window so that 
		#the window is rendered, so that it gets a handle from the operating system in order 
		#to pass it on to the player, to display its content
		#self.Show()
		# set the window id where to render VLC's video output
		self.player.set_xwindow(self.videopanel.GetHandle())        

		#self.player.play()            

		#Without the time delay, enabling image adjustment crashes the application
		#for some reason
		#time.sleep( 1 )

		#self.AdjustImageSettings()
		#self.videoWidth = self.player.video_get_width()
		#print( 'width:{}'.format( self.videoWidth ) )
		#self.videoHeight = self.player.video_get_height()
		#self.player.video_set_scale( 1.5 )

		#self.videopanel.Bind(wx.EVT_SIZE, self.OnSize)
		#self.UpdateVideoWidth()

		#self.player.video_set_scale( 0.0 )
		#self.player.video_set_crop_geometry( None )

	def AdjustImageSettings( self ):
		with self.playerLock :
			self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			#self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, self.State.brightness/50.0 )
			#self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, self.State.contrast/50.0 )
			self.OnSetBrightness()
			self.OnSetContrast()

	def SetDevice( self, event ):
		with self.playerLock :
			self.device = self.deviceTxt.GetValue()
			m = self.Instance.media_new( self.device )
			self.player.set_media( m )
			self.player.play()
			self.State.device = self.device
			self.SaveState()
		
	def PlayMedia( self, media, options ):
		print( 'VLCControl was asked to PlayMedia: {}'.format( media ) )
		with self.playerLock :
			if( self.player.is_playing() == 1 ):
				print( 'stopping media player' )
				self.player.stop()

			m = self.Instance.media_new( media )
			m.add_options( options )
			self.player.set_media( m )		
			if( self.player.play() == -1 ):
				print( 'Cannot play "{0}"'.format( media ) )
			else:			
				#start a thread and wait until the tuner has tuned and we have tv picture
				#print( 'starting CheckPlayerThread...' )
				CheckPlayerThread( self ) #, self.player, self.playerLock )
				#self.AdjustImageSettings()
				print( 'Playing "{0}"'.format( media ) )

	def ShowMarquee( self, show, text = '' ):
		with self.playerLock :
			if( show ):
				self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
				self.player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, text )
			else:
				self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 0)
			
	def __dump( self ):
		scale = self.player.video_get_scale()
		print( 'scale:{}'.format( scale ) )
		ar = self.player.video_get_aspect_ratio()
		print( 'aspect ratio:{}'.format( ar ) )
		self.videoWidth = self.player.video_get_width()
		print( 'width:{}'.format( self.videoWidth ) )
		self.videoHeight = self.player.video_get_height()
		print( 'height:{}'.format( self.videoHeight ) )

	def IncreaseBrightness( self, event ):
		brightness = self.brightnessSlider.GetValue() * 2
		if( brightness >= VLCControl.SetMax ):
			print( 'brightness:{} >= VLCControl.SetMax:{}'.format( brightness, VLCControl.SetMax ) )
			return
		brightness += VLCControl.SetStep
		self.brightnessSlider.SetValue( brightness/2 )
		self.OnSetBrightness()
		return

	def DecreaseBrightness( self, event ):
		brightness = self.brightnessSlider.GetValue() * 2
		if( brightness <= VLCControl.SetMin ):
			print( 'brightness:{} <= VLCControl.SetMax:{}'.format( brightness, VLCControl.SetMax ) )
			return
		brightness -= VLCControl.SetStep
		self.brightnessSlider.SetValue( brightness/2 )
		self.OnSetBrightness()
		return

	def IncreaseContrast( self, event ):
		contrast = self.contrastSlider.GetValue() * 2
		if( contrast >= VLCControl.SetMax ):
			print( 'contrast:{} >= VLCControl.SetMax:{}'.format( contrast, VLCControl.SetMax ) )
			return
		contrast += VLCControl.SetStep
		self.contrastSlider.SetValue( contrast/2 )
		self.OnSetContrast()
		return

	def DecreaseContrast( self, event ):
		contrast = self.contrastSlider.GetValue() * 2
		if( contrast <= VLCControl.SetMin ):
			print( 'contrast:{} <= VLCControl.SetMax:{}'.format( contrast, VLCControl.SetMax ) )
			return
		contrast -= VLCControl.SetStep
		self.contrastSlider.SetValue( contrast/2 )
		self.OnSetContrast()
		return

	def VideopanelClicked( self, event ):
		if( self.videoPanelClickCallback is not None ):
			self.videoPanelClickCallback()

	def OnSetBrightness(self, evt=None):
		"""Set the brightness according to the brightness slider.
		"""
		with self.playerLock :
			#self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			brightness = self.brightnessSlider.GetValue() * 2
			print( 'new brightness: {}'.format( brightness ) )
			if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, brightness/100.0 ) == -1:
				self.errorDialog("Failed to set brightness")
			else:
				self.State.brightness = brightness/2
				self.SaveState()

	def OnSetContrast(self, evt=None):
		"""Set the contrast according to the contrast slider.
		"""
		with self.playerLock :
			#self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
			contrast = self.contrastSlider.GetValue() * 2
			print( 'new contrast: {}'.format( contrast ) )
			if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, contrast/100.0 ) == -1:
				self.errorDialog("Failed to set contrast")
			else:
				self.State.contrast = contrast/2
				self.SaveState()

	def errorDialog(self, errormessage):
		"""Display a simple error dialog.
		"""
		edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK|wx.ICON_ERROR)
		edialog.ShowModal()

	def SaveState( self ):
		if( self.stateSaveCallback is not None ):
			self.stateSaveCallback()

def GetImage( imageFile, size ='48x48' ):
	imageDir = os.getcwd() + '/images/' + size + '/'
	imageFile = imageDir + imageFile
	image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()	
	return image

EVT_ADJUSTIMAGE_ID = wx.NewId()

def EVT_ADJUSTIMAGE(win, func):
	"""Define ADJUSTIMAGE Event."""
	win.Connect(-1, -1, EVT_ADJUSTIMAGE_ID, func)

class AdjustImageEvent(wx.PyEvent):
	"""Simple event"""
	def __init__(self):
		"""Init ADJUSTIMAGE Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_ADJUSTIMAGE_ID)

class CheckPlayerThread(Thread):
	'''Thread to check if the player is playing. While the player is not playing it will sleep for 0.1 secs and try again'''
	def __init__( self, vlccontrol ): #notify_window, player, playerLock ):
		Thread.__init__(self)
		#self._notify_window = notify_window
		#self._player = player
		#self._playerLock = playerLock
		self.vlccontrol = vlccontrol
		self.setDaemon(1)
		self.start()

	def run(self):
		''' Run Worker Thread. Once this thread is started it will run forever until it detects that the player is playing.
			As soon as it detects that the player is playing it will post an event to VLCControl and finish.
			It will not block for access to the player, instead it will sleep and try later. If the player is not playing
			it will again sleep and try later.
		'''
		while( True ):
			if( self.vlccontrol.playerLock.acquire( False ) ):
				try:
					if( self.vlccontrol.player.is_playing() == 1 ):
						#wx.PostEvent( self._notify_window, AdjustImageEvent() )
						#print( 'Thread is adjusting image settings...' )
						self.vlccontrol.AdjustImageSettings()
						#print( 'Thread finished adjusting image settings.' )
						break	#finished
					#else:
						#print( 'player is not playing yet' )
				finally:
					#print( 'Thread is releasing the playerlock' )					
					self.vlccontrol.playerLock.release()
					#print( 'Thread released the playerlock' )
			time.sleep( 1 )
		

if __name__ == "__main__":
    # Create a wx.App(), which handles the windowing system event loop
    app = wx.PySimpleApp()
    # Create the window containing our small media player
    camera = VLCControl("Simple PyVLC Player")
    # show the player window centred and run the application
    camera.Centre()
    camera.Show()
    app.MainLoop()
