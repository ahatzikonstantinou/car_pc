# FMRadio
# Module for controlling a V4L2 FM radio device via Python
#
# Heavily based upon the original work of Martin Grimme:
# Copyright (C) 2007 - 2008 Martin Grimme  <martin.grimme _AT_ lintegra.de>
#
# Modified by Andy Buckingham <andy.buckingham@thisisglobal.com> to make
# generic for any V4L2 FM radio device and to add support for RDS module.
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


# make 'from FMRadio import *' safe
__all__ = ["FMRadio", "FMRadioError", "FMRadioUnavailableError",
           "FMRadioOperationNotSupportedError"]


from RDSDecoder import RDSDecoder
#from RDSDecoderCore import RDSDecoderCore
import os
from fcntl import ioctl
import struct
import time
import threading

# kernel definitions for ioctl commands
_IOC_NRBITS   = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS  = 2

_IOC_NRSHIFT   = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT  = _IOC_SIZESHIFT + _IOC_SIZEBITS

_IOC_WRITE = 1
_IOC_READ  = 2

_IOC  = lambda d,t,nr,size: (d << _IOC_DIRSHIFT) | (ord(t) << _IOC_TYPESHIFT) | \
                            (nr << _IOC_NRSHIFT) | (size << _IOC_SIZESHIFT)
_IOW  = lambda t,nr,size: _IOC(_IOC_WRITE, t, nr, size)
_IOR  = lambda t,nr,size: _IOC(_IOC_READ, t, nr, size)
_IOWR = lambda t,nr,size: _IOC(_IOC_READ | _IOC_WRITE, t, nr, size)

# V4L2 stuff for accessing the tuner driver
_VIDIOC_G_TUNER     = _IOWR('V', 29, 84)
_VIDIOC_G_AUDIO     = _IOR ('V', 33, 52)
_VIDIOC_S_AUDIO     = _IOW ('V', 34, 52)
_VIDIOC_G_FREQUENCY = _IOWR('V', 56, 44)
_VIDIOC_S_FREQUENCY = _IOW ('V', 57, 44)
_VIDIOC_G_CTRL      = _IOWR('V', 27, 8)
_VIDIOC_S_CTRL      = _IOWR('V', 28, 8)

# tuner capabilities
_V4L2_TUNER_CAP_LOW    = 0x0001
_V4L2_TUNER_CAP_NORM_  = 0x0002
_V4L2_TUNER_CAP_STEREO = 0x0010
_V4L2_TUNER_CAP_LANG2  = 0x0020
_V4L2_TUNER_CAP_SAP    = 0x0020

# rxsubchans flags
_V4L2_TUNER_SUB_MONO   = 0x0001
_V4L2_TUNER_SUB_STEREO = 0x0002
_V4L2_TUNER_SUB_LANG2  = 0x0004
_V4L2_TUNER_SUB_SAP    = 0x0004
_V4L2_TUNER_SUB_LANG1  = 0x0008

# user-class control IDs defined by V4L2
_V4L2_CTRL_CLASS_USER = 0x00980000
_V4L2_CID_BASE        = _V4L2_CTRL_CLASS_USER | 0x900
_V4L2_CID_FM_BAND     = _V4L2_CID_BASE + 0

# signal scanning parameters
_SIGNAL_LOCK_TIME = 0.1
_SIGNAL_TRIES = 1
_SIGNAL_SAMPLE_SLEEP = 0.005
_SIGNAL_THRESHOLD = 20
_SCAN_STEP_KHZ = 50


class FMRadioError(StandardError):
    """
    Base class for FMRadio-related exceptions.
    """
    pass

class FMRadioUnavailableError(FMRadioError):
    """
    Exception to throw if the radio is unavailable.
    """
    pass
    
class FMRadioOperationNotSupportedError(FMRadioError):
    """
    Exception to throw when calling an unsupported operation.
    """
    pass
    

