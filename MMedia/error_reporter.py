#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx.lib.pubsub import Publisher

class ErrorReporter:
    def __init__( self, publisher_message_name ):
        self._publisher_message_name = publisher_message_name
    
    def ReportError( self, error_msg):
        wx.CallAfter(Publisher().sendMessage, self._publisher_message_name, error_msg )
