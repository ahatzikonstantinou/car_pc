#! /usr/bin/python
# -*- coding: utf-8 -*-

# import external libraries
import wx # 2.8
import vlc

# import standard libraries
import os
import user

import time
import traceback

from state import *
from settings import *

class Camera(wx.Frame):
    """The main window has to deal with events.
    """
    SetStep = 10
    SetMin = 0
    SetMax = 200
    
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, pos=wx.DefaultPosition, size=(750, 450))
        
        self.device = 'v4l2:///dev/video0'

        self.State = State()
        self.State.Load()
        self.Settings = Settings()
        self.Settings.Load()

        self.device = self.State.device
        
        # Panels
        # The first panel holds the video and it's all black
        self.videopanel = wx.Panel(self, -1)
        self.videopanel.SetBackgroundColour(wx.BLACK)

        # The second panel holds controls
        self.ctrlpanel = wx.Panel(self, -1 )
        brightnessL = wx.StaticText(self.ctrlpanel, label="Brightness")
        minusBrightnessBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-minus.png' ) )
        plusBrightnessBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-plus.png' ) )
        self.brightnessSlider = wx.Slider(self.ctrlpanel, -1, self.State.brightness, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        contrastL = wx.StaticText(self.ctrlpanel, label="Contrast")
        minusContrastBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-minus.png' ) )
        plusContrastBtn = wx.StaticBitmap( self.ctrlpanel, bitmap = GetImage( 'button-plus.png' ) )
        self.contrastSlider = wx.Slider(self.ctrlpanel, -1, self.State.contrast, 0, 100, size=(100, -1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        deviceL = wx.StaticText( self.ctrlpanel, label='Device:' )
        self.deviceTxt = wx.TextCtrl( self.ctrlpanel )
        self.deviceTxt.SetValue( self.device )
        deviceBtn = wx.Button( self.ctrlpanel, label='Ok' )
        maxImageBtn = wx.ToggleButton( self.ctrlpanel, wx.ID_ANY, 'Maximize' )
        maxImageBtn.SetValue( self.State.maxImage )
        self.maxImage = self.State.maxImage

        # Bind controls to events
        self.videopanel.Bind( wx.EVT_LEFT_UP, self.VideopanelClicked )
        
        self.Bind(wx.EVT_SLIDER, self.OnSetBrightness, self.brightnessSlider)
        self.Bind(wx.EVT_SLIDER, self.OnSetContrast, self.contrastSlider)
        minusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseBrightness )
        plusBrightnessBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseBrightness )
        minusContrastBtn.Bind( wx.EVT_LEFT_UP, self.DecreaseContrast )
        plusContrastBtn.Bind( wx.EVT_LEFT_UP, self.IncreaseContrast )
        maxImageBtn.Bind( wx.EVT_TOGGLEBUTTON, self.MaxImage )  
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
        dbox.Add( deviceBtn, 0 )
        gridSizer.AddMany([
            ( brightnessL,0,wx.ALIGN_CENTER_VERTICAL ), ( bbox, 1, wx.EXPAND ),
            ( contrastL,0,wx.ALIGN_CENTER_VERTICAL ), ( cbox, 1, wx.EXPAND ),
            ( deviceL, 0,wx.ALIGN_CENTER_VERTICAL ), ( dbox, 1, wx.EXPAND )
        ])
        ctrlbox.Add( gridSizer, 1, wx.EXPAND | wx.ALL )
        ctrlbox.Add( maxImageBtn, 0, wx.TOP|wx.BOTTOM, border = 20 )
                
        self.ctrlpanel.SetSizer(ctrlbox)
        # Put everything together
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        self.sizer.Add(self.ctrlpanel, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(self.sizer)
        #self.SetMinSize((350, 300))

        self.ctrlpanel.Hide()
        self.ctrlPanelHidden = True
        
        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        m = self.Instance.media_new( self.device )
        self.player.set_media( m )
        self.SetTitle("Rear Camera")
        
        #Show the main application window so that the window is rendered,
        #it gets a handle from the operating system in order to pass it on
        #to the player, to display its content
        self.Show()
        # set the window id where to render VLC's video output
        self.player.set_xwindow(self.videopanel.GetHandle())        
        
        self.player.play()            
        
        #Without the time delay, enabling image adjustment crashes the application
        #for some reason
        time.sleep( 1 )
        
        self.player.video_set_adjust_int( vlc.VideoAdjustOption.Enable, 1 )
        self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, self.State.brightness/50.0 )
        self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, self.State.contrast/50.0 )
        #
        #brightness = self.player.video_get_adjust_float( vlc.VideoAdjustOption.Brightness )
        #print( 'brightness:{}'.format( brightness ) )
        #contrast = self.player.video_get_adjust_float( vlc.VideoAdjustOption.Contrast )
        #print( 'contrast:{}'.format( contrast ) )
        #scale = self.player.video_get_scale()
        #print( 'scale:{}'.format( scale ) )
        #ar = self.player.video_get_aspect_ratio()
        #print( 'aspect ratio:{}'.format( ar ) )
        self.videoWidth = self.player.video_get_width()
        #print( 'width:{}'.format( self.videoWidth ) )
        self.videoHeight = self.player.video_get_height()
        #self.player.video_set_scale( 1.5 )
        
        self.videopanel.Bind(wx.EVT_SIZE, self.OnSize)
        self.UpdateVideoWidth()
        
    def SetDevice( self, event ):
        self.device = self.deviceTxt.GetValue()
        m = self.Instance.media_new( self.device )
        self.player.set_media( m )
        self.player.play()
        self.State.device = self.device
        self.State.Save()
    
    def __dump( self ):
        scale = self.player.video_get_scale()
        print( 'scale:{}'.format( scale ) )
        ar = self.player.video_get_aspect_ratio()
        print( 'aspect ratio:{}'.format( ar ) )
        self.videoWidth = self.player.video_get_width()
        print( 'width:{}'.format( self.videoWidth ) )
        self.videoHeight = self.player.video_get_height()
        print( 'height:{}'.format( self.videoHeight ) )
        
    def UpdateVideoWidth( self ):
        if( self.maxImage ):
            size = self.videopanel.GetClientSize()
            width = size[0]
            scale = 1.0
            if( self.videoWidth > 0 ):
				scale = float( width )/self.videoWidth
            self.player.video_set_scale( scale )
            diff = self.videoHeight - size[1]/scale
            if( diff > 0 ):
                self.player.video_set_crop_geometry( str( self.videoWidth ) + 'x' + str( self.videoHeight ) + '+0+' + str( diff ) )
        else:
            self.player.video_set_scale( 0.0 )
            self.player.video_set_crop_geometry( None ) 
        
    def OnSize( self, event ):
        self.UpdateVideoWidth()
        self.Layout()
        #self.__dump()
        return
        
    def IncreaseBrightness( self, event ):
        brightness = self.brightnessSlider.GetValue() * 2
        if( brightness >= Camera.SetMax ):
            print( 'brightness:{} >= Camera.SetMax:{}'.format( brightness, Camera.SetMax ) )
            return
        brightness += Camera.SetStep
        self.brightnessSlider.SetValue( brightness/2 )
        self.OnSetBrightness()
        return

    def DecreaseBrightness( self, event ):
        brightness = self.brightnessSlider.GetValue() * 2
        if( brightness <= Camera.SetMin ):
            print( 'brightness:{} <= Camera.SetMax:{}'.format( brightness, Camera.SetMax ) )
            return
        brightness -= Camera.SetStep
        self.brightnessSlider.SetValue( brightness/2 )
        self.OnSetBrightness()
        return
        
    def IncreaseContrast( self, event ):
        contrast = self.contrastSlider.GetValue() * 2
        if( contrast >= Camera.SetMax ):
            print( 'contrast:{} >= Camera.SetMax:{}'.format( contrast, Camera.SetMax ) )
            return
        contrast += Camera.SetStep
        self.contrastSlider.SetValue( contrast/2 )
        self.OnSetContrast()
        return
                    
    def DecreaseContrast( self, event ):
        contrast = self.contrastSlider.GetValue() * 2
        if( contrast <= Camera.SetMin ):
            print( 'contrast:{} <= Camera.SetMax:{}'.format( contrast, Camera.SetMax ) )
            return
        contrast -= Camera.SetStep
        self.contrastSlider.SetValue( contrast/2 )
        self.OnSetContrast()
        return
             
    def VideopanelClicked( self, event ):
        if( self.ctrlPanelHidden ):
            self.ctrlPanelHidden = False
            self.ctrlpanel.Show()
        else:
            self.ctrlPanelHidden = True
            self.ctrlpanel.Hide()
        self.Layout()
            
    def OnSetBrightness(self, evt=None):
        """Set the brightness according to the brightness slider.
        """
        brightness = self.brightnessSlider.GetValue() * 2
        print( 'new brightness: {}'.format( brightness ) )
        if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Brightness, brightness/100.0 ) == -1:
            self.errorDialog("Failed to set brightness")
        else:
            self.State.brightness = brightness/2
            self.State.Save()

    def OnSetContrast(self, evt=None):
        """Set the contrast according to the contrast slider.
        """
        contrast = self.contrastSlider.GetValue() * 2
        print( 'new contrast: {}'.format( contrast ) )
        if self.player.video_set_adjust_float( vlc.VideoAdjustOption.Contrast, contrast/100.0 ) == -1:
            self.errorDialog("Failed to set contrast")
        else:
            self.State.contrast = contrast/2
            self.State.Save()

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK|
                                                                wx.ICON_ERROR)
        edialog.ShowModal()

    def MaxImage( self, event ):
        self.maxImage = not self.maxImage
        self.State.maxImage = self.maxImage
        self.State.Save()
        self.UpdateVideoWidth()
        self.Layout()
        
def GetImage( imageFile, size ='48x48' ):
	imageDir = os.getcwd() + '/images/' + size + '/'
	imageFile = imageDir + imageFile
	image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	
	return image
if __name__ == "__main__":
    # Create a wx.App(), which handles the windowing system event loop
    app = wx.PySimpleApp()
    # Create the window containing our small media player
    camera = Camera("Simple PyVLC Player")
    # show the player window centred and run the application
    camera.Centre()
    camera.Show()
    app.MainLoop()
