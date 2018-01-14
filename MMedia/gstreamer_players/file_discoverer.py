#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import gst

from gst.extend.pygobject import gsignal


class FileDiscoverer:
	'''
	The 'discovered' callback has one boolean argument, which is True if the
    file contains decodable multimedia streams.
    '''
	__gsignals__ = {
		'discovered' : (gobject.SIGNAL_RUN_FIRST,
		None,
		(gobject.TYPE_BOOLEAN, ))
	}

	def __init__( self, filename, timeout=3000, max_interleave=1.0 ):
		self.is_video = False
		self.is_audio = False
		self.finished = False

		self._success = False
		self._nomorepads = False

		self._timeoutid = 0
		self._timeout = timeout
		self._max_interleave = max_interleave

		if not os.path.isfile(filename):
			self.debug("File '%s' does not exist, finished" % filename)
			self.finished = True
			return
		
		# the initial elements of the pipeline
		self.src = gst.element_factory_make("filesrc")
		self.src.set_property("location", filename)
		self.src.set_property("blocksize", 1000000)
		self.dbin = gst.element_factory_make("decodebin")
		self.add(self.src, self.dbin)
		self.src.link(self.dbin)
		self.typefind = self.dbin.get_by_name("typefind")

		def _timed_out_or_eos(self):
			if (not self.is_audio and not self.is_video) or \
				(self.is_audio and not self.audiocaps) or \
				(self.is_video and not self.videocaps):
				self._finished(False)
			else:
				self._finished(True)

		def _finished(self, success=False):
			self.debug("success:%d" % success)
			self._success = success
			self.bus.remove_signal_watch()
			if self._timeoutid:
				gobject.source_remove(self._timeoutid)
				self._timeoutid = 0
			gobject.idle_add(self._stop)
			return False

		def _stop(self):
			self.debug("success:%d" % self._success)
			self.finished = True
			self.set_state(gst.STATE_READY)
			self.debug("about to emit signal")
			self.emit('discovered', self._success)

		def discover(self):
			"""Find the information on the given file asynchronously"""
			self.debug("starting discovery")
			if self.finished:
				self.emit('discovered', False)
				return

			self.bus = self.get_bus()
			self.bus.add_signal_watch()
			self.bus.connect("message", self._bus_message_cb)

			# 3s timeout
			self._timeoutid = gobject.timeout_add(self._timeout, self._timed_out_or_eos)

			self.info("setting to PLAY")
			if not self.set_state(gst.STATE_PLAYING):
				self._finished()