import logging
logging.basicConfig( level = logging.DEBUG )

class BehaviorState:
	def __init__( self, state, actor ):
		self.state = state
		self.actor = actor

class DeviceBehaviorOnActivate:
	AUDIO_MUTE = 0
	AUDIO_UNMUTE = 1
	PLAYER_PAUSED = 0
	PLAYER_STOPPED = 1
	PLAYER_PLAYING = 2
	ACTOR_USER = 0
	ACTOR_SYSTEM = 1
	
	def __init__( self, device, mute_on_deactivate = False, unmute_on_activate = False, pause_on_deactivate = False, stop_on_deactivate = False, play_on_activate = False ):
		self.device = device
		self.system_mute_on_deactivate = mute_on_deactivate
		self.system_unmute_on_activate = unmute_on_activate
		self.system_mediaplayer_pause_on_deactivate = pause_on_deactivate
		self.system_mediaplayer_stop_on_deactivate = stop_on_deactivate
		self.system_mediaplayer_play_on_activate = play_on_activate
		
		self.audio_state = BehaviorState( DeviceBehaviorOnActivate.AUDIO_UNMUTE, DeviceBehaviorOnActivate.ACTOR_USER )
		self.player_state = BehaviorState( DeviceBehaviorOnActivate.PLAYER_STOPPED, DeviceBehaviorOnActivate.ACTOR_USER )
		
	def Activate( self ):
		logging.debug( 'DeviceBehaviorOnActivate.Activate:' )
		logging.debug( '\tsystem_unmute_on_activate: {}'.format( self.system_unmute_on_activate ) )
		logging.debug( '\taudio_state.state: {}'.format( self.audio_state.state ) )
		logging.debug( '\taudio_state.actor: {}'.format( self.audio_state.actor ) )
		if( self.system_unmute_on_activate and 
			self.audio_state.state == DeviceBehaviorOnActivate.AUDIO_MUTE and 
			self.audio_state.actor == DeviceBehaviorOnActivate.ACTOR_SYSTEM ):
			logging.debug( '\twill SYSTEM unmute [device.SetMute( False )]' )
			self.device.SetMute( False )
			self.audio_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM
		else:
			logging.debug( '\twill NOT unmute' )
			
		logging.debug( '\tsystem_mediaplayer_play_on_activate: {}'.format( self.system_mediaplayer_play_on_activate ) )
		logging.debug( '\tplayer_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tplayer_state.actor: {}'.format( self.player_state.actor ) )
		if( self.system_mediaplayer_play_on_activate and 
			self.player_state.state in ( DeviceBehaviorOnActivate.PLAYER_PAUSED, DeviceBehaviorOnActivate.PLAYER_STOPPED ) and
			self.player_state.actor == DeviceBehaviorOnActivate.ACTOR_SYSTEM ):
			logging.debug( '\twill SYSTEM play [device.Play()]' )
			self.device.Play()
			self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM
		else:
			logging.debug( '\twill NOT play' )
		
	def Deactivate( self ):
		logging.debug( 'DeviceBehaviorOnActivate.Deactivate:' )
		logging.debug( '\tsystem_mute_on_deactivate: {}'.format( self.system_mute_on_deactivate ) )
		if( self.system_mute_on_deactivate and
			self.audio_state.state == DeviceBehaviorOnActivate.AUDIO_UNMUTE ):
			logging.debug( '\twill SYSTEM mute [device.SetMute( True )]' )
			self.device.SetMute( True )
			self.audio_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM
		else:
			logging.debug( '\twill NOT mute' )
			
		logging.debug( '\taudio_state.state: {}'.format( self.audio_state.state ) )
		logging.debug( '\taudio_state.actor: {}'.format( self.audio_state.actor ) )
			
		logging.debug( '\tBefore player_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tsystem_mediaplayer_stop_on_deactivate: {}'.format( self.system_mediaplayer_stop_on_deactivate ) )
		logging.debug( '\tsystem_mediaplayer_pause_on_deactivate: {}'.format( self.system_mediaplayer_pause_on_deactivate ) )
		if( self.player_state.state == DeviceBehaviorOnActivate.PLAYER_PLAYING ):
			if( self.system_mediaplayer_stop_on_deactivate ):
				logging.debug( '\twill SYSTEM stop [device.Stop()]' )
				self.device.Stop()
				self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM			
			elif( self.system_mediaplayer_pause_on_deactivate ):
				logging.debug( '\twill SYSTEM pause [device.Pause()]' )
				self.device.Pause()
				self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM
			else:
				logging.debug( '\twill NIETHER stop NOR pause' )
				
		logging.debug( '\tAfter player_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tplayer_state.actor: {}'.format( self.player_state.actor ) )
			
	def SetUserPause( self ):
		logging.debug( 'DeviceBehaviorOnActivate.SetUserPause:' )
		self.player_state.state = DeviceBehaviorOnActivate.PLAYER_PAUSED
		self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_USER
		logging.debug( '\tplayer_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tplayer_state.actor: {}'.format( self.player_state.actor ) )
		
	def SetUserStop( self ):
		logging.debug( 'DeviceBehaviorOnActivate.SetUserStop:' )
		self.player_state.state = DeviceBehaviorOnActivate.PLAYER_STOPPED
		self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_USER
		logging.debug( '\tplayer_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tplayer_state.actor: {}'.format( self.player_state.actor ) )

	def SetUserPlay( self ):
		logging.debug( 'DeviceBehaviorOnActivate.SetUserPlay:' )
		self.player_state.state = DeviceBehaviorOnActivate.PLAYER_PLAYING
		self.player_state.actor = DeviceBehaviorOnActivate.ACTOR_USER
		logging.debug( '\tplayer_state.state: {}'.format( self.player_state.state ) )
		logging.debug( '\tplayer_state.actor: {}'.format( self.player_state.actor ) )
		
	def SetUserMute( self, on ):
		logging.debug( 'DeviceBehaviorOnActivate.SetUserMute {}:'.format( on ) )
		self.audio_state.state = ( DeviceBehaviorOnActivate.AUDIO_MUTE if on else DeviceBehaviorOnActivate.AUDIO_UNMUTE )
		self.audio_state.actor = DeviceBehaviorOnActivate.ACTOR_USER
		logging.debug( '\taudio_state.state: {}'.format( self.audio_state.state ) )
		logging.debug( '\taudio_state.actor: {}'.format( self.audio_state.actor ) )

	def SetSystemMute( self, on ):
		logging.debug( 'DeviceBehaviorOnActivate.SetUserMute {}:'.format( on ) )
		self.audio_state.state = ( DeviceBehaviorOnActivate.AUDIO_MUTE if on else DeviceBehaviorOnActivate.AUDIO_UNMUTE )
		self.audio_state.actor = DeviceBehaviorOnActivate.ACTOR_SYSTEM
		logging.debug( '\taudio_state.state: {}'.format( self.audio_state.state ) )
		logging.debug( '\taudio_state.actor: {}'.format( self.audio_state.actor ) )
