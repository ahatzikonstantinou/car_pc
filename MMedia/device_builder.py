#!/usr/bin/python
# -*- coding: utf-8 -*-

#device_builder

import wx
import subprocess
import logging

from filesystem_device import *
from media_device import *
from fm_radio import *
from tv import *
from usb import *
from mount_detector import *
from audiocd_device import *
from dvd_device import *
from upnp.upnp_provider import *
from upnp.upnp_mediaserver_device import *
from upnp.upnp_mediarenderer_device import *
from samba import *
from a2dp import *

__all__ = [ 'DeviceBuilder', 'EVT_DEVICE_ADD', 'EVT_DEVICE_DELETE' ]

class DeviceBuilder:
	MOUNT_DIR = '/media'
	
	def __init__( self, dev_media_functions, mmedia_gui, error_reporter, message_reporter, publisher_text_display_message_name, GetSelectedListFilesCallback, SetPlaylistLabelTextCallback, GetSelectedPlaylistItemsCallback, GetSelectedSystemPlaylistItemsCallback, playerLock, a2dp_provider ):#, DeviceAddedCallback, DeviceRemovedCallback ):
		self._dev_media_functions = dev_media_functions
		self._mmedia_gui = mmedia_gui
		self._error_reporter = error_reporter
		self._message_reporter = message_reporter
		self._publisher_text_display_message_name = publisher_text_display_message_name
		self._GetSelectedListFilesCallback = GetSelectedListFilesCallback
		self._SetPlaylistLabelTextCallback = SetPlaylistLabelTextCallback
		self._GetSelectedPlaylistItemsCallback = GetSelectedPlaylistItemsCallback
		self._GetSelectedSystemPlaylistItemsCallback = GetSelectedSystemPlaylistItemsCallback
		self._playerLock = playerLock
		self.a2dp_provider = a2dp_provider
		self.a2dp_provider.AddSourceAddedObserver( self )
		self.a2dp_provider.AddSourceRemovedObserver( self )
		#self._DeviceAddedCallback = DeviceAddedCallback
		#self._DeviceRemovedCallback = DeviceRemovedCallback
		
		#self.usb_detector = usb_detect.USBDetector( DeviceBuilder.MOUNT_DIR, self._FilesystemMounted, self._FilesystemUnmounted )
		thread = MountDetectorThread( self._mmedia_gui, self )
		thread = UPnPDetectorThread( self._mmedia_gui, self )
		
	def Build( self, abstract_device ):
		if( abstract_device.dev_type == MediaDevice.TYPE_TV_TUNER ):
			return self.TV( abstract_device )
		elif( abstract_device.dev_type == MediaDevice.TYPE_FM_RADIO ):
			return self.FMRadio( abstract_device )
		elif( abstract_device.dev_type == MediaDevice.TYPE_USB ):
			#return self.Usb( abstract_device )
			raise Exception( 'Usb devices must be autodetected in order to be properly included in the MMedia application. If there is a usb device added in devices_list.csv please remove it!' )
		elif( abstract_device.dev_type == MediaDevice.TYPE_INTERNAL_HARD_DISK ):
			return self.InternalHardDisk( abstract_device )
		elif( abstract_device.dev_type == MediaDevice.TYPE_EXTERNAL_HARD_DISK ):
			return self.ExternalHardDisk( abstract_device )
		elif( abstract_device.dev_type == MediaDevice.TYPE_DVD ):
			return self.Dvd( abstract_device )
		elif( abstract_device.dev_type == MediaDevice.TYPE_UPNP_MEDIARENDERER ):
			return self.UPnPMediaRenderer( abstract_device )
		
		return abstract_device #return the abstract device for unkown types

	def UPnPMediaRenderer( self, abstract_device ):
		return UPnPMediaRendererDevice( abstract_device )
		
	def TV( self, abstract_device ):
		return TV( abstract_device )
		
	def FMRadio( self, abstract_device	):
		return Radio( abstract_device, CarPC_RDSDecoderListener( self._publisher_text_display_message_name ) )
		
	def DVDFromMount( self, gio_mount ):
		return DVDDevice(
			root_dir = gio_mount.get_root().get_path(), 
			abstract_device = MediaDevice( 
				name = gio_mount.get_name(),
				dev_path = gio_mount.get_root().get_path(),
				dev_type = MediaDevice.TYPE_DVD,
				mmedia_gui = self._mmedia_gui, 
				gui_media_functions = self._dev_media_functions, 
				error_reporter = self._error_reporter,
				message_reporter = self._message_reporter,
				GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
				playerLock = self._playerLock
			),
			gio_mount = gio_mount,
			GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
			SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
			GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
		)
		
	def AudioCdFromMount( self, gio_mount ):
		return AudioCDDevice(
			root_dir = gio_mount.get_root().get_path(), 
			abstract_device = MediaDevice( 
				name = gio_mount.get_name(),
				dev_path = gio_mount.get_root().get_path(),
				dev_type = MediaDevice.TYPE_AUDIOCD,
				mmedia_gui = self._mmedia_gui, 
				gui_media_functions = self._dev_media_functions, 
				error_reporter = self._error_reporter,
				message_reporter = self._message_reporter,
				GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
				playerLock = self._playerLock
			),
			gio_mount = gio_mount,
			GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
			SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
			GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
		)
		
	#def UsbFromUSBDisk( self, usb_disk ):
		#return usb_device.USBDevice( 
						#uuid = DeviceBuilder.GetUUID( usb_disk.mount_path ),
						#root_dir = usb_disk.mount_path,
						#abstract_device = MediaDevice( 
							#name = usb_disk.label,
							#dev_path = usb_disk.mount_path,
							#dev_type = MediaDevice.TYPE_USB,
							#mmedia_gui = self._mmedia_gui, 
							#gui_media_functions = self._dev_media_functions, 
							#error_reporter = self._error_reporter,
							#message_reporter = self._message_reporter,
							#GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
							#playerLock = self._playerLock
						#),
						#GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
						#SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
						#GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
					#)
					
	def UsbFromMount( self, gio_mount ):
		mount_path = gio_mount.get_root().get_path()
		return usb_device.USBDevice( 
						gio_mount = gio_mount,
						uuid = DeviceBuilder.GetUUID( mount_path ),
						root_dir = mount_path,
						abstract_device = MediaDevice( 
							name = gio_mount.get_name(), #os.path.basename( mount_path ),
							dev_path = mount_path,
							dev_type = MediaDevice.TYPE_USB,
							mmedia_gui = self._mmedia_gui, 
							gui_media_functions = self._dev_media_functions, 
							error_reporter = self._error_reporter,
							message_reporter = self._message_reporter,
							GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
							playerLock = self._playerLock
						),
						GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
						SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
						GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
					)
					
	def SambaFromMount( self, gio_mount ):
		return samba_device.SambaDevice( 
						root_dir = gio_mount.get_root().get_path(),
						gio_mount = gio_mount,
						abstract_device = MediaDevice( 
							name = gio_mount.get_name(), #os.path.basename( gio_mount.get_root().get_path() ),
							dev_path = gio_mount.get_root().get_path(),
							dev_type = MediaDevice.TYPE_SAMBA_SHARE,
							mmedia_gui = self._mmedia_gui, 
							gui_media_functions = self._dev_media_functions, 
							error_reporter = self._error_reporter,
							message_reporter = self._message_reporter,
							GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
							playerLock = self._playerLock
						),
						GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
						SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
						GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
					)
					
	#def Usb( self, abstract_device ):
		#return usb_device.USBDevice( 
						#uuid = DeviceBuilder.GetUUID( abstract_device.dev_path ),
						#root = abstract_device.dev_path,
						#abstract_device = abstract_device,
						#GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
						#SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
						#GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
						#)					
		
	def InternalHardDisk( self, abstract_device	):
		return Filesystem( abstract_device, GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
			SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
			GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback )
		
	def ExternalHardDisk( self, abstract_device	):
		return Filesystem( abstract_device, GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
			SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
			GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback )
		
	def Dvd( self, abstract_device	):
		return Dvd()

	def GetDeviceFromMount( self, gio_mount ):
		#import pprint; pprint.pprint( gio_mount ) ; pprint.pprint( gio_mount.guess_content_type_sync( True ) )
		dev = None
		content_type_list = gio_mount.guess_content_type_sync( 0 )
		#if( gio_mount.get_root().get_uri().startswith( 'smb://' ) ):
		if( gio_mount.get_root().has_uri_scheme( 'smb' ) ):
			print( 'this is a samba mount' )
			dev = self.SambaFromMount( gio_mount )
		elif( content_type_list is None ):
			print( 'this is a filesystem mount' )
			dev = self.UsbFromMount( gio_mount )
		elif( 'x-content/audio-cdda' in content_type_list ):
			print( 'this is an audio cd' )
			dev = self.AudioCdFromMount( gio_mount )
		elif( 'x-content/video-dvd' in content_type_list ):
			print( 'this is a dvd' )
			dev = self.DVDFromMount( gio_mount )
		else:
			print( 'this is a filesystem mount' )
			dev = self.UsbFromMount( gio_mount )
		logging.debug( 'uri: {}'.format( gio_mount.get_root().get_uri() ) )
		return dev
				
	@staticmethod
	def _GetDevSystemPath( device_path ):
		cmd = 'cat /proc/mounts | grep "{}" | cut -d " " -f 1'.format( device_path )
		lines = subprocess.check_output( cmd, shell=True ).strip().split( ' ' )
		#import pprint; pprint.pprint( lines )
		return lines[0].strip()
	
	@staticmethod	
	def GetUUID( device_path ):
		uuid = os.path.basename( device_path )	#default for the cases where no UUID exists e.g. cdrom
		try:
			system_path = DeviceBuilder._GetDevSystemPath( device_path )
			cmd = 'ls -l /dev/disk/by-uuid/ | tr -s " " | cut -d " " -f 9,11 | tail -n +2 | grep "{}"'.format( os.path.basename( system_path ) )
			#print( 'cmd: {}'.format( cmd ) )
			lines = subprocess.check_output( cmd, shell=True ).strip().split( ' ' )
			#import pprint; pprint.pprint( lines )
			uuid = lines[0].strip()
			#print( 'uuid: {}, path: {}'.format( uuid, device_path ) )
		except:			
			pass
		return uuid
		
	def BuildUPnPMediaServerDevice( self, hostInfo, upnp_device_name, upnp_provider ):
		return UPnPMediaServerDevice(
			upnp_hostInfo = hostInfo,
			upnp_device_name = upnp_device_name,
			upnp_provider = upnp_provider,
			abstract_device = MediaDevice( 
				name = hostInfo['deviceList'][upnp_device_name]['friendlyName'], #upnp_device_name,
				dev_path = hostInfo['name'],
				dev_type = MediaDevice.TYPE_UPNP_MEDIASERVER,
				mmedia_gui = self._mmedia_gui, 
				gui_media_functions = self._dev_media_functions, 
				error_reporter = self._error_reporter,
				message_reporter = self._message_reporter,
				GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
				playerLock = self._playerLock
			),
			GetSelectedListFilesCallback = self._GetSelectedListFilesCallback,
			SetPlaylistLabelTextCallback = self._SetPlaylistLabelTextCallback,
			GetSelectedPlaylistItemsCallback = self._GetSelectedPlaylistItemsCallback
		)
		
	def GetA2DPDevices( self ):
		a2dp_devices = []
		for a2dp_sources in self.a2dp_provider.GetAllSources():
			a2dp_devices.append( self.BuildA2DPDevice( a2dp_sources ) )
		return a2dp_devices
		
	def A2DPSourceAdded( self, a2dp_source ):
		dev = self.BuildA2DPDevice( a2dp_source )
		wx.PostEvent( self._mmedia_gui, DeviceAddEvent( device = dev ) )
				
	def BuildA2DPDevice( self, a2dp_source ):
		dev = A2DPDevice( 
			a2dp_source = a2dp_source,
			abstract_device = MediaDevice( 
				name = a2dp_source.name,
				dev_path = a2dp_source.Hash(),
				dev_type = MediaDevice.TYPE_A2DP_BLUETOOTH_SOURCE,
				mmedia_gui = self._mmedia_gui, 
				gui_media_functions = self._dev_media_functions, 
				error_reporter = self._error_reporter,
				message_reporter = self._message_reporter,
				GetSelectedSystemPlaylistItemsCallback = self._GetSelectedSystemPlaylistItemsCallback,
				playerLock = self._playerLock
			)
		)
		return dev
		
	def A2DPSourceRemoved( self, a2dp_source_hash ):
		wx.PostEvent( self._mmedia_gui, DeviceDeleteEvent( device_path = a2dp_source_hash ) )
		
