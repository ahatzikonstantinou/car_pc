#! /usr/bin/python
# -*- coding: utf-8 -*-

import AT
import Pbap
from Phonebook import *
from threading import Thread

import pygtk
pygtk.require("2.0")

import gtk
import gtk.glade
import gobject
import pango
import glib

import sys
import time
import re
import cgi

class ContactsGUI:
	def __init__( self, device, dialCallback = None ):
		self.__device = device
		self.__dialCallback = dialCallback
		self.__phonebook = Phonebook()
		self.__drawPhonebook = self.__phonebook
		self.__CreateControl()
		self.__GetPhonebookStartThread()
		#glib.threads_init()
		gtk.gdk.threads_init()
		
	def __CreateControl( self ):
		self.__contactsList = gtk.ScrolledWindow()
		self.__contactsList.set_policy( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC )
		self.__vbox = gtk.VBox( True, 0 )
		self.__contactsList.add_with_viewport( self.__vbox )
		self.__vbox.show()
		self.__contactsList.show()
		
	def GetControl( self ):
		return self.__contactsList
		#return self.__vbox
		
	def __GetPhonebookStartThread( self ):
		print( 'starting thread...' )
		self.__SetMessage( "Initializing" )
		#glib.idle_add( self.__GetPhonebookThread )
		Thread(target=self.__GetPhonebookThread).start()
		print( 'starting thread finished' )
		
	def __GetPhonebookThread( self ):
		print( 'thread started' )
		phonebookIsAvailable = self.__GetPhonebook()
		print( 'GetPhonebook() returned {}'.format( phonebookIsAvailable ) )
		if( phonebookIsAvailable ):
			self.__DrawContacts()
		else:
			gobject.idle_add( self.__SetMessage, "Phonebook not available" )
		print( 'thread finished' )
		return False
		
	def __GetPhonebook( self ):
		print( 'GetPhonebook started' )
		pbapContacts = Pbap.Pbap( self.__device )
		if( pbapContacts.SupportsPhonebook() ):
			self.__phonebook.FromPbapVCards( pbapContacts.GetVCards() )
			self.__drawPhonebook = self.__phonebook
			return True
		else:
			atContacts = AT.AT( self.__device )
			if( atContacts.SupportsPhonebook() ):
				self.__phonebook = atContacts.GetPhonebook()
				self.__drawPhonebook = self.__phonebook
				return True
		return False

	def __DrawContactsNew( self, pattern = None ):
		self.__ClearContactsList()
		keys = sorted( self.__drawPhonebook.entries.keys() )
		text = ''
		for key in keys:
			c = self.__drawPhonebook.entries[key]
			text = c.name + '\r\n'
			label = gtk.Button( text )
			label.show()
			gobject.idle_add( self.__vbox.pack_start, label, False )
		return False
		
	def __DrawContacts( self, pattern = None ):
		print( '__DrawContacts started' )
		self.__ClearContactsList()
		keys = sorted( self.__drawPhonebook.entries.keys() )
		for key in keys:
			c = self.__drawPhonebook.entries[key]
			self.__DrawContact( c, pattern ) #Highlighted
			#time.sleep( 0.001 )
		print( '__DrawContacts finished' )
		return False
			
	def __ClearContactsList( self ):
		print( 'will clear all contacts' )
		children = self.__vbox.get_children()
		print( 'will remove {} children widgets'.format( len( children ) ) )
		for child in children:
			print( 'will remove child {}'.format( child ) )
			self.__vbox.remove( child )
		print( 'finished clearing contacts' )
		
	def __BuildTextView( self, text, parentControl, pattern = None ):
		textview = gtk.TextView()
		#textview.set_editable( False )
		#textview.set_cursor_visible( False )
		textview.set_wrap_mode( gtk.WRAP_WORD )
		textview.set_justification( gtk.JUSTIFY_LEFT )
		textview.modify_base( gtk.STATE_NORMAL, parentControl.get_style().bg[gtk.STATE_NORMAL])
		textview.modify_bg( gtk.STATE_NORMAL, parentControl.get_style().bg[gtk.STATE_NORMAL])

		textbuffer = textview.get_buffer()
		textbuffer.set_text( text )
		textbuffer.create_tag( 'highlight',	background='yellow' )
		#if pattern is not None:
			#try:
				#index = text.index( pattern )
				#print( 'will highlight {} which matches pattern "{}", positions:{} - {}'.format( 
					#text, pattern, index, index + len( pattern ) ) )
				#colormap = TestText.colormap
				#color = colormap.alloc_color(0xAAAA, 0xAAAA, 0xAAAA)
				#tag = textbuffer.create_tag( 'highlight',	background_gdk=color )
				#tag = textbuffer.create_tag( 'highlight',	background='yellow' )
				#start = textbuffer.get_iter_at_offset( 1 )
				#end = textbuffer.get_iter_at_offset( 6 )
				#textbuffer.apply_tag( 
					#tag, 
					#start, #textbuffer.get_start_iter(),
					#end #textbuffer.get_end_iter()
					#)
			#except:
				#pass
				#
		textview.show()
		return textview
		
	def __BuildLabel( self, text ):
		width_chars = 30
		label = gtk.Label( text )
		label.props.wrap = True
		label.props.width_chars = width_chars
		label.set_justify(gtk.JUSTIFY_LEFT)
		label.show()
		return label
		
	def __DrawContact( self, contact, pattern = None ):		
		#button = gtk.Frame()
		button = gtk.Button()		
		
		box = gtk.VBox( False )
		#button.nameTextView = self.__BuildTextView( contact.name, button, pattern )
		#box.pack_start( button.nameTextView, False )
		lalign = gtk.Alignment(0, 0, 0, 0)
		lalign.add( self.__BuildLabel( contact.name ) )
		lalign.show()
		box.pack_start( lalign, False )
		
		#button.numberTextviews = []
		for number in contact.numbers:			
			t = 'Other'
			if number.phoneType == Phonenumber.HOUSE:
				t = 'House'
			elif number.phoneType == Phonenumber.CELL:
				t = 'Mobile'
			elif number.phoneType == Phonenumber.WORK:
				t = 'Work'
			hbox = gtk.HBox( False )
			l = gtk.Label( t+':' )
			l.show()
			hbox.add( l )
			#numberTextview = self.__BuildTextView( number.number, button, pattern )
			#numberTextview.show()
			#button.numberTextviews.append( numberTextview )
			#hbox.add( numberTextview )
			hbox.pack_start( self.__BuildLabel( number.number ), False, False, 0 )
			hbox.show()
			box.pack_start( hbox, False )
		#-------------
		#l1 = gtk.Label( contact.name )
		#l2 = gtk.Label( text )
		#box.add( l1 )
		#box.add( l2 )
		#l1.show()
		#l2.show()
		#-------------
		
		button.add( box )
		box.show()
		
		#self.__vbox.pack_start( box, False )
				
		button.contact = contact
		button.connect("clicked", self.__ContactDlg, None)
		gobject.idle_add( self.__vbox.pack_start, button, True, True, 0 )
		button.show()
		
	def __SetMessage( self, message ):
		print( 'setting message: {}'.format( message ) )
		self.__ClearContactsList()
		label = gtk.Label( message )
		self.__vbox.add( label )
		label.show()
		return False
		
	def Refresh( self ):
		self.__GetPhonebookThread()
		
	def __HighlightEntry( self, entryControl, pattern ):
		#do the name
		#print( 'will search for {} in {}'.format( pattern, entryControl.contact.convertedName ) )
		regPattern = r'\b' + pattern
		match = re.search( regPattern, entryControl.contact.convertedName, re.U )
		if( match is not None ):
			actualBuffer = entryControl.nameTextView.get_buffer()
			start = actualBuffer.get_start_iter()
			end = actualBuffer.get_start_iter()
			start.set_offset( match.start() )
			end.set_offset( match.end() )
			actualBuffer.apply_tag_by_name( 
				'highlight', 
				start,
				end
				)		
			
		for tbuf in [ x.get_buffer() for x in entryControl.numberTextviews ]:
			start_iter =  tbuf.get_start_iter()
			found = start_iter.forward_search(pattern,0, None) 
			if found:
				match_start,match_end = found
				#print( 'found a match in number {},{}'.format( match_start,match_end ) )				
				tbuf.apply_tag_by_name( 
					'highlight', 
					match_start,
					match_end
					)
		
	def __ClearHighlights( self, entryControl ):
		return
		buffers = [ x.get_buffer() for x in entryControl.numberTextviews ]
		buffers.append( entryControl.nameTextView.get_buffer() )
		for tbuf in buffers:
			start_iter =  tbuf.get_start_iter()
			end_iter = tbuf.get_end_iter()
			tbuf.remove_all_tags( start_iter, end_iter )

	def Filter2( self, chars, pos ):
		if( chars is None or len( chars ) == 0 ):
			self.ResetFilter()
			return
			
		#phonebook = self.__drawPhonebook.Filter2( chars, pos )
		contacts = self.__drawPhonebook.Filter2( chars, pos )
		print( 'filter2 finished' )
		#self.__ShowByKey( phonebook.entries.keys() )
		self.__ShowByKey( [ c.name for c in contacts ] )
			
	def Filter( self, patterns ):
		if( patterns is None or len( [ p for p in patterns if p is not None and len(p) > 0 ] ) == 0 ):
			self.ResetFilter()
			return
			
		phonebook = self.__drawPhonebook.Filter( patterns )
		#self.__DrawContacts( pattern )
		#keys = sorted( phonebook.entries.keys() )
		self.__ShowByKey( phonebook.entries.keys() )
		
	def __ShowByKey( self, keys ):
		children = self.__vbox.get_children()
		for child in children:
			self.__ClearHighlights( child )
			if child.contact.name not in keys:				
				child.hide()
				#print( 'filter: hide {}'.format( child.contact.name ) )
			else:
				child.show()
				#for pattern in patterns:
					#self.__HighlightEntry( child, self.__phonebook.Convert( pattern ) )
				#print( 'filter: show {}'.format( child.contact.name ) )
		#time.sleep( 0.001 )
		
	def ResetFilter( self ):
		self.__drawPhonebook = self.__phonebook
		self.__drawPhonebook.searchResults = []
		children = self.__vbox.get_children()
		for child in children:
			self.__ClearHighlights( child )
			child.show()
			
	def SetSelectedContact( self, number ):
		#TODO
		#iterate all contacts
		#when contact found
		#	scroll into view
		#	highlight
		pass

	def __ContactDlg( self, widget, data=None ):		
		self.contactDialog = gtk.Dialog( "Contact", None, 0 )
		self.contactDialog.add_button( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL )
		self.contactDialog.set_default_size(250, 300)
		
		numbersList = gtk.ScrolledWindow()
		self.contactDialog.vbox.pack_start( numbersList, True, True, 0 )
		
		numbersList.set_policy( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC )
		vbox = gtk.VBox( False, 0 )
		numbersList.add_with_viewport( vbox )
		
		contact = widget.contact
		nameLabel = gtk.Label()
		nameLabel.set_markup( '<span size="x-large" weight="heavy">' + cgi.escape( contact.name ) + '</span>' )
		nameLabel.props.wrap = True
		nameLabel.props.width_chars = 50
		nameLabel.set_justify(gtk.JUSTIFY_LEFT)
		nameLabel.show()
		vbox.pack_start( nameLabel, False, False, 10 )
		
		for number in contact.numbers:
			button = gtk.Button()
			button.number = number
			t = 'Other'
			if number.phoneType == Phonenumber.HOUSE:
				t = 'House'
			elif number.phoneType == Phonenumber.CELL:
				t = 'Mobile'
			elif number.phoneType == Phonenumber.WORK:
				t = 'Work'
			hbox = gtk.HBox( False )
			l = gtk.Label( t+': ' )
			l.show()
			hbox.pack_start( l, False, False, 0 )	
			nl = gtk.Label( number.number )		
			hbox.pack_start( nl, False, False, 0 )
			hbox.show()
			button.add( hbox )
			button.set_size_request( -1, 60 )			
			button.connect("clicked", self.__Dial, None)
			vbox.pack_start( button, False, False, 0 )
			
		vbox.show()
		numbersList.show()

		self.contactDialog.show_all()

		response = self.contactDialog.run()

		self.contactDialog.destroy()
	
	def __Dial( self, widget, data=None ):
		number = widget.number.number
		#md = gtk.MessageDialog(None, 
			#gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
			#gtk.BUTTONS_CLOSE, number )
		#md.run()
		#md.destroy()
		self.contactDialog.destroy()
		self.__dialCallback( number )
		
	def ContactLookup( self, number ):
		return self.__phonebook.ContactLookup( number )
		
