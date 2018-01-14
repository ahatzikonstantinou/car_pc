#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import logging

class ImageSettingsPanel( wx.Panel ):
	def __init__( self, parent, minus_button_image, plus_button_image, SetStep = 10, SetMin = 0, SetMax = 200, initial_brightness = 0, initial_contrast = 0, initial_gamma = 0, initial_hue = 0, initial_saturation = 0,	SetBrightnessCallback = None, SetContrastCallback = None, SetGammaCallback = None, SetHueCallback = None, SetSaturationCallback = None, 
	scale = { 
		'brightness': { 'step': 10, 'min': 0, 'max': 200, 'factor': 100.0, 'default': 1.0 },
		'contrast': { 'step': 10, 'min': 0, 'max': 200, 'factor': 100.0, 'default': 1.0 },
		'gamma': { 'step': 10, 'min': 1, 'max': 1000, 'factor': 100.0, 'default': 1.0 },
		'hue': { 'step': 10, 'min': 0, 'max': 360, 'factor': 1, 'default': 0 },
		'saturation': { 'step': 10, 'min': 0, 'max': 300, 'factor': 100.0, 'default': 1.0 }
		} 
	):
		wx.Panel.__init__( self, parent = parent, id = wx.ID_ANY )
		
		self.scale = scale
		#self.SetStep = SetStep
		#self.SetMin = SetMin
		#self.SetMax = SetMax
		
		self.brightness = initial_brightness
		self.contrast = initial_contrast
		self.gamma = initial_gamma
		#self.hue = initial_hue
		#self.saturation = initial_saturation
		
		self.SetBrightnessCallback = SetBrightnessCallback
		self.SetContrastCallback = SetContrastCallback
		self.SetGammaCallback = SetGammaCallback
		#self.SetHueCallback = SetHueCallback
		#self.SetSaturationCallback = SetSaturationCallback

		#nb = wx.Notebook( self )
		
		#bp = wx.Panel( nb )
		bp = self
		brightnessL = wx.StaticText( bp, label="Brightness")
		minusBrightnessBtn = wx.StaticBitmap( bp, bitmap = minus_button_image )
		plusBrightnessBtn = wx.StaticBitmap( bp, bitmap = plus_button_image )
		self.brightnessSlider = wx.Slider( bp, -1, self.brightness, self.scale['brightness']['min'], self.scale['brightness']['max'], size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		
		#cp = wx.Panel( nb )
		cp = self
		contrastL = wx.StaticText( cp, label="Contrast")
		minusContrastBtn = wx.StaticBitmap( cp, bitmap = minus_button_image )
		plusContrastBtn = wx.StaticBitmap( cp, bitmap = plus_button_image )
		self.contrastSlider = wx.Slider( cp, -1, self.contrast, self.scale['contrast']['min'], self.scale['contrast']['max'], size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		
		#gp = wx.Panel( nb )
		gp = self
		gammaL = wx.StaticText( gp, label="Gamma")
		minusGammaBtn = wx.StaticBitmap( gp, bitmap = minus_button_image )
		plusGammaBtn = wx.StaticBitmap( gp, bitmap = plus_button_image )
		self.gammaSlider = wx.Slider( gp, -1, self.gamma, self.scale['gamma']['min'], self.scale['gamma']['max'], size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		
		#hp = wx.Panel( nb )
		#hueL = wx.StaticText( hp, label="Hue")
		#minusHueBtn = wx.StaticBitmap( hp, bitmap = minus_button_image )
		#plusHueBtn = wx.StaticBitmap( hp, bitmap = plus_button_image )
		#self.hueSlider = wx.Slider( hp, -1, self.hue, self.scale['hue']['min'], self.scale['hue']['max'], size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		
		#sp = wx.Panel( nb )
		#saturationL = wx.StaticText( sp, label="Saturation")
		#minusSaturationBtn = wx.StaticBitmap( sp, bitmap = minus_button_image )
		#plusSaturationBtn = wx.StaticBitmap( sp, bitmap = plus_button_image )
		#self.saturationSlider = wx.Slider( sp, -1, self.saturation, self.scale['saturation']['min'], self.scale['saturation']['max'], size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)

		resetBtn = wx.Button( self, wx.ID_ANY, label='Reset' )
		# Bind controls to events
		
		self.Bind( wx.EVT_SLIDER, self.OnSetBrightness, self.brightnessSlider )
		self.Bind( wx.EVT_SLIDER, self.OnSetContrast, self.contrastSlider )
		self.Bind( wx.EVT_SLIDER, self.OnSetGamma, self.gammaSlider )
		#self.Bind( wx.EVT_SLIDER, self.OnSetHue, self.hueSlider )
		#self.Bind( wx.EVT_SLIDER, self.OnSetSaturation, self.saturationSlider )
		
		minusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseBrightness )
		plusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseBrightness )
		minusContrastBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseContrast )
		plusContrastBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseContrast )
		minusGammaBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseGamma )
		plusGammaBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseGamma )
		#minusHueBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseHue )
		#plusHueBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseHue )
		#minusSaturationBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseSaturation )
		#plusSaturationBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseSaturation )
		resetBtn.Bind( wx.EVT_BUTTON, self.Reset )

		# Give a pretty layout to the controls
		ctrlbox = wx.BoxSizer( wx.HORIZONTAL )
		vbox = wx.BoxSizer( wx.VERTICAL )
		
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
		
		gbox = wx.BoxSizer( wx.HORIZONTAL )
		gbox.Add( minusGammaBtn, 0, wx.CENTER )
		gbox.Add( self.gammaSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		gbox.Add( plusGammaBtn, 0, wx.CENTER )
		
		#hbox = wx.BoxSizer( wx.HORIZONTAL )
		#hbox.Add( minusHueBtn, 0, wx.CENTER )
		#hbox.Add( self.hueSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		#hbox.Add( plusHueBtn, 0, wx.CENTER )
		#
		#sbox = wx.BoxSizer( wx.HORIZONTAL )
		#sbox.Add( minusSaturationBtn, 0, wx.CENTER )
		#sbox.Add( self.saturationSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		#sbox.Add( plusSaturationBtn, 0, wx.CENTER )
		
		gridSizer.AddMany([
			( brightnessL,0,wx.ALIGN_CENTER_VERTICAL ), ( bbox, 1, wx.EXPAND ),
			( contrastL,0,wx.ALIGN_CENTER_VERTICAL ), ( cbox, 1, wx.EXPAND ),
			( gammaL,0,wx.ALIGN_CENTER_VERTICAL ), ( gbox, 1, wx.EXPAND ),
			#( hueL,0,wx.ALIGN_CENTER_VERTICAL ), ( hbox, 1, wx.EXPAND ),
			#( saturationL,0,wx.ALIGN_CENTER_VERTICAL ), ( sbox, 1, wx.EXPAND )
		])
		vbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL, border = 10 )
		ctrlbox.Add( vbox, 1, wx.EXPAND | wx.ALL, border = 10 )
		ctrlbox.Add( resetBtn, 0, wx.ALL, border = 10 )

		#bp.SetSizer( bbox )
		#cp.SetSizer( cbox )
		#gp.SetSizer( gbox )
		#hp.SetSizer( hbox )
		#sp.SetSizer( sbox )
		#nb.AddPage( bp, 'Brightness' )
		#nb.AddPage( cp, 'Contrast' )
		#nb.AddPage( gp, 'Gamma' )
		#nb.AddPage( hp, 'Hue' )
		#nb.AddPage( sp, 'Saturation' )
		#ctrlbox.Add( nb, 1, wx.EXPAND )
				
		self.SetSizer(ctrlbox)

	def _Increase( self, slider, parameter_name, OnSetFunction ):
		value = slider.GetValue()
		smax = self.scale[parameter_name]['max']
		if( value >= smax ):
			logging.debug( '{}:{} >= max:{}'.format( parameter_name, value, smax ) )
			return
		value += self.scale[parameter_name]['step']
		slider.SetValue( value )
		OnSetFunction()
		
	def _Decrease( self, slider, parameter_name, OnSetFunction ):
		value = slider.GetValue()
		smin = self.scale[parameter_name]['min']
		if( value <= smin ):
			logging.debug( '{}:{} <= min:{}'.format( parameter_name, value, smin ) )
			return
		value -= self.scale[parameter_name]['step']
		slider.SetValue( value )
		OnSetFunction()
		
	def _OnSet( self, local_param, parameter_name, slider, Callback ):
		local_param = slider.GetValue()/self.scale[parameter_name]['factor']
		logging.debug( 'new {}: {}'.format( parameter_name, local_param ) )
		if( Callback ):
			Callback( local_param )
	
	def _Set( self, local_param, value, slider, parameter_name ):
		local_param = value
		slider.SetValue( local_param * self.scale[parameter_name]['factor'] )

	def IncreaseBrightness( self, event ):
		self._Increase( self.brightnessSlider, 'brightness', self.OnSetBrightness )

	def DecreaseBrightness( self, event ):
		self._Decrease( self.brightnessSlider, 'brightness', self.OnSetBrightness )

	def IncreaseContrast( self, event ):
		self._Increase( self.contrastSlider, 'contrast', self.OnSetContrast )

	def DecreaseContrast( self, event ):
		self._Decrease( self.contrastSlider, 'contrast', self.OnSetContrast )
	
	def IncreaseGamma( self, event ):
		self._Increase( self.gammaSlider, 'gamma', self.OnSetGamma )

	def DecreaseGamma( self, event ):
		self._Decrease( self.gammaSlider, 'gamma', self.OnSetGamma )
	
	def IncreaseHue( self, event ):
		self._Increase( self.hueSlider, 'hue', self.OnSetHue )

	def DecreaseHue( self, event ):
		self._Decrease( self.hueSlider, 'hue', self.OnSetHue )

	def IncreaseSaturation( self, event ):
		self._Increase( self.saturationSlider, 'saturation', self.OnSetSaturation )

	def DecreaseSaturation( self, event ):
		self._Decrease( self.saturationSlider, 'saturation', self.OnSetSaturation )

	def OnSetBrightness(self, evt=None):
		"""
		Set the brightness according to the brightness slider.
		"""
		#self.brightness = self.brightnessSlider.GetValue() * 2
		#print( 'new brightness: {}'.format( self.brightness ) )
		#if( self.SetBrightnessCallback ):
			#self.SetBrightnessCallback( self.brightness )
		self._OnSet( self.brightness, 'brightness', self.brightnessSlider, self.SetBrightnessCallback )

	def OnSetContrast(self, evt=None):
		"""
		Set the contrast according to the contrast slider.
		"""
		#self.contrast = self.contrastSlider.GetValue() * 2
		#print( 'new contrast: {}'.format( self.contrast ) )
		#if( self.SetContrastCallback ):
			#self.SetContrastCallback( self.contrast )
		self._OnSet( self.contrast, 'contrast', self.contrastSlider, self.SetContrastCallback )

	def OnSetGamma(self, evt=None):
		"""
		Set the gamma according to the gamma slider.
		"""
		#self.gamma = self.gammaSlider.GetValue() * 2
		#print( 'new gamma: {}'.format( self.gamma ) )
		#if( self.SetGammaCallback ):
			#self.SetGammaCallback( self.gamma )
		self._OnSet( self.gamma, 'gamma', self.gammaSlider, self.SetGammaCallback )

	def OnSetHue(self, evt=None):
		"""
		Set the hue according to the hue slider.
		"""
		#self.hue = self.hueSlider.GetValue() * 2
		#print( 'new hue: {}'.format( self.hue ) )
		#if( self.SetHueCallback ):
			#self.SetHueCallback( self.hue )
		self._OnSet( self.hue, 'hue', self.hueSlider, self.SetHueCallback )

	def OnSetSaturation(self, evt=None):
		"""
		Set the saturation according to the saturation slider.
		"""
		#self.saturation = self.saturationSlider.GetValue() * 2
		#print( 'new saturation: {}'.format( self.saturation ) )
		#if( self.SetSaturationCallback ):
			#self.SetSaturationCallback( self.saturation )
		self._OnSet( self.saturation, 'saturation', self.hueSlider, self.SetSaturationCallback )

	def SetBrightness( self, brightness ):
		'''
		Will be called e.g. when a new device is activated and the control shoudl be updated to the current brightness value of the new device
		'''
		#self.brightness = brightness
		#self.brightnessSlider.SetValue( self.brightness )
		self._Set( self.brightness, brightness, self.brightnessSlider, 'brightness' )
	
	def SetContrast( self, contrast ):
		'''
		Will be called e.g. when a new device is activated and the control shoudl be updated to the current contrast value of the new device
		'''
		#self.contrast = contrast
		#self.contrastSlider.SetValue( self.contrast )
		self._Set( self.contrast, contrast, self.contrastSlider, 'contrast' )

	def SetGamma( self, gamma ):
		'''
		Will be called e.g. when a new device is activated and the control shoudl be updated to the current gamma value of the new device
		'''
		self._Set( self.gamma, gamma, self.gammaSlider, 'gamma' )

	#def SetHue( self, hue ):
		#'''
		#Will be called e.g. when a new device is activated and the control shoudl be updated to the current hue value of the new device
		#'''
		#self._Set( self.hue, hue, self.hueSlider, 'hue' )
