#!/usr/bin/python
# -*- coding: utf-8 -*-

# mmedia_list.py

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from media_track import MediaTrack

class MMediaListItem( MediaTrack ):
	def __init__( self, hash, text, is_enabled=True, is_playlist=False ):
		#print( 'created MMediaListItem hash:{}, text:{}'.format( hash, text ) )
		MediaTrack.__init__( self, hash, text )
		self.is_enabled = is_enabled
		self.is_playlist = is_playlist

class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	'''This is a class that autoresizes the listctrl so that the one and only column
	   that we use in MMediaList expands to the extent of the entire listctrl widget
	'''
	def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0 ):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		ListCtrlAutoWidthMixin.__init__(self)
		self.setResizeColumn(0)

class MMediaList:
	FILELIST = 0
	PLAYLIST = 1
	SYSTEM_PLAYLISTS = 2
	def __init__( self, parent_panel, settings, type=PLAYLIST, with_list_title=False, select_list_item_callback = None, click_list_item_callback = None, actions=[] ):
		self._panel = wx.Panel( parent_panel )
		parent_panel.GetSizer().Add( self._panel, 1, wx.EXPAND|wx.ALL, 15 )		
		sizer = wx.BoxSizer( wx.VERTICAL )
		self._panel.SetSizer( sizer )
		
		self.items = []
		self.settings = settings
		self.type = type
		self.with_list_title = with_list_title
		self._title_text = ''
		self.list_title = None
		self._select_list_item_callback = select_list_item_callback	#enter or doubleclick
		self._click_list_item_callback = click_list_item_callback	#single click
		
		self.itemListButtonsBackgroundColour = wx.Colour(0,0,0)
		self.itemListButtonsForegroundColour = wx.Colour(0,0,0)

		self.itemsFont = ( self.settings.FilelistFont if type==MMediaList.FILELIST else self.settings.PlaylistFont )		
		self.itemsColor = ( self.settings.FilelistFont.Color if type==MMediaList.FILELIST else self.settings.PlaylistFont.Color )
		self.itemsDisabledColor = ( self.settings.FilelistDisabledFontColor if type==MMediaList.FILELIST else self.settings.PlaylistDisabledFontColor )		
		self.itemlistPressColor = ( self.settings.FilelistPressColor if type==MMediaList.FILELIST else self.settings.PlaylistPressColor )
		self.itemlistBackgroundColour = ( self.settings.FilelistBackgroundColour if type==MMediaList.FILELIST else self.settings.PlaylistBackgroundColour )
		self.itemlistSelectedBackgroundColour = ( self.settings.FilelistSelectedBackgroundColour if type==MMediaList.FILELIST else self.settings.PlaylistSelectedBackgroundColour )
		self.itemlistSelectedForegroundColour = ( self.settings.FilelistSelectedForegroundColour if type==MMediaList.FILELIST else self.settings.PlaylistSelectedForegroundColour )

		if( with_list_title ):
			self.title_panel = wx.Panel( self._panel )
			self.title_panel.SetBackgroundColour( self.settings.PlaylistTitleBackgroundColour )
			title_panel_sizer = wx.BoxSizer( wx.VERTICAL )
			title_inner_sizer = wx.BoxSizer( wx.VERTICAL )#( wx.HORIZONTAL )
			self.title_panel.SetSizer( title_panel_sizer )

			self.list_title = wx.StaticText( self.title_panel, label = 'NEW' )
			self.list_title.SetFont( self.settings.PlaylistTitleFont.GetFont() )
			self.list_title.SetForegroundColour( self.settings.PlaylistTitleFont.Color )
			title_panel_sizer.Add( title_inner_sizer, 1, wx.EXPAND|wx.CENTRE, border = 5 )

			#title_inner_sizer.Add( (0,0),1,wx.EXPAND)
			title_inner_sizer.Add( self.list_title, 1, wx.ALIGN_LEFT|wx.ALL, border = 10 )	
			sizer.Add( self.title_panel, 0, wx.EXPAND|wx.BOTTOM, 5 )
		
		#filelists are multiselect and have select convenience buttons
		if( type == MMediaList.FILELIST ):
			select_panel = wx.Panel( self._panel )
			select_panel_sizer = wx.BoxSizer( wx.HORIZONTAL )
			select_panel.SetSizer( select_panel_sizer )
			
			select_all_button = wx.Button( select_panel, wx.ID_ANY, label = 'All' )
			unselect_all_button = wx.Button( select_panel, wx.ID_ANY, label = 'None' )
			select_inverse_button = wx.Button( select_panel, wx.ID_ANY, label = 'Inverse' )
			
			select_all_button.Bind( wx.EVT_BUTTON, self.SelectAll )
			unselect_all_button.Bind( wx.EVT_BUTTON, self.UnselectAll )
			select_inverse_button.Bind( wx.EVT_BUTTON, self.InvertSelected )
			
			select_panel_sizer.Add( select_all_button )
			select_panel_sizer.Add( unselect_all_button )
			select_panel_sizer.Add( select_inverse_button )
			
			sizer.Add( select_panel, 0, wx.EXPAND | wx.ALL, 2 )
		elif( type == MMediaList.PLAYLIST ):
			playlist_buttons_panel = wx.Panel( self._panel )
			playlist_buttons_panel_sizer = wx.BoxSizer( wx.HORIZONTAL )
			playlist_buttons_panel.SetSizer( playlist_buttons_panel_sizer )
			
			self.up_button = wx.Button( playlist_buttons_panel, wx.ID_ANY, label = 'up' )
			self.down_button = wx.Button( playlist_buttons_panel, wx.ID_ANY, label = 'Down' )
		
			self.up_button.Bind( wx.EVT_BUTTON, self.UpItem )
			self.down_button.Bind( wx.EVT_BUTTON, self.DownItem )
			
			playlist_buttons_panel_sizer.Add( self.up_button )
			playlist_buttons_panel_sizer.Add( self.down_button )
		
			sizer.Add( playlist_buttons_panel, 0, wx.EXPAND | wx.ALL, 2 )
						
		self.list = CustomListCtrl( self._panel, style=wx.LC_REPORT|wx.LC_NO_HEADER|( 0 if type==MMediaList.FILELIST else wx.LC_SINGLE_SEL ) |wx.LC_HRULES|wx.LC_VRULES)
		self.list.SetBackgroundColour( self.itemlistBackgroundColour )
		self.list.InsertColumn( 0, 'item')
		self.list.SetColumnWidth( -1, wx.LIST_AUTOSIZE )
		self.list.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.ItemSelected )	#enter or doubleclick
		
		self.filelist_selected_item_index = None
		self.list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ItemClicked )
		if( type == MMediaList.FILELIST ):
			self.filelist_selected_item_index = []	#will keep here the selected items, special handling			

		sizer.Add( self.list, 1, wx.EXPAND )
		
		if( actions ):
			self._action_buttons = {}
			self._actions_panel = self._BuildListActions( self._panel, actions )
			sizer.Add( self._actions_panel, 0, wx.EXPAND|wx.TOP, 5 )
		return
		
	def ShowReordering( self, show ):
		if( self.type != MMediaList.PLAYLIST ):
			return
			
		if( show ):
			self.up_button.Show()
			self.down_button.Show()
		else:
			self.up_button.Hide()
			self.down_button.Hide()
			
	def _GetSelectedItems( self ):
		selection = []
		# start at -1 to get the first selected item
		current = -1
		while True:
			next_sel_item = self.list.GetNextItem( current, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED )
			if next_sel_item == -1:
				return selection

			selection.append( next_sel_item )
			current = next_sel_item
			
	def UpItem( self, event ):
		items = self._GetSelectedItems()
		print( 'will move up {}'.format( items ) )
		new_indices = []
		for i in items:
			new_index = max( 0, i-1 )
			self.items.insert( new_index, self.items.pop( i ) )
			new_indices.append( new_index )
		self._BuildList()
		print( 'will select {}'.format( new_indices ) )
		self._SetSelectedState( new_indices )
		
	def DownItem( self, event ):
		items = self._GetSelectedItems()
		print( 'will move down {}'.format( items ) )
		new_indices = []
		for i in items:
			new_index = min( i+1, len( self.items ) - 1 )
			self.items.insert( new_index, self.items.pop( i ) )
			new_indices.append( new_index )
		self._BuildList()
		print( 'will select {}'.format( new_indices ) )
		self._SetSelectedState( new_indices )

	def _SetSelectedState( self, selected_item_indices ):
		self.list.Unbind( wx.EVT_LIST_ITEM_SELECTED )
		for i in range( len( self.items ) ):
			if( i in selected_item_indices ):
				print( 'selecting {}'.format( i ) )
				self.list.SetItemState( i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED )
				self.list.SetItemState( i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED )
			else:
				print( 'unselecting {}'.format( i ) )
				self.list.SetItemState( i, 0, wx.LIST_STATE_SELECTED )
		self.list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ItemClicked )

	def SelectAll( self, event ):
		self.filelist_selected_item_index = range( len( self.items ) )
		self._SetSelectedState( self.filelist_selected_item_index )
		
	def UnselectAll( self, event ):
		self.filelist_selected_item_index = []
		self._SetSelectedState( self.filelist_selected_item_index )
		
	def InvertSelected( self, event ):
		self.filelist_selected_item_index = [ i for i in range( len( self.items ) ) if i not in self.filelist_selected_item_index ]
		self._SetSelectedState( self.filelist_selected_item_index )
			
	def ItemClicked( self, event ):
		'''
		We will implement a special behaviour especially for multiselect filelists.
		If an item is clicked it will be selected. If it is clicked again it will be unselected.
		This was a tricky one. I had to unbind the EVT_LIST_ITEM_SELECTED handler or else each update
		was firing again the event.
		Also item removal i.e. deselection must happen explicitly
		'''
		item_index = event.GetIndex()
		if( self.filelist_selected_item_index is not None ):			
			if( item_index in self.filelist_selected_item_index ):
				#print( 'removing item {}'.format( item_index ) )
				self.filelist_selected_item_index.remove( item_index )
				self.list.SetItemState( item_index, 0, wx.LIST_STATE_SELECTED )		#unselect the removed item
			else:
				#print( 'adding item {}'.format( item_index ) )
				self.filelist_selected_item_index.append( item_index )
			#print( self.filelist_selected_item_index )
				
			self.list.Unbind( wx.EVT_LIST_ITEM_SELECTED )
			for i in self.filelist_selected_item_index:
				if( i != item_index ):
					self.list.SetItemState( i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED )
					self.list.SetItemState( i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED )	
			self.list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ItemClicked )
		elif( self._click_list_item_callback ):
			self._click_list_item_callback( self.items[item_index] )
					
	def ItemSelected( self, event ):
		#print( 'ItemSelected' )
		#print( 'responding to event select item index {}'.format( event.GetIndex() ) )
		#import pprint; pprint.pprint( dir( event ) )
		#for property, value in vars(event).iteritems():
			#print property, ": ", value

		#import pprint; pprint.pprint( event )
		#print( 'event type {}'.format( event.GetEventType() ) )
		item_index = event.GetIndex()
		#print( 'Before: {}'.format( self.filelist_selected_item_index ) )
		if( self.filelist_selected_item_index is not None ): #if this is a filelist i.e. multiselect clear other selections
			#I must unbind and then rebind EVT_LIST_ITEM_SELECTED or else a previously selected item will be deselected
			#by EVT_LIST_ITEM_SELECTED if clicked again
			self.list.Unbind( wx.EVT_LIST_ITEM_SELECTED )
			for i in self.filelist_selected_item_index:
				if( i != item_index ):
					print( 'deactivating {}'.format( i ) )
					self.list.SetItemState( i, 0, wx.LIST_STATE_SELECTED )	
			#print( 'initialising [] and activating with {}'.format( item_index ) )
			self.filelist_selected_item_index = [ item_index ]
			self.list.SetItemState( item_index, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED )
			self.list.SetItemState( item_index, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED )
			self.list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ItemClicked )
			#print( 'After: {}'.format( self.filelist_selected_item_index ) )
			
		if( self._select_list_item_callback ):
			#item = self.list.GetItem(event.GetIndex())
			item = self.items[item_index]
			#print( 'medialist calls back selected item.Hash {} ({})'.format( item.Hash(), item.Hash().__class__ ) )
			self._select_list_item_callback( self, item.Hash() )

	def ShowTitle( self, show ):
		if( self.title_panel ):
			if( show ):
				self.title_panel.Show()
			else:
				self.title_panel.Hide()
			self._panel.GetSizer().Layout()
		
	def SetTitle( self, title ):
		#print( 'SetTitle: {}'.format( title ) )
		self._title_text =  title
		try:
			self.list_title.SetLabel( self._title_text )
		except:
			pass
			
	def RefreshTitle( self ):
		try:
			self.list_title.SetLabel( self._title_text )
		except:
			pass
		
	def ClearTitle( self ):
		try:
			self._title_text = ''
			self.list_title.SetLabel( '' )
		except:
			pass
			
	def GetWidget( self ):
		return self._panel #self.list
		
	def SetItems( self, items ):
		#print( 'setting items...' )
		self.items = items
		#import pprint ; pprint.pprint( self.items )
		self._BuildList()
		
	def _CreateListItem( self, medialist_item, index ):
		item = wx.ListItem()
		item.SetText( medialist_item.Text() )
		if( self.type == MMediaList.FILELIST and medialist_item.is_playlist ):
			item.SetFont( self.settings.FilelistFileIsPlaylistFont.GetFont() )
			item.SetTextColour( self.settings.FilelistFileIsPlaylistFont.Color )
		else:
			item.SetFont( self.itemsFont.GetFont() )
			item.SetTextColour( ( self.itemsColor if medialist_item.is_enabled else self.itemsDisabledColor ) )
		if( index % 2 ):
			item.SetBackgroundColour( "white" )
		else:
			item.SetBackgroundColour( "grey" )
		return item
			
	def _BuildList( self ):
		self.list.DeleteAllItems()
		if( self._click_list_item_callback ):
			self._click_list_item_callback( None )	#in order to reset any media buttons or anything else related to selected playlist items, see 'subtitles' media_button
			
		if( self.items is None ):
			return
			
		itemsIndex = 0
		for i in reversed( self.items ):
			item = self._CreateListItem( i, itemsIndex )
			#item = wx.ListItem()
			#item.SetText( i.Text() )
			#if( self.type == MMediaList.FILELIST and i.is_playlist ):
				#item.SetFont( self.settings.FilelistFileIsPlaylistFont.GetFont() )
				#item.SetTextColour( self.settings.FilelistFileIsPlaylistFont.Color )
			#else:
				#item.SetFont( self.itemsFont.GetFont() )
				#item.SetTextColour( ( self.itemsColor if i.is_enabled else self.itemsDisabledColor ) )
			#if( itemsIndex % 2 ):
				#item.SetBackgroundColour( "white" )
			#else:
				#item.SetBackgroundColour( "grey" )
			itemsIndex += 1
			self.list.InsertItem( item )
			
	def _BuildListActions( self, panel, actions ):
		actions_panel = wx.Panel( panel )
		sizer = wx.BoxSizer( wx.HORIZONTAL )
		actions_panel.SetSizer( sizer )
		for action in actions:
			action_button = wx.Button( actions_panel, label=action )
			action_button.action = action #add this info for the EVT_BUTTON handler
			action_button.get_selected_item_hash_callback = self.GetSelectedItemHash
			#action_button.refresh_list_items_callback = self.SetItems
			#No event binding yet
			self._action_buttons[action] = action_button
			sizer.Add( action_button )
		return actions_panel
		
	def ShowAction( self, action ):
		self.ShowHideAction( self, action, True )
		
	def HideAction( self, action ):
		self.ShowHideAction( self, action, False )
		
	def ShowHideAction( self, action, show ):
		#print( 'Medialist will {} action {}'.format( ( 'show' if show else 'hide' ), action ) )
		#print( self._action_buttons.keys() )
		if( self._action_buttons.has_key( action ) ):
			if( show ):
				#print( 'Showing {}'.format( action ) )
				self._action_buttons[action].Show()
			else:
				#print( 'Hiding {}'.format( action ) )
				self._action_buttons[action].Hide()
		
	def BindActions( self, action_callbacks ):
		for action, callback in action_callbacks.iteritems():
			if( self._action_buttons.has_key( action ) ):
				#print( 'binding list button {} with action {}'.format( action, callback.__name__ ) )
				self._action_buttons[action].Bind( wx.EVT_BUTTON, callback )

	def GetSelectedItemHash( self ):
		i = self.list.GetFirstSelected()
		if( i == -1 ):
			return None
		
		#print( 'GetSelectedItemHash for item {}'.format( i ) )
		item = self.items[i]
		return item.Hash()
		
	def GetSelectedItems( self ):
		selected = []
		selected_indices = self._GetSelectedItems()
		#print( 'GetSelectedItems selected_indices: {}'.format( selected_indices ) )
		#for i in self.filelist_selected_item_index:
		for i in selected_indices:
			selected.append( self.items[i] )
		#print( 'GetSelectedItems returns: {}'.format( selected ) )
		return selected

	def ListSelectNext( self, forward ):
		if( len( self.items ) == 0 ):
			return

		nextItemIndex = 0
		itemIndex = self.ListFindSelectedIndex()
		print( 'ListFindSelectedIndex : {}'.format( itemIndex ) )
		if( itemIndex is not None ):
			if( forward ):
				nextItemIndex = ( itemIndex + 1 ) if ( itemIndex + 1 ) < len( self.items ) else 0
			else:
				nextItemIndex = ( itemIndex - 1 ) if ( itemIndex - 1 ) >= 0 else ( len( self.items ) - 1 )

		#print( 'Next {} itemIndex:{}'.format( 'next' if forward else 'previous', nextItemIndex ) )
		self.ListSelect( nextItemIndex )

	def ListFindSelectedIndex( self, state = wx.LIST_STATE_SELECTED):
		indices = []
		lastFound = -1
		while True:
			index = self.list.GetNextItem( lastFound, wx.LIST_NEXT_ALL, state	)
			if( index == -1 ):
				break
			else:
				lastFound = index
				indices.append( index )
		if( len( indices ) > 0 ):
			return indices[0]
		return None
		
	def ListSelect( self, item_index ):
		#print( 'will post event to activate item index {}'.format( item_index ) )
		cmd = wx.ListEvent( 10156, self.list.GetId() )
		cmd.m_itemIndex = item_index
		#print( 'will generate 10156 event:' )
		#for property, value in vars(cmd).iteritems():
			#print property, ": ", value
		wx.PostEvent( self.list, cmd )

	def SelectListTrack( self, track_hash ):
		#print( 'track_hash: {}'.format( track_hash ) )
		#for i in self.items:
			#print( 'list item {} -> {}'.format(  i.Hash(), i.Text() ) )
		item_to_select = [ i for i in self.items if i.Hash() == track_hash ]
		#import pprint, sys; pprint.pprint( item_to_select ) ; sys.exit()
		if( len( item_to_select ) == 0 ):
			print( 'track_hash {} not found in items'.format( track_hash ) )
			return
			
		index = self.items.index( item_to_select[0] )
		#print( 'track_hash {} found in items index {}'.format( track_hash, index ) )
		self.list.SetItemState( index, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED )
		self.list.SetItemState( index, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED )
		self.list.EnsureVisible( index )
		#self.list.SetItemState( index, wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED, wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED )

	#TODO: the rest of the functions should be reviewed and possibly deleted
	def ResetListButtons( self ):
		for i in self.itemButtons:
			i.SetBackgroundColour( self.itemListButtonsBackgroundColour )
			i.SetForegroundColour( self.itemListButtonsForegroundColour )
			i.selected = False
			i.Refresh()		
		
	def SelectListItem( self, event ):
		#print( 'SelectListItem' )
		button = event.GetEventObject()
		self.ListSelect( button )
		
	def ListScrollIntoView( self, button ):
		parentPosX, parentPosY = button.GetPosition()
		hx, hy = button.GetSizeTuple()
		overallPosY = ( button.index )* ( hy + 4 ) + 2
		clientSizeX, clientSizeY = self.scrollingListWindow.GetClientSize()

		rx, ry = self.scrollingListWindow.GetScrollPixelsPerUnit()
		unit = ry
		sx, sy = self.scrollingListWindow.GetViewStart()
		#~ magicNumber = 20		# Where did this value come from ?!
		sx = sx * rx #magicNumber
		sy = sy * ry #magicNumber

		#~ print( 'overallPosY:{}, parentPosY:{}, hy:{}, sy:{}, clientSizeY:{} '.format( 
			#~ overallPosY, parentPosY , hy, sy, clientSizeY ) )
		scrollPosY = overallPosY #parentPosY
		
		if( overallPosY + hy < clientSizeY ):
			#~ print( 'will scroll to the top' )
			self.scrollingListWindow.Scroll( 0, 0 )
		else:	
			if (parentPosY < 0 ): #sy ) :
				if( overallPosY + hy > clientSizeY ):
					#~ print( 'overallPosY + hy > clientSizeY' )
					scrollPosY = overallPosY - clientSizeY + 1.5*hy
				#~ print( 'parentPosY < sy Scroll( {}, {} )'.format( 0, scrollPosY/unit ) )
				self.scrollingListWindow.Scroll( 0, scrollPosY/unit )

		if ( parentPosX < sx ) :
			#~ print( 'parentPosX < sx Scroll( {}, {} )'.format( 0, -1 ) )
			self.scrollingListWindow.Scroll( 0, -1 )

		if (parentPosX + sx) > clientSizeX  :
			#~ print( '(parentPosX + sx) > clientSizeX Scroll( {}, {} )'.format( 0, -1 ) )
			self.scrollingListWindow.Scroll( 0, -1 )

		if (parentPosY + hy ) > clientSizeY : # - sy) > clientSizeY :
			#~ print( '(parentPosY + hy - sy) > clientSizeY Scroll( {}, {} )'.format( 0, scrollPosY/unit ) )
			self.scrollingListWindow.Scroll( 0, scrollPosY/unit )
