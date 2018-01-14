#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class SpeedDialPopup():
	def __init__( self, gui_parent, parent_panel, menu_item_height ):
		self._gui_parent = gui_parent
		self._parent_panel = parent_panel
		self._menu_item_height = menu_item_height
		self._current_event_speeddial_button = None
		#self.popupmenu = wx.Menu()
		#
		#for text in "one two three four five".split():
			#item = self.popupmenu.Append(-1, text)
			#self._gui_parent.Bind( wx.EVT_MENU, self.OnPopupItemSelected, item )
		#p.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

	def GetWidget( self ):
		return self.popupmenu
		
	def OnShowPopup(self, event):
		self._current_event_speeddial_button = event.GetEventObject()
		items = self._GetSpeedDialPopupitems( self._current_event_speeddial_button )
		if( len( items ) == 0 ):
			return
			
		self.popupmenu = wx.Menu()
		count = 0
		for item in items:
			item = self.popupmenu.AppendItem( item )
			item.SetBackgroundColour( ( 'white' if ( count % 2 ) else 'grey' ) )
			self._gui_parent.Bind( wx.EVT_MENU, self.OnPopupItemSelected, item )
			count += 1
		pos = event.GetPosition()
		print( 'event pos: {}'.format( pos ) )
		#pos = self._gui_parent.ScreenToClient(pos)
		#pos = event.GetEventObject().ClientToScreen(pos)
		#pos = self._parent_panel.ClientToScreen(pos)
		print( 'popup pos: {}'.format( pos ) )
		height = self.popupmenu.GetMenuItemCount() * self._menu_item_height
		pos = ( pos.x, pos.y - height )
		event.GetEventObject().PopupMenu(self.popupmenu, pos)

	def OnPopupItemSelected(self, event):
		item_id = event.GetId()
		item = self.popupmenu.FindItemById( item_id )
		text = item.GetText()
		wx.MessageBox("You selected item '%s'" % text)
		
		if( 0 == item_id ):
			self._StoreCurrentTrack()
		elif( 1 == item_id ):
			self._StoreCurrentDirectory()
		elif( 2 == item_id ):
			self._StoreCurrentPlaylist()
		elif( 3 == item_id ):
			self._ClearSpeedDialButton()
		else:
			raise Exception( 'Unknown item id {} in speeddial popup'.format( item_id ) )
		self._current_event_speeddial_button = None	#reset it
		
	def _StoreCurrentTrack( self ):
		self._gui_parent.SetSpeedDialTrack( self._current_event_speeddial_button )
		
	def _StoreCurrentDirectory( self ):
		self._gui_parent.SetSpeedDialDirectory( self._current_event_speeddial_button )
		
	def _StoreCurrentPlaylist( self ):
		self._gui_parent.SetSpeedDialPlaylist( self._current_event_speeddial_button )
		
	def _ClearSpeedDialButton( self ):
		self._gui_parent.ClearSpeedDialButton( self._current_event_speeddial_button )
	
	def _GetSpeedDialPopupitems( self, speeddial_button ):
		popup_items = []
		current_device = self._gui_parent._current_device
		if( not current_device ):
			return []
			
		track_hash = current_device.CurrentTrackHash()
		if( track_hash ):
			popup_items.append( wx.MenuItem( id = 0, text = 'Store track' ) )
			
		if( current_device.SupportsCapability( 'filesystem' ) ):
			directory_hash = current_device.GetCurrentDirectoryHash()
			#if this is a filesystem and the user has double clicked on a directory to cd into it
			#the current directory is also the current track. So only show the 'sore directory' option
			if( directory_hash == track_hash ):
				popup_items = []
			popup_items.append( wx.MenuItem( id = 1, text = 'Store directory' ) )
			
		if( current_device.GetCurrentPlaylistHash() ):
			popup_items.append( wx.MenuItem( id = 2, text = 'Store playlist' ) )
			
		button_index = speeddial_button.GetLabel()
		if( current_device.SupportsCapability( 'clear_speeddial_button' ) ): #and 
			#current_device.state.speed_dials.has_key( button_index ) 	
		#):
			popup_items.append( wx.MenuItem( id = 3, text = 'Clear' ) )
		
		return popup_items