if __name__ == "__main__":
	class TestForm:
		def __init__(self, device ):
			self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
			#self.button = gtk.Button("Hello World")
			#self.window.add(self.button)
			#self.button.show()
			#self.window.add( self.contactsGUI.GetControl() )
			
			box = gtk.HBox( False )
			self.entry = gtk.Entry()
			self.entry.show()
			box.pack_start( self.entry, False )
			
			self.filterButton = gtk.Button( 'Filter' )
			self.filterButton.show()
			self.filterButton.connect("clicked", self.filterContacts, None)
			#self.filterButton.connect("clicked", self.testFilter, None)
			box.pack_start( self.filterButton, False )
			
			self.clearButton = gtk.Button( 'Clear' )
			self.clearButton.show()
			self.clearButton.connect("clicked", self.clearFilter, None)
			box.pack_start( self.clearButton, False )
			
			box.show()
			vbox = gtk.VBox( False )
			vbox.pack_start( box, False )
			
			self.contactsGUI = ContactsGUI( device )
			
			vbox.add( self.contactsGUI.GetControl() )
			
			vbox.show()
			
			self.window.add( vbox )
			
			#textview = gtk.TextView()
			#self.textbuffer = textview.get_buffer()
			#self.textbuffer.set_text( 'Hello world αυτή είναι μία δοκιμή' )
			#self.tag = self.textbuffer.create_tag( 'highlight',	background='yellow' )
			#textview.show()
			#vbox.pack_start( textview, False )
			#self.window.add( textview )
			
			self.window.connect("destroy", self.destroy)
			 
			self.window.set_default_size( 500, 400 )
			self.window.show()

		def main(self):
			gtk.main()
			
		def filterContacts( self, widget, data=None ):
			self.contactsGUI.Filter( self.entry.get_text().decode( 'utf-8' ) )
			
		def clearFilter( self, widget, data=None ):
			self.entry.set_text( '' )
			
		def testFilter( self, widget, data=None ):
			pattern = self.entry.get_text().decode( 'utf-8' )
			start_iter =  self.textbuffer.get_start_iter()
			found = start_iter.forward_search(pattern,0, None) 
			if found:
			   match_start,match_end = found
			   #self.textbuffer.select_range(match_start,match_end)
			#start = self.textbuffer.get_iter_at_offset( 1 )
			#end = self.textbuffer.get_iter_at_offset( 3 )
			#start = self.textbuffer.get_start_iter()
			#end = self.textbuffer.get_end_iter()			
			self.textbuffer.apply_tag( 
				self.tag, 
				match_start,
				match_end
				)
			
			
		def destroy(self, widget, data=None):
			gtk.main_quit()

	test = TestForm( sys.argv[1] );
	test.main()
