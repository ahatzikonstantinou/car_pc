#! /bin/python
# -*- coding: utf-8 -*-

import re
import os

class Phonenumber:
    HOUSE = 0
    CELL = 1
    WORK = 2
    OTHER = 3
    def __init__( self ):
	self.phoneType = -1
	self.number = ''
	    
class PhonebookEntry:    
    def __init__( self, convert_function ):
	self.name = ''
	self.convertedName = ''
	self.words = [] #these are the words of the convertedName
	self.matchingWords = []
	self.numbers = []
	self.convert_function = convert_function
	
    def Copy( self ):
	c = PhonebookEntry( self.convert_function )
	c.name = self.name
	c.convertedName = self.convertedName
	c.words = self.words[:]
	c.matchingWords = self.matchingWords[:]
	c.numbers = self.numbers[:]
	return c
    
    def Contains2( self, chars, pos ):
	#print( 'searching for chars {} at pos {}'.format( chars, pos ) )
	if( pos == 0 ):
	    self.matchingWords = self.convertedName.split() + [ n.number for n in self.numbers ]
	#print( 'will look in {}'.format( self.matchingWords ) )
	matches = []
	for w in self.matchingWords:
	    #print( 'Looking in {}'.format( w ) )
	    for char in chars:
		#print( ' for {}'.format( char ) )
		if( len( w ) > pos and w[pos] == char and w not in matches ):
		    #print( 'found a match {}.find({}) == pos'.format( w, char, pos ) )
		    matches.append( w )
		    break
	    #matches = [ x for x in self.matchingWords if x.find( char ) == pos ]
	self.matchingWords = matches
	
	#if( len( self.matchingWords ) > 0 ):
	    #for w in self.matchingWords:
		#print( w )
	#else:
	    #print( 'No matches found' )
	    
	return len( self.matchingWords ) > 0
	
    def Contains( self, pattern ):
	regPattern = r'\b' + pattern
	if re.search( regPattern, self.convertedName, re.U ) is not None:
	    return True
	#if pattern in ( self.convertedName ):
	    #return True
	for number in self.numbers:	    
	    if re.search( regPattern, number.number, re.U ) is not None:
		return True
	    
	    #for >10 digit numbers i.e. with full international code also
	    #try to match the last 10 numbers
	    if len( number.number ) > 10 and re.search( regPattern, number.number[-10:], re.U ) is not None:
		return True
		
	    #if pattern in number.number:
		#return True
	
	return False
	
    def HasNumber( self, callingNumber ):
	for number in self.numbers:	    
	    if number.number.find( callingNumber ) > -1:
		return True

	return False
	
    def FromVCard( self, vcard ):
	lines = vcard.split( "\r\n" )
	nameFound = False
	name = ''
	numbers = []
	for line in lines:	    
	    if 'FN:' in line:
		name = line[3:].replace( '\,', '' )
		nameFound = True
		#print( 'Found name {}'.format( name ) )
	    elif 'TEL;' in line:
		tel = re.compile(r'TEL;TYPE=(\S+):(.*)').match( line ).groups()	
		#if 'VOICE' not in tel[0]:	#if this is not a voice telephone e.g. fax
		    #continue
		telType = Phonenumber.OTHER
		if 'WORK' in tel[0]:
		    telType = Phonenumber.WORK
		elif 'HOUSE' in tel[0]:
		    telType = Phonenumber.HOUSE
		elif 'CELL' in tel[0]:
		    telType = Phonenumber.CELL
		n = Phonenumber()
		n.phoneType = telType
		n.number = tel[1]
		numbers.append( n )
		#print( ' and added number {}'.format( n ) )
	if nameFound and len( numbers ) > 0 :
	    self.name = name
	    self.convertedName = self.convert_function( name )
	    #print( 'converted {} to {}'.format( self.name, self.convertedName ) )
	    self.words = self.convertedName.split()
	    self.numbers = numbers
	    #print( ' returning True' )
	    return True
	
	return False
	     
class PhonebookSearchResult:
    def __init__( self ):
	self.pos = -1
	self.matches = []
	self.chars = []
	
