#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class ImageSettingsPanel( wx.Panel ):
	def __init__( self, parent, minus_button_image, plus_button_image, SetStep = 10, SetMin = 0, SetMax = 200, initial_brightness = 0, initial_contrast = 0, SetBrightnessCallback = None, SetContrastCallback = None ):
		wx.Panel.__init__( self, parent = parent, id = wx.ID_ANY )
		
		self.SetStep = SetStep
		self.SetMin = SetMin
		self.SetMax = SetMax
		
		self.brightness = initial_brightness
		self.contrast = initial_contrast
		
		self.SetBrightnessCallback = SetBrightnessCallback
		self.SetContrastCallback = SetContrastCallback

		brightnessL = wx.StaticText( self, label="Brightness")
		minusBrightnessBtn = wx.StaticBitmap( self, bitmap = minus_button_image )
		plusBrightnessBtn = wx.StaticBitmap( self, bitmap = plus_button_image )
		self.brightnessSlider = wx.Slider( self, -1, self.brightness, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		contrastL = wx.StaticText( self, label="Contrast")
		minusContrastBtn = wx.StaticBitmap( self, bitmap = minus_button_image )
		plusContrastBtn = wx.StaticBitmap( self, bitmap = plus_button_image )
		self.contrastSlider = wx.Slider( self, -1, self.contrast, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)

		# Bind controls to events
		
		self.Bind( wx.EVT_SLIDER, self.OnSetBrightness, self.brightnessSlider )
		self.Bind( wx.EVT_SLIDER, self.OnSetContrast, self.contrastSlider )
		minusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseBrightness )
		plusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseBrightness )
		minusContrastBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseContrast )
		plusContrastBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseContrast )

		# Give a pretty layout to the controls
		ctrlbox = wx.BoxSizer( wx.VERTICAL )
		
		gridSizer = wx.FlexGridSizer( rows=2, cols=2, hgap=5, vgap=5 )
		gridSizer.AddGrowableCol( 1 )
		
		bbox = wx.BoxSizer( wx.HORIZONTAL )
		bbox.Add( minusBrightnessBtn, 0, wx.CENTER )
		bbox.Add( self.brightnessSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		bbox.Add( plusBrightnessBtn, 0, wx.CENTER )
		
		cbox = wx.BoxSizer( wx.HORIZONTAL )
		cbox.Add( minusContrastBtn, 0, wx.CENTER )
		cbox.Add( self.contrastSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		cbox.Add( plusContrastBtn, 0, wx.CENTER )
		
		gridSizer.AddMany([
			( brightnessL,0,wx.ALIGN_CENTER_VERTICAL ), ( bbox, 1, wx.EXPAND ),
			( contrastL,0,wx.ALIGN_CENTER_VERTICAL ), ( cbox, 1, wx.EXPAND )
		])
		ctrlbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL, border = 10 )
				
		self.SetSizer(ctrlbox)
		
	def IncreaseBrightness( self, event ):
		brightness = self.brightnessSlider.GetValue() * 2
		if( brightness >= self.SetMax ):
			print( 'brightness:{} >= self.SetMax:{}'.format( brightness, self.SetMax ) )
			return
		brightness += self.SetStep
		self.brightnessSlider.SetValue( brightness/2 )
		self.OnSetBrightness()
		return

	def DecreaseBrightness( self, event ):
		brightness = self.brightnessSlider.GetValue() * 2
		if( brightness <= self.SetMin ):
			print( 'brightness:{} <= self.SetMax:{}'.format( brightness, self.SetMax ) )
			return
		brightness -= self.SetStep
		self.brightnessSlider.SetValue( brightness/2 )
		self.OnSetBrightness()
		return
		
	def IncreaseContrast( self, event ):
		contrast = self.contrastSlider.GetValue() * 2
		if( contrast >= self.SetMax ):
			print( 'contrast:{} >= self.SetMax:{}'.format( contrast, self.SetMax ) )
			return
		contrast += self.SetStep
		self.contrastSlider.SetValue( contrast/2 )
		self.OnSetContrast()
		return
					
	def DecreaseContrast( self, event ):
		contrast = self.contrastSlider.GetValue() * 2
		if( contrast <= self.SetMin ):
			print( 'contrast:{} <= self.SetMax:{}'.format( contrast, self.SetMax ) )
			return
		contrast -= self.SetStep
		self.contrastSlider.SetValue( contrast/2 )
		self.OnSetContrast()
		return
		
	def OnSetBrightness(self, evt=None):
		"""
		Set the brightness according to the brightness slider.
		"""
		self.brightness = self.brightnessSlider.GetValue() * 2
		print( 'new brightness: {}'.format( self.brightness ) )
		if( self.SetBrightnessCallback ):
			self.SetBrightnessCallback( self.brightness )

	def OnSetContrast(self, evt=None):
		"""
		Set the contrast according to the contrast slider.
		"""
		self.contrast = self.contrastSlider.GetValue() * 2
		print( 'new contrast: {}'.format( self.contrast ) )
		if( self.SetContrastCallback ):
			self.SetContrastCallback( self.contrast )

	def errorDialog(self, errormessage):
		"""
		Display a simple error dialog.
		"""
		edialog = wx.MessageDialog( self, errormessage, 'Error', wx.OK|wx.ICON_ERROR )
		edialog.ShowModal()
				
class AudioSettingsPanel( wx.Panel ):
	def __init__( self, parent, initial_visual_effect = '', initial_equalizer_active = False, initial_equalizer_preset = '' ):
		'''
Visualizer filter
   General:
	  --effect-list=<string>     Effects list
		  A list of visual effect, separated by commas.
Current effects
		  include: dummy, scope, spectrum, spectrometer and vuMeter.
	  --effect-width=<integer [-2147483648 .. 2147483647]>
								 Video width
		  The width of the effects video window, in pixels.
	  --effect-height=<integer [-2147483648 .. 2147483647]>
								 Video height
		  The height of the effects video window, in pixels.
   Spectrum analyser:
	  --visual-80-bands, --no-visual-80-bands
								 Show 80 bands instead of 20 (default enabled)
		  Show 80 bands instead of 20 (default enabled)
	  --visual-peaks, --no-visual-peaks
								 Draw peaks in the analyzer (default enabled)
		  Draw peaks in the analyzer (default enabled)
   Spectrometer:
	  --spect-show-original, --no-spect-show-original
								 Enable original graphic spectrum (default
								 disabled)
		  Enable the "flat" spectrum analyzer in the spectrometer. (default
		  disabled)
	  --spect-show-base, --no-spect-show-base
								 Draw the base of the bands (default enabled)
		  Draw the base of the bands (default enabled)
	  --spect-radius=<integer [-2147483648 .. 2147483647]>
								 Base pixel radius
		  Defines radius size in pixels, of base of bands(beginning).
	  --spect-sections=<integer [-2147483648 .. 2147483647]>
								 Spectral sections
		  Determines how many sections of spectrum will exist.
	  --spect-color=<integer [-2147483648 .. 2147483647]>
								 V-plane color
		  YUV-Color cube shifting across the V-plane ( 0 - 127 ).
	  --spect-show-bands, --no-spect-show-bands
								 Draw bands in the spectrometer (default
								 enabled)
		  Draw bands in the spectrometer (default enabled)
	  --spect-80-bands, --no-spect-80-bands
								 Show 80 bands instead of 20 (default enabled)
		  Show 80 bands instead of 20 (default enabled)
	  --spect-separ=<integer [-2147483648 .. 2147483647]>
								 Number of blank pixels between bands.
		  Number of blank pixels between bands.
	  --spect-amp=<integer [-2147483648 .. 2147483647]>
								 Amplification
		  This is a coefficient that modifies the height of the bands.
	  --spect-show-peaks, --no-spect-show-peaks
								 Draw peaks in the analyzer (default enabled)
		  Draw peaks in the analyzer (default enabled)
	  --spect-peak-width=<integer [-2147483648 .. 2147483647]>
								 Peak extra width
		  Additions or subtractions of pixels on the peak width.
	  --spect-peak-height=<integer [-2147483648 .. 2147483647]>
								 Peak height
		  Total pixel height of the peak items.

 libprojectM effect
	  --projectm-preset-path=<string>
								 projectM preset path
		  Path to the projectM preset directory
	  --projectm-title-font=<string>
								 Title font
		  Font used for the titles
	  --projectm-menu-font=<string>
								 Font menu
		  Font used for the menus
	  --projectm-width=<integer [-2147483648 .. 2147483647]>
								 Video width
		  The width of the video window, in pixels.
	  --projectm-height=<integer [-2147483648 .. 2147483647]>
								 Video height
		  The height of the video window, in pixels.
	  --projectm-meshx=<integer [-2147483648 .. 2147483647]>
								 Mesh width
		  The width of the mesh, in pixels.
	  --projectm-meshy=<integer [-2147483648 .. 2147483647]>
								 Mesh height
		  The height of the mesh, in pixels.
	  --projectm-texture-size=<integer [-2147483648 .. 2147483647]>
								 Texture size
		  The size of the texture, in pixels.

 Goom effect
	  --goom-width=<integer [-2147483648 .. 2147483647]>
								 Goom display width
		  This allows you to set the resolution of the Goom display (bigger
		  resolution will be prettier but more CPU intensive).
	  --goom-height=<integer [-2147483648 .. 2147483647]>
								 Goom display height
		  This allows you to set the resolution of the Goom display (bigger
		  resolution will be prettier but more CPU intensive).
	  --goom-speed=<integer [1 .. 10]>
								 Goom animation speed
		  This allows you to set the animation speed (between 1 and 10,
		  defaults to 6).
		  '''
		wx.Panel.__init__( self, parent = parent, id = wx.ID_ANY )
		
		initial_visual_effect, initial_equalizer_active, initial_equalizer_preset
		
		visual_effects_label = wx.StaticText( self, label ='Visual effects' )
		
		visual_effects_dropdown = wx.ComboBox( self, wx.ID_ANY, value = initial_visual_effect,  choices = ['dummy', 'scope', 'spectrum', 'spectrometer', 'vuMeter', 'libprojectM', 'goom' ])
		equalizer_ctrl = wx.CheckBox( self, wx.ID_ANY, 'Equalizer effects' )
		self.equalizer_presets_dropdown = wx.ComboBox( self, wx.ID_ANY, value = initial_equalizer_preset, style = wx.CB_READONLY|wx.CB_SORT, choices = ['flat', 'classical', 'club' ,'dance', 'fullbass', 'fullbasstreble', 'fulltreble', 'headphones', 'largehall', 'live', 'party', 'pop', 'reggae', 'rock', 'ska', 'soft', 'softrock', 'techno' ] )

		if( initial_equalizer_active ):
			equalizer_ctrl.SetValue( True )
		else:
			equalizer_ctrl.SetValue( False )
			self.equalizer_presets_dropdown.Enable( False )

		equalizer_ctrl.Bind( wx.EVT_CHECKBOX, self.EnableEqualizerPresets )
		
		ctrlbox = wx.BoxSizer( wx.VERTICAL )
		
		gridSizer = wx.FlexGridSizer( rows=2, cols=2, hgap=5, vgap=5 )
		gridSizer.AddGrowableCol( 1 )
		
		
		gridSizer.AddMany([
			( visual_effects_label,0,wx.ALIGN_CENTER_VERTICAL ), ( visual_effects_dropdown, 1, wx.EXPAND ),
			( equalizer_ctrl,0,wx.ALIGN_CENTER_VERTICAL ), ( self.equalizer_presets_dropdown, 1, wx.EXPAND )
		])
		ctrlbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL, border = 10 )
				
		self.SetSizer(ctrlbox)
		
	def EnableEqualizerPresets ( self, event ):
			 self.equalizer_presets_dropdown.Enable( event.GetEventObject().IsChecked() )
		
class SettingsControl( wx.Listbook ):
	def __init__(self, parent, minus_button_image, plus_button_image, SetStep = 10, SetMin = 0, SetMax = 200, initial_brightness = 0, initial_contrast = 0, SetBrightnessCallback = None, SetContrastCallback = None, initial_visual_effect = '', initial_equalizer_active = False, initial_equalizer_preset = '' ):
		"""Constructor"""
		wx.Listbook.__init__(self, parent, wx.ID_ANY, style=
							wx.BK_DEFAULT
							#wx.BK_TOP
							#wx.BK_BOTTOM
							#wx.BK_LEFT
							#wx.BK_RIGHT
							)
		img_panel = ImageSettingsPanel( self, minus_button_image, plus_button_image, SetStep, SetMin, SetMax, initial_brightness, initial_contrast, SetBrightnessCallback, SetContrastCallback )
		audio_panel = AudioSettingsPanel( self, initial_visual_effect, initial_equalizer_active, initial_equalizer_preset )
		pages = [ 
			( img_panel, "Image" ),
			( audio_panel, "Sound")#,
			#( General( self ), "General")
		]
		
		for page, label in pages:
			self.AddPage( page, label )
			
		#self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
		#self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)
