#!/usr/bin/python
# -*- coding: utf-8 -*-

#import wx
import os
import subprocess
import time

class Sounds:
	def __init__( self ):
		pass
		
	def __PlayFile( self, soundFile ):
		playSoundScript = os.getcwd() + '/scripts/play_soundfile'
		SoundsFolder = os.getcwd() + '/sounds/'
		soundfileFull = SoundsFolder + soundFile
		subprocess.call( ['sh', playSoundScript, soundfileFull] )
		#sound = wx.Sound( soundfileFull )
		#if sound.IsOk():
			#print( 'Playing soundfile {}'.format( soundfileFull ) )
			#sound.Play(wx.SOUND_SYNC)
		#else:
			#print( 'Playing wx.Bell' )
			#wx.Bell()

	def PlayError( self ):
		self.__PlayFile( 'Windows Critical Stop.wav' )

	def PlayCancel( self ):
		self.__PlayFile( 'Windows Critical Stop.wav' )
		#wx.Bell()
		#time.sleep( 1 )
		#wx.Bell()
		
	def PlayComplete( self ):
		self.__PlayFile( 'Ready.wav' )
		#wx.Bell()
		
if __name__ == '__main__':
	sounds = Sounds()
	sounds.PlayError()
	time.sleep( 2 )
	sounds.PlayCancel()
	time.sleep( 2 )
	sounds.PlayComplete()
