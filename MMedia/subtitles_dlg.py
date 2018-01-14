#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import logging
logging.basicConfig( level = logging.DEBUG )

from custom_controls import *

class SelectSubtitlesDlg( wx.Dialog ):
	def __init__( self, parent, title, current_subtitle = '', size=(650, 250) ):
		wx.Dialog.__init__( self, parent = parent, title = title, size = size )

		self.current_subtitle = current_subtitle
		self.subtitles = []
		
		self.panel = wx.Panel(self)
		self.vbox = wx.BoxSizer( wx.VERTICAL )
		
		current_subtitle_LBL = wx.StaticText( self.panel, wx.ID_ANY, label = 'Current subtitle:' )
		current_subtitle_TXT = wx.StaticText( self.panel, wx.ID_ANY, label = self.current_subtitle )
		self.show_CHK = wx.CheckBox( self.panel, wx.ID_ANY, 'Show subtitles' )
		if( len( self.current_subtitle ) > 0 ):
			self.show_CHK.SetValue( True )
		
		self.subtitle_list = CustomListCtrl( self.panel, style = wx.LC_REPORT  | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES )
		self.subtitle_list.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.OnSubtitleSelected )	#enter or doubleclick
		self.subtitle_list.InsertColumn( 0, 'Directory listing:')
		self.subtitle_list.SetColumnWidth( -1, wx.LIST_AUTOSIZE )
		
		okButton = wx.Button( self.panel, wx.ID_OK, '')
		okButton.Bind(wx.EVT_BUTTON, self.OnOk)
		closeButton = wx.Button( self.panel, wx.ID_CANCEL, '')
		closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
		
		self.hbox_current_sub = wx.BoxSizer( wx.HORIZONTAL )
		self.hbox_buttons = wx.StdDialogButtonSizer() #wx.BoxSizer(wx.HORIZONTAL)
		
		self.hbox_current_sub.Add( current_subtitle_LBL, 0 )
		self.hbox_current_sub.Add( current_subtitle_TXT, 0,wx.LEFT, 5 )
		
		self.hbox_buttons.AddButton(okButton)
		self.hbox_buttons.AddButton(closeButton) #, flag=wx.LEFT, border=5)
		self.hbox_buttons.SetAffirmativeButton(okButton)
		self.hbox_buttons.SetCancelButton(closeButton)
		self.hbox_buttons.Realize()
		
		self.vbox.Add( self.hbox_current_sub )
		self.vbox.Add( self.show_CHK )
		self.vbox.Add( self.subtitle_list, 1, wx.EXPAND )
		self.vbox.Add( self.hbox_buttons, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10 )
		
		self.panel.SetSizer( self.vbox )
		
	def OnOk( self,e ):
		self.EndModal(e.GetId())
			
	def OnClose(self, e):
		self.Destroy()
		
	def _GetFiles( self ):
		'''
		Concrete classes of this class may override this to refresh or fill in self.subtitles
		'''
		logging.debug( 'returning {}'.format( self.subtitles ) )
		return self.subtitles
		
	def FillList( self ):
		self.subtitle_list.DeleteAllItems()
		logging.debug( 'Cleared subtitle_list' )
		self._GetFiles()
		index = 0
		for f in reversed( self.subtitles ):
			item = wx.ListItem()
			item.SetText( f )
			if( index % 2 ):
				item.SetBackgroundColour( "white" )
			else:
				item.SetBackgroundColour( "grey" )
			self.subtitle_list.InsertItem( item )
			index += 1
	
	def OnSubtitleSelected( self, event ):
		'''
		Concrete classes of this class should implement this
		'''
		pass
			
	def GetSelectedSubtitle( self ):
		index = self.subtitle_list.GetFirstSelected()
		if( -1 == index ):
			return None
			
		subtitle = self.subtitles[ index ]
		return subtitle
		
	def ShowSubtitles( self ):
		return self.show_CHK.GetValue()
		
class SubtitlesDlg:
	'''
	Abstract class for subtitles dialog. Three kinds of such dialogs exist. 
	1) A file based subtitles dialog
	2) The dialog for subtitles included in dvds
	3) The dialog for subtitles included in the xml returned when browsing UPnP(DLNA) media servers
	'''
	def __init__( self, parent, SelectedSubtitlesCallback, current_subtitle ):
		self.parent = parent
		self.SelectedSubtitlesCallback = SelectedSubtitlesCallback
		self.current_subtitle = current_subtitle
		logging.debug( 'self.current_subtitle: {}'.format( self.current_subtitle ) )
		
	def _GetDialog( self ):
		'''
		Concrete classes must implement this function
		'''
		raise Exception( 'No concrete implementation of _GetDialog' )
		
	def ShowDialog( self ):
		dlg = self._GetDialog()
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetSelectedSubtitle()
			logging.debug( "You chose the following file:" )
			self.SelectedSubtitlesCallback( ok = True, show_subtitles = dlg.ShowSubtitles(), subtitle = path )
		else:
			self.SelectedSubtitlesCallback( ok = False, show_subtitles = dlg.ShowSubtitles(), subtitle = None )
		dlg.Destroy()
		