class FMRadio(object):
    """
    Class for controlling the radio.
    """
    MAX_SIGNAL_STRENGTH = 100
    # FM bands
    FM_BAND_EUR = 0
    FM_BAND_JPN = 1
    
    def __init__(self, dev="/dev/radio0", enable_rds=True):
        
        self.dev = dev
        self.__is_scanning = False
        
        try:            
            self.__fd = os.open(self.dev, os.O_RDONLY | os.O_NONBLOCK)
            self.deviceLock = threading.RLock()
        except OSError:
            raise FMRadioUnavailableError("FM radio is not available.")
        
        #self.rds = RDSDecoderCore(self, self.__fd) if enable_rds else None
        self.rds = RDSDecoder(self, self.__fd) if enable_rds else None
        
        self.__tuner = self.__get_tuner()
        self.__factor = (self.__tuner["capability"] & _V4L2_TUNER_CAP_LOW) \
                        and 16 or 0.016      
        self.__freq_range = (self.__tuner["rangelow"] / self.__factor,
                             self.__tuner["rangehigh"] / self.__factor)        

    def Refresh( self ):
        self.__tuner = self.__get_tuner()
        
    def IsStereo( self ):
        return self.__tuner["audmode"]
        
    
    def __get_tuner(self):
        """
        Returns information about the tuner.
        """
        #tries = 3
        #finished = False
        #try:
            #while( tries > 0 and not finished ):
        #try:
        with self.deviceLock:
            data = ioctl(self.__fd, _VIDIOC_G_TUNER, struct.pack("84x"))
        #except:
            #print( 'Error' )
        #print( 'Finished' )
        #import sys
        #sys.exit(0)
        #data = ioctl(self.__fd, _VIDIOC_G_TUNER, struct.pack("136x"))

        fmt = "I32sIIIIIIii4I" #"L32sLLLLLll4L"
        #print( 'fmt ="{}", calcsize(fmt)={} ~ len(data)={}'.format( fmt, struct.calcsize(fmt), len(data) ) ) 
  
        fields = struct.unpack( fmt, data)
        tuner = { "index": fields[0],
            "name": fields[1],
            "type": fields[2],
            "capability": fields[3],
            "rangelow": fields[4],
            "rangehigh": fields[5],
            "rxsubchans": fields[6],
            "audmode": fields[7],
            "signal": fields[8],
            "afc": fields[9] }
        #finished = True
        #print( 'get tuner worked fine' )

        #for i in tuner.items():
            #print( '{}: {}'.format( i[0], unicode( i[1] ) ) )
        #print( 'rxsubchans:{}'.format( tuner["rxsubchans"] ) )
        return tuner
        #except:
            #print( 'get tuner error at try {}'.format( tries ) )
            #tries -= 1
            #
        #return None
        

    def close(self):
        """
        Closes the radio and powers off the FM tuner chip.
        """
        
        if self.rds:
            self.rds.close()
        
        self.cancel_scanning()        
        self.set_frequency(0)
        with self.deviceLock:
            os.close(self.__fd)
        

    def set_fm_band(self, band):
        """
        Sets the FM band to the given value.
        """
        
        assert band in (self.FM_BAND_EUR, self.FM_BAND_JPN)
        
        inp = struct.pack("Ii", _V4L2_CID_FM_BAND, band)
        try:        
            with self.deviceLock:
                ioctl(self.__fd, _VIDIOC_S_CTRL, inp)
        except:
            raise FMRadioOperationNotSupportedError(
                      "FM tuner driver does not support switching the FM band")
        
        # changing the FM band invalidates our stored frequency range so that
        # we have to read it again
        self.__tuner = self.__get_tuner()
        self.__freq_range = (self.__tuner["rangelow"] / self.__factor,
                             self.__tuner["rangehigh"] / self.__factor)        
        

    def get_fm_band(self):
        """
        Returns the current FM band. This is either FM_BAND_EUR for the
        US/Europe FM band and FM_BAND_JPN for the Japanese FM band.
        """
        
        inp = struct.pack("Ii", _V4L2_CID_FM_BAND, 0)
        try:
            with self.deviceLock:
                data = ioctl(self.__fd, _VIDIOC_G_CTRL, inp)
        except:
            # we may assume that if the operation is unsupported, the band
            # is set to US/Europe
            band = self.FM_BAND_EUR
        else:
            fields = struct.unpack("Ii", data)
            band = fields[1]
        
        return band
        

    def get_frequency_range(self):
        """
        Returns the supported frequency range as a (low, high) tuple.
        The range depends on the selected FM band.
        """
        
        low, high = self.__freq_range
        return (low, high)
        

    def get_frequency(self):
        """
        Returns the current frequency value.
        """
        #print ('FMRadio will try to get_frequency' )
        fmt = "III8I" #"LLL8L"
        inp = struct.pack( fmt,
                          self.__tuner["index"],
                          self.__tuner["type"],
                          0, 0, 0, 0, 0, 0, 0, 0, 0)
        with self.deviceLock:
            data = ioctl(self.__fd, _VIDIOC_G_FREQUENCY, inp)
            #print ('FMRadio get_frequency read the device' )
        fields = struct.unpack(fmt, data)
        #print ('FMRadio get_frequency unpacked the data' )
        freq = fields[2]
        freq = int(freq / self.__factor / float(_SCAN_STEP_KHZ) + 0.5) * \
               _SCAN_STEP_KHZ
        
        return freq
        

    def set_frequency(self, freq):
        """
        Sets the frequency to the given value.
        """
        
        self.cancel_scanning()
        self.__set_frequency(freq)
        
        if self.rds and freq is not 0:
            self.rds.reset()
            
        #print( 'FMRadio finished set_frequency' )
        

    def __set_frequency(self, freq):
        """
        Internal method for setting frequency to avoid cancelling scanning
        """
        
        low, high = self.__freq_range
        # a frequency of 0 tells the FM tuner to power down
        debugFreq = int(freq * self.__factor)
        #print( 'FMRadio will try to tune to {}MHz'.format( freq ) )
        #print( 'freq:{}, factor:{} assert {} <= freq <= {}'.format( debugFreq, self.__factor, low, high ) )
        assert(freq == 0 or low <= freq <= high)
        #print( 'FMRadio __set_frequency: self.__tuner["index"]={0}, self.__tuner["type"]={1}, freq={2}'.format( self.__tuner["index"], self.__tuner["type"], int(freq * self.__factor) ) )
        fmt = "III8I" #"LLL8L"
        inp = struct.pack( fmt,
                          self.__tuner["index"],
                          self.__tuner["type"],
                          #freq, 0, 0, 0, 0, 0, 0, 0, 0)
                          int(freq * self.__factor), 0, 0, 0, 0, 0, 0, 0, 0)
        with self.deviceLock:
            ioctl(self.__fd, _VIDIOC_S_FREQUENCY, inp)
        #print( 'FMRadio finished __set_frequency' )
        
    def get_stereo( self ):
        """
        Returns 1 on stereo, o on mono
        """
        
        self.__tuner = self.__get_tuner()
        mode = int( self.__tuner["rxsubchans"] )& _V4L2_TUNER_SUB_STEREO
        #print( 'rxsubchans:{}, _V4L2_TUNER_SUB_STEREO:{} => stereo mode:{}'.format( 
            #self.__tuner["rxsubchans"], _V4L2_TUNER_SUB_STEREO, mode ) )
        return mode
        
        #fmt = "I32sII2I"
        #inp = struct.pack( fmt, self.__tuner["index"], self.__tuner["name"], 0, 0, 0, 0 )
        #with self.deviceLock:
            #data = ioctl( self.__fd, _VIDIOC_G_AUDIO, inp )
            #print( 'past ioctl get audio' )
        #fields = struct.unpack( fmt, data )
        #mode = ( int( fields[2] )& _V4L2_TUNER_SUB_STEREO )
        #print( 'stereo mode:{}'.format( int( mode ) ) )
        #return mode

    def get_signal_strength(self, calculate = False):
        """
        Returns the current signal strength as a value between 0 and 100.
        """
        # return 100.0*self.__tuner["signal"]/65535
        
        # algorithm adapted from fmscan by Russell Kroll
        time.sleep(_SIGNAL_LOCK_TIME)
        totsig = 0
        for i in range(_SIGNAL_TRIES):
            tuner = self.__get_tuner()
            signal = tuner["signal"]
            totsig += signal
            time.sleep(_SIGNAL_SAMPLE_SLEEP)
        #end for
        
        perc = totsig / float(0xffff * _SIGNAL_TRIES)
        
        return int( perc * 100 )
        

    def is_signal_good(self):
        """
        Returns whether the current signal strength is good enough.
        """
        
        return (self.get_signal_strength() > _SIGNAL_THRESHOLD)
        

    def scan(self, cb = None):
        """
        Scans for stations and returns a list of the frequencies of the
        stations found.
        If you pass a callback function, it will be called at every step.
        The signature of the callback must be: f(freq, is_station)
        """
        
        if (self.__is_scanning): return []
        
        stations = []
        low, high = self.get_frequency_range()
        self.__is_scanning = True
        for freq in range(low, high + 1, _SCAN_STEP_KHZ):
            self.__set_frequency(freq)
            is_good = self.is_signal_good()
            if (is_good): stations.append(freq)
            if (cb):
                try:
                    cb(freq, is_good)
                except:
                    pass
            if (not self.__is_scanning): break
        #end for
        self.__is_scanning = False
        
        return stations
        

    def __scan_next(self, scan_to, step, cb):
        """
        Scans for the next station.
        A station is recognized on the peak of signal strength
        (RISING -> FALLING) when the signal
        strength is high enough.
        """
    
        FALLING = 0
        RISING = 1       

        current = self.get_frequency()
        if (self.__is_scanning): return current
        
        prev_freq = current
        prev_strength = self.get_signal_strength()
        
        mode = FALLING
        self.__is_scanning = True
        for freq in range(current + step, scan_to, step):
            self.__set_frequency(freq)
            strength = self.get_signal_strength()
            
            if (prev_strength > strength):
                if (mode == RISING):
                    # found peak
                    if (prev_strength > _SIGNAL_THRESHOLD):
                        self.__set_frequency(prev_freq)
                        return freq
                    
                else:
                    mode = FALLING
            else:
                mode = RISING

            if (cb):
                try:
                    cb(freq)
                except:
                    pass
            #end if
                
            prev_freq = freq
            prev_strength = strength
            
            if (not self.__is_scanning): break
        #end for
        self.__is_scanning = False
        
        return current
        

    def scan_previous(self, cb = None):
        """
        Scans for the previous radio station and returns its frequency.
        If no station was found, the current frequency will be returned instead.
        """
        
        low, high = self.get_frequency_range()
        return self.__scan_next(low, -_SCAN_STEP_KHZ, cb)
        

    def scan_next(self, cb = None):
        """
        Scans for the next radio station and returns its frequency.
        If no station was found, the current frequency will be returned instead.        
        """
        
        low, high = self.get_frequency_range()
        return self.__scan_next(high, _SCAN_STEP_KHZ, cb)
        

    def cancel_scanning(self):
        """
        Cancels scanning for stations.
        """
        
        self.__is_scanning = False

    def refresh_rds( self ):
        self.rds.run_once()
