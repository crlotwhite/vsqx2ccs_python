from ccs.models.base_tick import BaseTick


class BeatData:
    def __init__(self):
        self.denominator = ""
        self.numerator = ""
        self._tempo_change_point = 0
        #TODO: 왜 deff지?
        self.deff = BaseTick()

    @property
    def tempo_change_point(self):
        return self._tempo_change_point

    @tempo_change_point.setter
    def tempo_change_point(self, value):
        self._tempo_change_point = int(int(value) * self.deff.start_tick * 4 / 4)
