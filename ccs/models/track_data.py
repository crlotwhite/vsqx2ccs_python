from typing import List
from uuid import uuid4

from ccs.models.note_data import NoteData


class TrackData:
    def __init__(self):
        self.track_name = ""
        self.note: List[NoteData] = list()

        self._track_number = 0

        # track status
        self.mute = 0
        self.solo = 0
        self.volume = 0

        # GUID for track and mixer identification
        self.guid_value = uuid4()

    @property
    def track_guid(self):
        return str(self.guid_value)

    @property
    def track_number(self):
        return self._track_number

    @track_number.setter
    def track_number(self, value):
        self._track_number = int(value)
