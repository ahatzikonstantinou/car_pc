# CarPC_RDSDecoder
# Module for decoding RDS data from a V4L2 compatible FM radio device
#
# Copyright (C) 2010 <ahatzikonstantinou@gmail.com>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free 
# Software Foundation; either version 2.1 of the License, or (at your option) 
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA

from v4l2radio import *
import wx
import time
from wx.lib.pubsub import Publisher

class CarPC_RDSDecoderListener(RDSDecoderListener):
    """
    This class should be used as a base class for objects registered
    using Decoder.set_listener()
    """
    PSLEN = 8
    
    def __init__( self, publisher_message_name, rdsTextLength = 20 ):
        #self.frame = frame
        self.publisher_message_name = publisher_message_name
        self.rdsTextLength = rdsTextLength
        self.rdsText = ''
        self.ps = ''
        self.start = 0
        self.threshold = 1.1
        self.windowSize = 10
        self.window = self.windowSize*[None]
        self.currentPos = 0
    
    def on_pi_change(self, decoder, pi):
        """
        Called when the PI code changes
        """
        #print( 'pi:{}'.format( pi ) )
        pass
    
    def on_ecc_change(self, decoder, ecc):
        """
        Called when the ECC changes
        """
        #print( 'ecc:{}'.format( ecc ) )
        pass
    
    def on_ps_change(self, decoder, ps):
        """
        Called when the PS value changes
        """
        #print( 'ps:{}'.format( ps ) )
        wx.CallAfter(Publisher().sendMessage, self.publisher_message_name, ps )
        return
        
        if( self.start == 0 ):            
            self.start = time.clock()
            self.ps = ps
            return
        
        end = time.clock()    
        interval = end - self.start
        self.start = end
     
        lastPos = self.currentPos
        self.currentPos = ( self.currentPos + 1 ) % self.windowSize
        self.window[lastPos] = interval        
        if( None in self.window ):
            return
            
        #from pprint import pprint ; pprint( self.window )

        avg = sum( self.window ) / float( self.windowSize )
        print( 'avg:{}, time:{}, ps:{}, previous ps:{}'.format( avg, interval, ps, self.ps ) )
        if( self.window[lastPos] > self.threshold*avg ):
            start = 0 
            if( len( self.rdsText ) + len( self.ps ) > self.rdsTextLength ):
                start = self.rdsTextLength - ( len( self.rdsText ) + len( self.ps ) )
            self.rdsText = self.rdsText[ start:] + self.ps
            print( 'peak detected sending:{}'.format( self.rdsText ) )
            wx.CallAfter(Publisher().sendMessage, "update_rds", self.rdsText )
        
        self.ps = ps.strip() + ' '
        return
        
    
    def on_rt_change(self, decoder, message):
        """
        Called when a new RadioText message is received
        """
        #print( 'message:{}'.format( message ) )
    
    def on_reset(self, decoder):
        """
        Called when the RDS Decoder is reset, usually when changing the tuner's frequency
        """
        #self.frame.rdsText.SetLabel( '' )
        pass
