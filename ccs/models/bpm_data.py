from ccs.models.base_tick import BaseTick


class BpmData:
    def __init__(self):
        self.tempo = ""
        self._clock = 0
        self.integer_point = ""
        self.decimal_point = ""
        self.deff = BaseTick()

    @property
    def clock(self):
        return str(int(float(self._clock)))

    @clock.setter
    def clock(self, value):
        self._clock = int(value) * self.deff.difference / 2 + self.deff.start_tick