class FileSubtitlesDlg( SubtitlesDlg ):
	def __init__( self, parent, SelectedSubtitlesCallback, root_dir, directory, current_subtitle = '' ):
		SubtitlesDlg.__init__( self, parent, SelectedSubtitlesCallback, current_subtitle )
		self.root_dir = root_dir
		self.directory = directory
	
	def _GetDialog( self ):
		#wildcard = 'Subtitle files|*.aqt;*.cvd;*.dks;*.jss;*.sub;*.ttxt;*.mpl;*.txt;*.pjs;*.psb;*.rt;*.smi;*.srt;*.ssa;*.svcd;*.usf;*.idx | All files (*.*)|*.*'
		class Dlg( SelectSubtitlesDlg ):
			SUBTITLE_FILES_FILTER = ['Subtitle files', [ 'aqt', 'cvd', 'dks', 'jss', 'sub', 'ttxt', 'mpl', 'txt', 'pjs', 'psb', 'rt', 'smi', 'srt', 'ssa', 'svcd', 'usf', 'idx'] ]
			ALL_FILES_FILTER = ['All files', []]
			def __init__( self, parent, title, root_dir, current_directory, current_subtitle = '', size=(650, 250) ):
				SelectSubtitlesDlg.__init__( self, parent = parent, title = title, current_subtitle = current_subtitle, size = size )

				self.root_dir = root_dir
				self.current_directory = current_directory
				self.current_subtitle = current_subtitle
				self.current_file_filter = Dlg.SUBTITLE_FILES_FILTER[1]
				
				directory_label = wx.StaticText( self.panel, label = 'Current directory:' )
				self.directory_TXT = wx.StaticText( self.panel, label = self.current_directory )
				
				filter_label = wx.StaticText( self.panel, label = 'File filter:' )
				self.sub_filter_RAD = wx.RadioButton( self.panel, wx.ID_ANY, "Subtitle files", style = wx.RB_GROUP )
				self.sub_filter_RAD.SetValue( True )
				self.sub_filter_RAD.Bind( wx.EVT_RADIOBUTTON, self.OnFilterButton )
				self.all_filter_RAD = wx.RadioButton( self.panel, wx.ID_ANY, "All files" )
				self.all_filter_RAD.Bind( wx.EVT_RADIOBUTTON, self.OnFilterButton )
				
				self.dir_up_BTN = wx.Button( self.panel, label='Dir Up' )
				self.dir_up_BTN.Bind( wx.EVT_BUTTON, self.OnDirUp )
				
				hbox_dir = wx.BoxSizer( wx.HORIZONTAL )
				hbox_filter = wx.BoxSizer( wx.HORIZONTAL )
				
				hbox_dir.Add( directory_label, 0 )
				hbox_dir.Add( self.directory_TXT, 1, wx.LEFT, 5 )
				
				hbox_filter.Add( filter_label, 0 )
				hbox_filter.Add( self.sub_filter_RAD, 1, wx.LEFT, 5 )
				hbox_filter.Add( self.all_filter_RAD, 1, wx.LEFT, 5 )
				
				self.hbox_buttons.Insert( 1, self.dir_up_BTN )
				
				self.vbox.Insert( 2, hbox_dir )
				self.vbox.Insert( 3, hbox_filter )
				
				self.SetDirectory( self.current_directory )
				self.vbox.Layout()
				
			def EnableDirUpButton( self ):
				if( self.current_directory == self.root_dir ):
					self.dir_up_BTN.Disable()
				else:
					self.dir_up_BTN.Enable()
				
			def _GetFiles( self ):
				items = os.listdir( os.path.abspath( self.current_directory ) )
				dirs = [ '{}/'.format( i ) for i in items if os.path.isdir( os.path.abspath( os.path.join( self.current_directory, i ) ) ) ]
				files = [ i for i in items if os.path.isfile( os.path.abspath( os.path.join( self.current_directory, i ) ) ) ]
				logging.debug( 'Got {} dirs and {} files in {}'.format( len( dirs ), len( files ), os.path.abspath( self.current_directory ) ) )
				self.subtitles = sorted( dirs )
				if( len( self.current_file_filter ) == 0 ):
					logging.debug( 'No filter.' )
					self.subtitles += sorted( files )
					return
				#logging.debug( 'File filter: {}'.format( self.current_file_filter ) )
				for i in files:
					ext = os.path.splitext( i )[1][1:]
					#logging.debug( 'Checking {} (of {}) against filters: {}'.format( ext, i, self.current_file_filter ) )
					if( ext in self.current_file_filter ):
						self.subtitles.append( i )
				logging.debug( 'Filtered {} dirs and files'.format( len( self.subtitles ) ) )
				
			def OnFilterButton( self, event ):
				if( event.GetEventObject() == self.sub_filter_RAD ):
					self.current_file_filter = Dlg.SUBTITLE_FILES_FILTER[1]
				else:
					self.current_file_filter = Dlg.ALL_FILES_FILTER[1]
				self.FillList()
				
			def SetDirectory( self, directory ):
				self.current_directory = directory
				self.directory_TXT.SetLabel( self.current_directory )
				self.EnableDirUpButton()
				self.FillList()
				
			def OnSubtitleSelected( self, event ):
				#print( dir( event ) )
				file_item = self.subtitles[ event.GetIndex() ]
				full_path = os.path.join( self.current_directory, file_item )
				logging.debug( 'selected {}'.format( full_path ) )
				if( os.path.isdir( full_path ) ):
					logging.debug( '\twhich is a directory' )
					self.SetDirectory( full_path )
					
			def OnDirUp( self, event ):
				parent_dir = os.path.abspath( os.path.join( self.current_directory, os.path.pardir) )
				if( parent_dir != self.current_directory and self.current_directory != self.root_dir ):
					self.SetDirectory( parent_dir )
				
			def GetSelectedSubtitle( self ):
				subtitle = SelectSubtitlesDlg.GetSelectedSubtitle( self )
				if( subtitle is not None ):
					subtitle = os.path.join( self.current_directory, subtitle )
				return subtitle
				
		return Dlg( self.parent, 'Choose subtitle file', self.root_dir, self.directory, self.current_subtitle )
		