#
	#def SetSaturation( self, saturation ):
		'''
		Will be called e.g. when a new device is activated and the control shoudl be updated to the current saturation value of the new device
		'''
		#self._Set( self.saturation, saturation, self.saturationSlider, 'saturation' )

	def Reset( self, event ):
		self.brightnessSlider.SetValue( self.scale['brightness']['default']*self.scale['brightness']['factor'] )
		self.OnSetBrightness()
		self.contrastSlider.SetValue( self.scale['contrast']['default']*self.scale['contrast']['factor'] )
		self.OnSetContrast()
		self.gammaSlider.SetValue( self.scale['gamma']['default']*self.scale['gamma']['factor'] )
		self.OnSetGamma()
		
		
	def errorDialog(self, errormessage):
		"""
		Display a simple error dialog.
		"""
		edialog = wx.MessageDialog( self, errormessage, 'Error', wx.OK|wx.ICON_ERROR )
		edialog.ShowModal()

class AudioSettingsPanel( wx.Panel ):
	def __init__( self, parent, minus_button_image, plus_button_image, initial_visual_effect = '', initial_equalizer_active = False, initial_equalizer_preset = '', SetStep = 10, SetMin = 0, SetMax = 100, initial_preamp = 0, SetPreampCallback = None ):
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
		
		#visual_effects_label = wx.StaticText( self, label ='Visual effects' )
		#
		#visual_effects_dropdown = wx.ComboBox( self, wx.ID_ANY, value = initial_visual_effect,  choices = ['dummy', 'scope', 'spectrum', 'spectrometer', 'vuMeter', 'libprojectM', 'goom' ])
		#equalizer_ctrl = wx.CheckBox( self, wx.ID_ANY, 'Equalizer effects' )
		#self.equalizer_presets_dropdown = wx.ComboBox( self, wx.ID_ANY, value = initial_equalizer_preset, style = wx.CB_READONLY|wx.CB_SORT, choices = ['flat', 'classical', 'club' ,'dance', 'fullbass', 'fullbasstreble', 'fulltreble', 'headphones', 'largehall', 'live', 'party', 'pop', 'reggae', 'rock', 'ska', 'soft', 'softrock', 'techno' ] )

		#if( initial_equalizer_active ):
			#equalizer_ctrl.SetValue( True )
		#else:
			#equalizer_ctrl.SetValue( False )
			#self.equalizer_presets_dropdown.Enable( False )

		#equalizer_ctrl.Bind( wx.EVT_CHECKBOX, self.EnableEqualizerPresets )
		
		self.SetStep = SetStep
		self.SetMin = -100 #SetMin
		self.SetMax = 100 #SetMax
		
		self.preamp = initial_preamp
				
		self.SetPreampCallback = SetPreampCallback
		preampL = wx.StaticText( self, label="Preamp")
		minusPreampBtn = wx.StaticBitmap( self, bitmap = minus_button_image )
		plusPreampBtn = wx.StaticBitmap( self, bitmap = plus_button_image )
		self.preampSlider = wx.Slider( self, -1, self.preamp, self.SetMin, self.SetMax, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		self.Bind( wx.EVT_SLIDER, self.OnSetPreamp, self.preampSlider )
		minusPreampBtn.Bind( wx.EVT_LEFT_UP, self.DecreasePreamp )
		plusPreampBtn.Bind( wx.EVT_LEFT_UP, self.IncreasePreamp )
		
		ctrlbox = wx.BoxSizer( wx.VERTICAL )
		
		gridSizer = wx.FlexGridSizer( rows=2, cols=2, hgap=5, vgap=5 )
		gridSizer.AddGrowableCol( 1 )
		
		pbox = wx.BoxSizer( wx.HORIZONTAL )
		pbox.Add( minusPreampBtn, 0, wx.CENTER )
		pbox.Add( self.preampSlider, 1, wx.EXPAND|wx.CENTER|wx.BOTTOM, border=15 )
		pbox.Add( plusPreampBtn, 0, wx.CENTER )
		
		gridSizer.AddMany([
			#( visual_effects_label,0,wx.ALIGN_CENTER_VERTICAL ), ( visual_effects_dropdown, 1, wx.EXPAND ),
			#( equalizer_ctrl,0,wx.ALIGN_CENTER_VERTICAL ), ( self.equalizer_presets_dropdown, 1, wx.EXPAND )
			( preampL,0,wx.ALIGN_CENTER_VERTICAL ), ( pbox, 1, wx.EXPAND ),
		])
		ctrlbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL, border = 10 )
				
		self.SetSizer(ctrlbox)
		
	def IncreasePreamp( self, event ):
		preamp = self.preampSlider.GetValue()
		if( preamp >= self.SetMax ):
			print( 'preamp:{} >= self.SetMax:{}'.format( preamp, self.SetMax ) )
			return
		preamp += self.SetStep
		self.preampSlider.SetValue( preamp )
		self.OnSetPreamp()
		return

	def DecreasePreamp( self, event ):
		preamp = self.preampSlider.GetValue()
		if( preamp <= self.SetMin ):
			print( 'preamp:{} <= self.SetMax:{}'.format( preamp, self.SetMax ) )
			return
		preamp -= self.SetStep
		self.preampSlider.SetValue( preamp )
		self.OnSetPreamp()
		return
		
	def OnSetPreamp(self, evt=None):
		"""
		Set the preamp according to the preamp slider.
		"""
		self.preamp = self.preampSlider.GetValue()
		print( 'new preamp: {}'.format( self.preamp ) )
		if( self.SetPreampCallback ):
			self.SetPreampCallback( self.preamp )
		
	def SetPreamp( self, preamp ):
		'''
		Will be called e.g. when a new device is activated and the control shoudl be updated to the current preamp value of the new device
		'''
		self.preamp = preamp
		self.preampSlider.SetValue( self.preamp )
		
	def EnableEqualizerPresets ( self, event ):
			 self.equalizer_presets_dropdown.Enable( event.GetEventObject().IsChecked() )
		