class Phonebook:
    Conversions = 'search_normalisations'
    def __init__( self, entries = None, conversions = None ):
	self.entries = {}   #a dictionary of names that contains entries of phones/phonetypes
	if( entries is not None ):
	    self.entries = entries
	self.conversions = []
	if conversions is None:
	    self.__LoadConversions()
	self.searchResults = [] #list of PhonebookSearchResult
	    
    def __LoadConversions( self ):	
	path = os.getcwd() + '/phonebook/' + Phonebook.Conversions + '/'

	if not os.path.exists( path ):
	    print( 'Conversion file {} does not exist'.format( path ) )
	    return
	
	print( 'Loading conversions {}...'.format( path ) )    
	for filename in os.listdir( path ):
	    print filename
	    with open( path+'/'+filename ) as f:
		lines = f.readlines()
		for line in lines:
		    parts = line.split( '=' )
		    source = parts[0].split( ',' )
		    target = parts[1].strip()
		    self.conversions.append( [source, target] )
	
    def Convert( self, text ):
	#print( 'will convert {}'.format( text ) )
	convertedText = ''
	for ch in text.lower():
	    converted = False
	    #print( 'will test {} against {} patterns'.format( ch, len( self.conversions ) ) )
	    for cn in self.conversions:		
		if ch in cn[0]:
		    convertedText = convertedText + cn[1]
		    converted = True
		    #print( 'Converted char {} to {}'.format( ch, cn[1] ) )
		    break
	    if not converted:
		convertedText = convertedText + ch
	#print( 'Converted {} -> {}'.format( text, convertedText ) )
	return convertedText

    def Filter2( self, chars, pos ):
	#print( 'Filter2 starting with available positions {}'.format( [r.pos for r in self.searchResults] ) )
	#chs = u''
	#for ch in chars:
	    #chs += ch
	#print( 'search chars: {}'.format( chs ) )
	res = PhonebookSearchResult()
	if( len( self.searchResults ) -1 < pos ):	    
	    res.chars = chars
	    res.pos = pos
	    #entries = {}
	    startKeys = self.entries.keys() #start with the keys of all entries
	    contacts = [ c.Copy() for c in self.entries.values() ]
	    #if previous search results are available use those from the last position
	    if( len( self.searchResults ) > 0 ): 
		matches = [ r for r in self.searchResults if r.pos == pos - 1 ][0].matches
		contacts = [ m.Copy() for m in matches ]
		
	    #print( 'will search for a match starting with {} keys: {}'.format( len( startKeys ), startKeys ) )
	    #res.matches = [ key for key, value in self.entries.iteritems() if key in startKeys and value.Contains2( chars, pos ) ]
	    
	    #print( 'copy contacts:' )
	    for c in contacts:
		#print( '{} with {} matching words'.format( c.name, len( c.matchingWords ) ) )
		#for w in c.matchingWords:
		    #print( '\t{}, '.format( w ) ),
		    #print( '\n' )
		if c.Contains2( chars, pos ):
		    #entries[ key ] = value
		    res.matches.append( c )
	    self.searchResults.append( res )
	    #print( 'added result with {} matches to pos {}'.format( len( res.matches ), res.pos ) )
	    #print( 'available positions {}'.format( [r.pos for r in self.searchResults] ) )
	else:
	    #clean up later search results
	    self.searchResults[:] = [ r for r in self.searchResults if r.pos <= pos ]
	    #print( 'will try to locate result in pos {}'.format( pos ) )
	    #print( 'available positions {}'.format( [r.pos for r in self.searchResults] ) )
	    res = [ r for r in self.searchResults if r.pos == pos ][0]
	    #print( 'found res at pos {} with {} matches'.format( res.pos, len( res.matches ) ) )
	#return Phonebook( entries, self.conversions )
	return res.matches
	
    def Filter( self, patterns ):
	entries = {}
	for key, value in self.entries.iteritems():
	    for pattern in patterns:
		if value.Contains( self.Convert( pattern ) ):
		    entries[ key ] = value
		    break
	
	return Phonebook( entries, self.conversions )
	
    def FromPbapVCards( self, vcards ):
	#print( 'starting with {} vcards: {}'.format( len( vcards ), vcards ) )
	for card in vcards:
	    entry = PhonebookEntry( self.Convert )
	    if entry.FromVCard( card ):
		self.entries[ entry.name ] = entry
		
    def ContactLookup( self, number ):
	#print( 'Looking for number {}'.format( number ) )
	for key, value in self.entries.iteritems():
	    if( value.HasNumber( number ) ):
		return value.name
	return ''
	
if __name__ == '__main__':
    #p = PhonebookEntry()
    m = re.search( r'\bΕνωμ', 'Ενωμένα Εργοστάσια', re.U )
    print( 'match {}-{}'.format( m.start(), m.end() ) )	
