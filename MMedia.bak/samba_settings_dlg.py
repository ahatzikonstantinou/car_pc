#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import logging
import gio
from threading import *

from samba.samba_provider import *

class SambaSettingsDlg( wx.Dialog ):
	def __init__( self, parent, title, stations = {} ):
		wx.Dialog.__init__(self, parent=parent, title=title, size=(-1, -1), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.panel = SambaSettingsPanel( self, samba_provider = SambaProvider( domain = 'WORKGROUP', username = 'antonis', password = '312ggp12' ) )
	
class SambaSettingsPanel( wx.Panel ):
	DEBUG = False
	def __init__( self, parent, id = wx.ID_ANY, samba_provider = None ):
		wx.Panel.__init__( self, parent, id, pos = ( -1, -1 ), size = ( -1, -1 ) )

		self.samba_provider = samba_provider
		self.samba_provider.AddMountFinishedObserver( self )
		
		self.valid_selected_samba_item = None
		
		sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.SetSizer( sizer )
		
		self.tree_panel = wx.Panel( self )
		
		self.tree = wx.TreeCtrl( self.tree_panel, wx.ID_ANY, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_SINGLE )
		self.root = self.tree.AddRoot('Network')
		self._FillTree()
		self.tree.ExpandAll()
		self.tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged )
		
		self.expand_all_BTN = wx.Button( self.tree_panel, label='Expand all' )
		self.expand_all_BTN.Bind( wx.EVT_BUTTON, self.OnExpandAll )
		self.collapse_all_BTN = wx.Button( self.tree_panel, label='Colapse all' )
		self.collapse_all_BTN.Bind( wx.EVT_BUTTON, self.OnCollapseAll )
		self.refresh_tree_BTN = wx.Button( self.tree_panel, label='Refresh' )
		self.refresh_tree_BTN.Bind( wx.EVT_BUTTON, self.OnRefreshTree )
		
		selectionLabelST = wx.StaticText( self, label = 'Selected:' )
		usernameLabelST = wx.StaticText( self, label = 'username:' )
		passwordLabelST = wx.StaticText( self, label = 'password:' )
		
		self.selectedST = wx.StaticText( self )
		self.usernameTC = wx.TextCtrl( self )
		self.usernameTC.AppendText( self.samba_provider.authentication.username )
		self.passwordTC = wx.TextCtrl( self )
		self.passwordTC.AppendText( self.samba_provider.authentication.password )
		
		self.automount_CHK = wx.CheckBox( self, wx.ID_ANY, 'Automount' )
		self.automount_CHK.Bind( wx.EVT_CHECKBOX, self.OnCheckClick )
		
		test_BTN = wx.Button( self, wx.ID_ANY, 'Mount' )
		test_BTN.Bind( wx.EVT_BUTTON, self.OnMount )
		
		#save_BTN = wx.Button( self, wx.ID_ANY, 'Save' )
		#save_BTN.Bind( wx.EVT_BUTTON, self.OnSave )
		
		self.statusST = wx.StaticText( self )
		
		tree_panel_sizer = wx.BoxSizer( wx.VERTICAL )
		self.tree_panel.SetSizer( tree_panel_sizer )
		tree_buttons_sizer = wx.BoxSizer( wx.HORIZONTAL )

		tree_buttons_sizer.Add( self.expand_all_BTN )
		tree_buttons_sizer.Add( self.collapse_all_BTN )
		tree_buttons_sizer.Add( self.refresh_tree_BTN )

		tree_panel_sizer.Add( self.tree, 1, wx.EXPAND | wx.ALL, 5 )
		tree_panel_sizer.Add( tree_buttons_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		
		data_sizer = wx.FlexGridSizer( 2, 2 )
		data_sizer.AddMany([
			usernameLabelST, ( self.usernameTC, 1, wx.EXPAND ),
			passwordLabelST, ( self.passwordTC, 1, wx.EXPAND )
		])
		data_sizer.AddGrowableCol(1, 1)
		
		vsizer = wx.BoxSizer( wx.VERTICAL )

		vh_sizer = wx.BoxSizer( wx.HORIZONTAL )		
		vh_sizer.Add( selectionLabelST, 0, wx.ALL, 5 )
		vh_sizer.Add( self.selectedST, 1, wx.ALL, 5 )
		
		vh_sizer2 = wx.BoxSizer( wx.HORIZONTAL )
		vh_sizer2.Add( test_BTN )
		#vh_sizer2.Add( save_BTN )
		
		vsizer.Add( vh_sizer, 1, wx.EXPAND | wx.ALL, 5 )
		vsizer.Add( data_sizer, 0, wx.EXPAND | wx.ALL, 5 )
		vsizer.Add( self.automount_CHK, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		vsizer.Add( vh_sizer2, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		vsizer.Add( self.statusST, 0, wx.ALIGN_CENTER | wx.ALL, 5 )

		sizer.Add( self.tree_panel, 2, wx.EXPAND | wx.ALL, 5 )
		sizer.Add( vsizer, 1, wx.ALL, 5 )
		
		
	def OnExpandAll( self, event ):
		self.tree.ExpandAll()
		
	def OnCollapseAll( self, event ):
		self.tree.CollapseAll()
		
	def _FillTree( self, parent_dir = None ):
		'''
		TODO: add icons for automounted shares
		'''
		parent_dir_name = ( self.tree.GetItemText( parent_dir ) if parent_dir else '' )
		if( SambaSettingsPanel.DEBUG ):
			logging.debug( 'will browse {}'.format( parent_dir_name ) )
		for si in self.samba_provider.Browse( parent_dir_name ):
			if( SambaSettingsPanel.DEBUG ):
				logging.debug( 'Adding {} to the tree'.format( si.name ) )
			new_item = self.tree.AppendItem( ( parent_dir if parent_dir else self.root ), si.name )
			self.tree.SetItemData( new_item, wx.TreeItemData( si ) )
			self._FillTree( new_item )
	
	def OnSelChanged( self, event ):
		item = event.GetItem()
		samba_item = self.tree.GetItemData( item ).GetData()
		self.selectedST.SetLabel( '' )
		self.valid_selected_samba_item = None
		self.usernameTC.Clear()
		self.passwordTC.Clear()
		self.usernameTC.AppendText( self.samba_provider.authentication.username )
		self.passwordTC.AppendText( self.samba_provider.authentication.password )
		self.statusST.SetLabel( '' )
		if( samba_item.item_type == SambaItem.SHARE ):
			self.selectedST.SetLabel( self.tree.GetItemText( item ) )
			self.valid_selected_samba_item = samba_item
			automount = self.samba_provider.GetAutomount( samba_item.uri )
			if( automount ):
				self.automount_CHK.SetValue( True )
				self.usernameTC.Clear()
				self.passwordTC.Clear()
				self.usernameTC.AppendText( samba_item.authentication.username )
				self.passwordTC.AppendText( samba_item.authentication.password )
			else:
				self.automount_CHK.SetValue( False )
		
	def OnMount( self, event ):
		if( not self.valid_selected_samba_item ):
			return
		self.samba_provider.authentication = SambaAuthentication( self._GetDomain( self.valid_selected_samba_item ), self.usernameTC.GetValue().strip(), self.passwordTC.GetValue().strip() )
		self.samba_provider.Mount( gio.File( self.valid_selected_samba_item.uri ) )
		#TODO I might get a no response here so I shoudl implement some timeout check
		
	def MountFinished( self, success ):
		if( SambaSettingsPanel.DEBUG ):
			logging.debug( 'Was called with {}'.format( success ) )
		if( success ):
			self.statusST.SetLabel( 'Successfully mounted' )
		else:
			self.statusST.SetLabel( 'Mount failed' )
			
	def OnCheckClick( self, event ):
		if( not self.valid_selected_samba_item ):
			return None
			
		automount = self._GetSambaAutomount()
		if( self.automount_CHK.GetValue() ):
			self.samba_provider.AddAutomount( automount )
		else:
			self.samba_provider.RemoveAutomount( automount )
		
	def _GetDomain( self, samba_item ):
		'''
		TODO:
		'''
		return 'WORKGROUP'
		
	def _GetSambaAutomount( self ):
		'''
		Returns a SambaAutomount from the widgets
		'''
		if( not self.valid_selected_samba_item ):
			return None
			
		return self.valid_selected_samba_item.ToAutomount()
		
	def OnRefreshTree( self, event = None ):
		self.Refresh()
		
	def Refresh( self ):
		self.tree.DeleteChildren( self.root )
		self._FillTree()
		self.tree.ExpandAll()
		
if __name__ == '__main__':
	app = wx.App()
	app.MainLoop()
	dlg = NetworkSettingsDlg( None, 'Network Settings Test' )
	SambaAutomountThread( dlg.panel.samba_provider )
	dlg.ShowModal()
