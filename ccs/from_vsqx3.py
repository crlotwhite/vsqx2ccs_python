import xml.etree.ElementTree as ET
from typing import List
from os.path import join

from ccs.models.beat_data import BeatData
from ccs.models.bpm_data import BpmData
from ccs.models.note_data import NoteData
from ccs.models.track_data import TrackData
from ccs.utils.track_container import TrackContainer

from ccs.make_ccs import make_ccs

from vsqx2ccs.settings import MEDIA_ROOT

def from_vsqx3(file_name: str, tree, is_hiragana) -> bool:
    def tag_checker(element: ET.Element, tag_str: str) -> bool:
        def make_tag(raw_tag):
            schema_string = '{http://www.yamaha.co.jp/vocaloid/schema/vsq3/}'
            return f'{schema_string}{raw_tag}'

        return element.tag == make_tag(tag_str)

    base_name = file_name.split('.')
    if base_name[-1] != 'vsqx':
        return False

    save_file_name = base_name[0] + '.ccs'
    save_file_path = join(join(MEDIA_ROOT, 'files'), save_file_name)

    track_list = TrackContainer()
    beat_list: List[BeatData] = []
    bpm_list: List[BpmData] = []

    # parse vsqx file
    root = tree
    for child in root:
        # get track information
        if tag_checker(child, 'mixer'):
            for unit in child:
                if tag_checker(unit, 'vsUnit'):
                    track_data = TrackData()
                    for unit_data in unit:
                        if tag_checker(unit_data, 'vsTrackNo'):
                            track_data.track_number = int(unit_data.text)
                        elif tag_checker(unit_data, 'mute'):
                            track_data.mute = int(unit_data.text)
                        elif tag_checker(unit_data, 'solo'):
                            track_data.solo = int(unit_data.text)

                    track_list.append(track_data)

        # get beat and tempo data
        elif tag_checker(child, 'masterTrack'):
            for master_track_data in child:
                # is beat data
                if tag_checker(master_track_data, 'timeSig'):
                    beat_data = BeatData()
                    for data in master_track_data:
                        if tag_checker(data, 'posMes'):
                            beat_data.tempo_change_point = data.text
                        elif tag_checker(data, 'nume'):
                            beat_data.numerator = data.text
                        elif tag_checker(data, 'denomi'):
                            beat_data.denominator = data.text
                    beat_list.append(beat_data)

                # is tempo data
                elif tag_checker(master_track_data, 'tempo'):
                    bpm_data = BpmData()
                    for data in master_track_data:
                        if tag_checker(data, 'posTick'):
                            bpm_data.clock = data.text
                        elif tag_checker(data, 'bpm'):
                            tempo_str = data.text
                            bpm_data.tempo = tempo_str
                            if len(tempo_str) > 4:
                                bpm_data.integer_point = tempo_str[:3]
                                bpm_data.decimal_point = tempo_str[3:]
                            else:
                                bpm_data.integer_point = tempo_str[:2]
                                bpm_data.decimal_point = tempo_str[2:]

                    bpm_list.append(bpm_data)

        elif tag_checker(child, 'vsTrack'):
            track_number = 0
            for track_information in child:
                if tag_checker(track_information, 'vsTrackNo'):
                    track_number = int(track_information.text)
                elif tag_checker(track_information, 'trackName'):
                    track_list[track_number].track_name = track_information.text
                # get note data with playTime
                elif tag_checker(track_information, 'musicalPart'):
                    play_time = ""
                    note_list = []
                    part_posTick = 0
                    for musical_part_data in track_information:
                        if tag_checker(musical_part_data, 'playTime'):
                            play_time = musical_part_data.text
                        elif tag_checker(musical_part_data, 'posTick'):
                            part_posTick = int(musical_part_data.text)

                        # get data for NoteData
                        elif tag_checker(musical_part_data, 'note'):
                            # from this, a note will be created and added.
                            note_data = NoteData()
                            note_data.play_time = play_time
                            for note_information in musical_part_data:
                                if tag_checker(note_information, 'posTick'):
                                    # The note tag records the position relative to the part position.
                                    note_tick = part_posTick + int(note_information.text)
                                    note_data.set_begin_tick(note_tick)
                                elif tag_checker(note_information, 'durTick'):
                                    note_data.set_duration(note_information.text)
                                elif tag_checker(note_information, 'noteNum'):
                                    note_data.note_number = note_information.text
                                elif tag_checker(note_information, 'lyric'):
                                    # from romkan import to_hiragana
                                    # lyric = note_information.text
                                    # note_data.lyric = to_hiragana(lyric) if is_hiragana else lyric
                                    note_data.lyric = note_information.text

                            note_list.append(note_data)

                    if any(track_list[track_number].note):
                        track_list[track_number].note.extend(note_list.copy())
                    else:
                        track_list[track_number].note = note_list.copy()

    make_ccs(save_file_path, track_list, bpm_list, beat_list)
