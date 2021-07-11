class BaseTick:
    def __init__(self):
        self.vocaloid_time_resolution = 480
        self.cevio_time_resolution = 960
        # TODO: 어디 쓰이는지 확인 필요
        self.start_tick = 3840
        self.shift_octave = -1
        self.center_note_number = 64
        self.ccs_code = '7251BC4B6168E7B2992FA620BD3E1E77'

    @property
    def difference(self):
        return self.cevio_time_resolution / self.vocaloid_time_resolution
