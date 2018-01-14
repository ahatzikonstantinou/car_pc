#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
import os

from TV import *

class TVGui( wx.Frame ):
	def __init__(self, parent, title):	
		super( TVGui, self).__init__(parent, title=title, size=(750, 420))
		self.tv = TV()
		self.tv.LoadChannels()
		self.state = State()
		self.state.Load()
		self.InitUI()
		
	def InitUI(self):
        # Panels
        # The first panel holds the video and it's all black
		self.videopanel = wx.Panel(self)
		self.videopanel.SetBackgroundColour(wx.BLACK)

        # The second panel holds controls
        self.ctrlpanel = wx.Panel(self, -1 )

		# The stations panel
		self.stationsPanel = wx.Panel(self)