class SettingsControl( wx.Listbook ):
	def __init__(self, parent, minus_button_image, plus_button_image, SetStep = 10, SetMin = 0, SetMax = 100, initial_brightness = 0, initial_contrast = 0, initial_gamma = 0, initial_hue = 0, initial_saturation = 0, SetBrightnessCallback = None, SetContrastCallback = None, SetGammaCallback = None, SetHueCallback = None, SetSaturationCallback = None, initial_visual_effect = '', initial_equalizer_active = False, initial_equalizer_preset = '', initial_preamp = 0, SetPreampCallback = None ):
		"""Constructor"""
		wx.Listbook.__init__(self, parent, wx.ID_ANY, style=
							wx.BK_DEFAULT
							#wx.BK_TOP
							#wx.BK_BOTTOM
							#wx.BK_LEFT
							#wx.BK_RIGHT
							)
		self.img_panel = ImageSettingsPanel( self, minus_button_image, plus_button_image, SetStep, SetMin, SetMax, initial_brightness, initial_contrast, initial_gamma, initial_hue, initial_saturation, SetBrightnessCallback, SetContrastCallback, SetGammaCallback, SetHueCallback, SetSaturationCallback )
		self.audio_panel = AudioSettingsPanel( self, minus_button_image, plus_button_image,initial_visual_effect, initial_equalizer_active, initial_equalizer_preset, SetStep, SetMin, SetMax, initial_preamp, SetPreampCallback )
		
		self.image_page = ( self.img_panel, "Image" )
		pages = [ 
			( self.audio_panel, "Sound"),
			#( self.img_panel, "Image" ),
			#( General( self ), "General")
		]
		
		for page, label in pages:
			self.AddPage( page, label )
			
		#self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
		#self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

	def ShowImageSettings( self ):
		self._ShowImageSettings( True )
		
	def HideImageSettings( self ):
		self._ShowImageSettings( False )
		
	def _ShowImageSettings( self, showTrueHideFalse ):
		#img_page = self.GetPage( 0 )
		if( showTrueHideFalse ):
			#img_page.Show()
			if( self.GetPageCount() == 1 ):
				self.AddPage( self.image_page[0], self.image_page[1] )
		else:
			#img_page.Hide()
			self.RemovePage( 1 )