# Define notification events
EVT_DEVICE_ADD_ID = wx.NewId()
EVT_DEVICE_DELETE_ID = wx.NewId()

def EVT_DEVICE_ADD(win, func):
	"""Define Device Add Event."""
	win.Connect(-1, -1, EVT_DEVICE_ADD_ID, func)

def EVT_DEVICE_DELETE(win, func):
	"""Define Device Delete Event."""
	win.Connect(-1, -1, EVT_DEVICE_DELETE_ID, func)
	
class DeviceAddEvent(wx.PyEvent):
	"""Simple event to carry arbitrary result data."""
	def __init__(self, device):
		"""Init Complete Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_DEVICE_ADD_ID)
		self.device = device #usb_device.USBDevice

class DeviceDeleteEvent( wx.PyEvent ):
	def __init__( self, device_path = None, device_name = None ):
		"""Init Device Delete Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_DEVICE_DELETE_ID)
		self.device_path = device_path
		self.device_name = device_name
			
class MountDetectorThread( Thread ):
	def __init__( self, notify_window, device_builder ): #watch_path,  ):
		Thread.__init__(self)
		self.notify_window = notify_window
		#self.watch_path = watch_path
		self._device_builder = device_builder
		
		self.setDaemon(1)
		self.start()
		
	def run( self ):
		#detector = usb_detect.USBDetector( self.watch_path, self._FilesystemMounted, self._FilesystemUnmounted )
		detector = MountDetector( self._FilesystemMounted, self._FilesystemUnmounted )
	
	def _FilesystemMounted( self, mount ):
		if( MountDetector.IsAudioCd( mount ) and mount.can_eject() == False ):
			print( 'will ignore {} because it cannot eject'.format( mount.get_root().get_path() ) )
			return
		mount_path = mount.get_root().get_path()
		print( 'just built and will add device path: {}, name: {}'.format( mount_path, os.path.basename( mount_path ) ) )
		try:
			dev = self._device_builder.GetDeviceFromMount( mount )
			#There is a strange bug here. My MountDetector detects two mounts for each audio cd loaded in the computer.
			#They are exactly the same except for the fact that the first audiocd mount cannot be ejected while the second
			#one can. So ignore any audiocd mounts that cannot eject
			wx.PostEvent( self.notify_window, DeviceAddEvent( device = dev ) )
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
	def _FilesystemUnmounted( self, mount ):
		dev_path = mount.get_root().get_path()
		print( 'device at path {} was unmounted'.format( dev_path ) )
		try:
			wx.PostEvent( 
				self.notify_window, 
				DeviceDeleteEvent( 
					device_path = dev_path, 
					device_name = mount.get_name() 
				) 
			)
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
class UPnPDetectorThread( Thread ):
	def __init__( self, notify_window, device_builder ):
		Thread.__init__(self)
		self.notify_window = notify_window
		self._device_builder = device_builder
		self._upnp_provider = UPnPProvider()
		self.setDaemon(1)
		self.start()
		
	def run( self ):
		self._upnp_provider.AddDeviceAddedObserver( 'MediaServer', self.MediaServerAdded )
		self._upnp_provider.AddDeviceRemovedObserver( 'MediaServer', self.MediaServerRemoved )
		self._upnp_provider.Start()
	
	def MediaServerAdded( self, upnp_proxy, hostInfo, device_name ):
		print( 'will build and add device path: {}, name: {}'.format( hostInfo['name'],device_name ) )
		try:
			dev = self._device_builder.BuildUPnPMediaServerDevice( hostInfo, device_name, self._upnp_provider )
			wx.PostEvent( self.notify_window, DeviceAddEvent( device = dev ) )
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
	def MediaServerRemoved( self, hostname, device_name ):
		print( 'device at path {} was unmounted'.format( hostname ) )
		try:
			wx.PostEvent( self.notify_window, DeviceDeleteEvent( device_path = hostname ) )
		except:
			import sys; print('Error: %s' % sys.exc_info()[1])
		
class TestDeviceBuilder( DeviceBuilder ):
	def __init__( self, publisher_text_display_message_name ):
		DeviceBuilder.__init__( self, publisher_text_display_message_name )
		pass
		
	def Build( self, abstract_device ):
		return Radio( abstract_device, CarPC_RDSDecoderListener( self._publisher_text_display_message_name ) ) #abstract_device


if __name__ == '__main__':
	DeviceBuilder._GetUUID( '/media/KINGSTON' )
	
	db = DeviceBuilder( None, None,None, None,None, None )
	db._FilesystemMounted( '/media/KINGSTON' )
