from datetime import timedelta

from ccs.models.base_tick import BaseTick


class NoteData:
    # note range
    __note_count_max = 127
    __note_count_min = 0
    __dodecaphonism = 12

    def __init__(self):
        self.deff = BaseTick()

        # note lyric
        self._note_number = self.deff.center_note_number
        self.lyric = "a"

        # note start position and duration
        self.position1 = 0
        self.position2 = 0
        self.begin_position = "0"
        self.duration = str(self.deff.cevio_time_resolution)
        self._play_time = timedelta()

        # cevio note count
        self._pitch_step = 5
        self._pitch_octave = 0

    def set_tick(self, _note_number):
        """
        Set the scale in CeVIO from the note number
        :param note_number (int):
        :return:
        """
        note_number = int(_note_number)
        if note_number > self.__note_count_max:
            self.note_number = self.__note_count_max

        if note_number < self.__note_count_min:
            self.note_number = self.__note_count_min

        # Scale adjustment
        self._pitch_octave = note_number // self.__dodecaphonism + self.deff.shift_octave
        self._pitch_step = note_number % self.__dodecaphonism

    @property
    def clock(self):
        return str(int(float(self.begin_position)))

    @property
    def pitch_octave(self):
        return str(self._pitch_octave)

    @property
    def pitch_step(self):
        return str(self._pitch_step)

    @property
    def note_number(self):
        return self._note_number

    @note_number.setter
    def note_number(self, value):
        self._note_number = value
        self.set_tick(value)

    @property
    def play_time(self):
        h = self._play_time.total_seconds()//3600
        m = (self._play_time.total_seconds() % 3600) // 60
        s = (self._play_time.total_seconds() % 3600) % 60
        make_str = f"{h}:{m}:{s}"
        return make_str

    @play_time.setter
    def play_time(self, value):
        self._play_time = timedelta(int(value))

    def set_begin_tick(self, vsqx_begin):
        # Doubled for processing by CeVIO + start value
        self.position1 = int(vsqx_begin) * self.deff.difference + self.deff.start_tick
        self.begin_position = str(self.position1)

    def set_duration(self, vsqx_duration):
        # Corrected for processing with CeVIO
        self.position2 = int(vsqx_duration) * self.deff.difference
        self.duration = str(int(self.position2))