class DVDSubtitlesDlg( SubtitlesDlg ):
	def __init__( self, parent, SelectedSubtitlesCallback, media_player_subs_list, current_subtitle = '' ):
		SubtitlesDlg.__init__( self, parent, SelectedSubtitlesCallback, current_subtitle )
		self.media_player_subs_list = media_player_subs_list
				
	def _GetDialog( self ):
		class Dlg( SelectSubtitlesDlg ):
			def __init__( self, parent, title, media_player_subs_list, current_subtitle = '' ):
				SelectSubtitlesDlg.__init__( self, parent=parent, title=title, current_subtitle = current_subtitle, size=(650, 250) )
				for s in media_player_subs_list:
					logging.debug( 'doing {}'.format( s ) )
					if( s[0] == -1 or s[1] == 'Disable' ):
						continue	#skip the 'disable' item, we implement this with a checkbox
					self.subtitles.append( s[1] )
				self.FillList()
				
			def GetSelectedSubtitle( self ):
				index = self.subtitle_list.GetFirstSelected()
				if( -1 == index ):
					return None
					
				return index + 1
				
		return Dlg( self.parent, 'Select subtitle', self.media_player_subs_list, self.current_subtitle )
		

class UPnPSubtitlesDlg( SubtitlesDlg ):
	def __init__( self, parent, SelectedSubtitlesCallback, subs_list, current_subtitle = '' ):
		SubtitlesDlg.__init__( self, parent, SelectedSubtitlesCallback, current_subtitle )
		self.subs_list = subs_list
		
		
	def _GetDialog( self ):
		class Dlg( SelectSubtitlesDlg ):
			def __init__( self, parent, title, subs_list, current_subtitle = '' ):
				SelectSubtitlesDlg.__init__( self, parent=parent, title=title, current_subtitle = current_subtitle, size=(650, 250) )
				self.subs_list = subs_list
				index = 1
				for s in self.subs_list:
					logging.debug( 'doing {}'.format( s ) )
					self.subtitles.append( str( index ) )
					index += 1
				self.FillList()
				
			def GetSelectedSubtitle( self ):
				index = self.subtitle_list.GetFirstSelected()
				if( -1 == index ):
					return None
					
				return self.subs_list[ index - 1 ]
				
		return Dlg( self.parent, 'Select subtitle', self.subs_list, self.current_subtitle )


if __name__ == '__main__':
	app = wx.App()
	app.MainLoop()
	
	def ChosenSubtitle( ok, show_subtitles, subtitle ):
		print( 'ok: {}, show_subtitles: {}, subtitle: {}'.format( ok, show_subtitles, subtitle ) )
		
	#dlg = FileSubtitlesDlg( None, ChosenSubtitle, '/media/Elements/', '/media/Elements/movies/Agora.2009.DVDRiP.XViD-iKA.www.USABIT.com/Cd1/' )
	dlg = DVDSubtitlesDlg( None, ChosenSubtitle, [(-1, 'Disable'), (2, 'Track 1'), (3, 'Track 2'), (4, 'Track 3')], 'Track 3' )
	dlg.ShowDialog()
