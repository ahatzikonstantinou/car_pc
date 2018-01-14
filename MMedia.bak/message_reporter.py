#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx.lib.pubsub import Publisher

class MessageReporter:
    def __init__( self, publisher_message_name ):
        self._publisher_message_name = publisher_message_name
    
    def ReportMessage( self, msg):
        wx.CallAfter(Publisher().sendMessage, self._publisher_message_name, msg )
