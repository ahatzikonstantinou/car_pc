#! /bin/python

class AT:
	def __init__( self, device ):
		self.device = device
		#do sdp browse
		
		#check if DUN is in the response

		self.supportsDUN = False	#else True
		#if yes extract rfcomm channel from the sdptool response
		self.rfcommChannel = -1 #else save the DUN rfcomm channel
		
	def SupportsPhonebook( self ):
		if not self.supportsDUN:
			return False
		
		#else
			#attempt rfcomm connection to DUN channel
			#if attempt fails return False
			#check if at+cbpr? is supported
			#send at+cpbr?
			#if ok is in the response return True
			#else return False
		pass
		
	def GetPhonebook( self ):
		#rfcomm connect to DUN channel
		#send at+cpbr=?
		#extract phonebook from reply
		pass