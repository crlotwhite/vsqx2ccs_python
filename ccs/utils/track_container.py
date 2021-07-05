class TrackContainer(list):
    def __getitem__(self, track_number):
        for item in self:
            if item.track_number == track_number:
                return item

        return None
