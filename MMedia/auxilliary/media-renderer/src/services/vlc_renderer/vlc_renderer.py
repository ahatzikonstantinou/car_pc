from brisa.core import log
from brisa.utils.looping_call import LoopingCall


class VLCRenderer(object):

    def __init__(self):
        self.build_pipeline()
        self.__av_uri = None
        self.time_format = gst.Format(gst.FORMAT_TIME)
        self.player_state = 0
        loop = LoopingCall(self.poll_bus)
        loop.start(0.2, True)

    def poll_bus(self):
        if self.bus:
            message = self.bus.poll(gst.MESSAGE_ERROR|gst.MESSAGE_EOS,
                                    timeout=1)
            if message:
                self.on_message(self.bus, message)

    def get_state(self):
        if self.player_state == 0:
            return 'STOPPED'
        if self.player_state == 1:
            return 'PLAYING'
        if self.player_state == 2:
            return 'PAUSED_PLAYBACK'

    def __set_uri(self, uri):
        self.player.set_property('uri', uri)
        self.__av_uri = uri

    def __get_uri(self):
        return self.__av_uri

    av_uri = property(__get_uri, __set_uri)

    def build_pipeline(self):
        self.player = gst.element_factory_make("playbin", "player")
        self.bus = self.player.get_bus()
        self.player.set_state(gst.STATE_READY)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.player_state = 0
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.player_state = 0

    def play(self):
        if self.av_uri is not None:
            if (self.player.set_state(gst.STATE_PLAYING) ==
                gst.STATE_CHANGE_FAILURE):
                log.error("error trying to play %s.", self.av_uri)
            self.player_state = 1
        else:
            log.info("av_uri is None, unable to play.")

    def stop(self):
        if self.player.set_state(gst.STATE_READY) == gst.STATE_CHANGE_FAILURE:
            log.error("error while stopping the player")
        self.player_state = 0

    def pause(self):
        if self.player.set_state(gst.STATE_PAUSED) == gst.STATE_CHANGE_FAILURE:
            log.error("error while pausing the player")
        self.player_state = 2

    def seek(self, unit, target):
        if unit == "ABS_TIME":
            target_time = self.convert_int(target)
            self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH,
                                    target_time)

        if unit == "REL_TIME":
            target_time = self.convert_int(target)
            cur_pos = self.query_position()[1]
            self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH,
                                    target_time+cur_pos)

        if unit == "ABS_COUNT":
            self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH,
                                    target)

        if unit == "REL_COUNT":
            cur_pos = self.query_position()[1]
            self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH,
                                    target + cur_pos)

    def set_volume(self, volume):
        self.player.set_property("volume", volume/10)

    def get_volume(self):
        return int(self.player.get_property("volume")*10)

    def query_duration(self):
        time.sleep(0.3)
        try:
            dur_int = self.player.query_duration(self.time_format, None)[0]
            dur_str = self.convert_ns(dur_int)
        except gst.QueryError:
            dur_int = -1
            dur_str = ''

        return dur_str, dur_int

    def query_position(self):
        try:
            pos_int = self.player.query_position(self.time_format, None)[0]
            pos_str = self.convert_ns(pos_int)
        except gst.QueryError:
            pos_int = -1
            pos_str = ''

        return pos_str, pos_int

    def convert_ns(self, time):
        hours, left_time = divmod(time/1000000000, 3600)
        minutes, left_time = divmod(left_time, 60)
        return '%02d:%02d:%02d' % (hours, minutes, left_time)

    def convert_int(self, time_str):
        time_str = time_str.strip('")( ')
        (hours, min, sec) = time_str.split(":")
        time_int = int(hours) * 3600 + int(min) * 60 + int(sec)
        time_int = time_int * 1000000000
        return time_int

