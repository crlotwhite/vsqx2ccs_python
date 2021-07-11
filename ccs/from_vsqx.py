from typing import List
from os.path import join

from ccs.models.beat_data import BeatData
from ccs.models.bpm_data import BpmData
from ccs.models.note_data import NoteData
from ccs.models.track_data import TrackData
from ccs.utils.track_container import TrackContainer

from ccs.make_ccs import make_ccs
from ccs.utils.vsqx_general.get_tag_dictionary import get_tag_dictionary
from ccs.utils.vsqx_general.get_vocaloid_generation import get_vocaloid_generation
from ccs.utils.vsqx_general.tag_checker import tag_checker

from vsqx2ccs.settings import MEDIA_ROOT


def from_vsqx(file_name: str, tree, is_hiragana) -> bool:
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
    file_type = get_vocaloid_generation(root)
    tag_dict = get_tag_dictionary(file_type)

    # parse loop
    for child in root:
        # get track information
        if tag_checker(file_type, child, tag_dict['mixer']):
            for unit in child:
                if tag_checker(file_type, unit, tag_dict['vs_unit']):
                    track_data = TrackData()
                    for unit_data in unit:
                        if tag_checker(file_type, unit_data, tag_dict['vs_track_no']):
                            track_data.track_number = int(unit_data.text)
                        elif tag_checker(file_type, unit_data, tag_dict['mute']):
                            track_data.mute = int(unit_data.text)
                        elif tag_checker(file_type, unit_data, tag_dict['solo']):
                            track_data.solo = int(unit_data.text)

                    track_list.append(track_data)

        # get beat and tempo data
        elif tag_checker(file_type, child, tag_dict['master_track']):
            for master_track_data in child:
                # is beat data
                if tag_checker(file_type, master_track_data, tag_dict['time_signal']):
                    beat_data = BeatData()
                    for data in master_track_data:
                        if tag_checker(file_type, data, tag_dict['pos_mes']):
                            beat_data.tempo_change_point = data.text
                        elif tag_checker(file_type, data, tag_dict['numerator']):
                            beat_data.numerator = data.text
                        elif tag_checker(file_type, data, tag_dict['denominator']):
                            beat_data.denominator = data.text
                    beat_list.append(beat_data)

                # is tempo data
                elif tag_checker(file_type, master_track_data, tag_dict['tempo']):
                    bpm_data = BpmData()
                    for data in master_track_data:
                        if tag_checker(file_type, data, tag_dict['position_tick']):
                            bpm_data.clock = data.text
                        elif tag_checker(file_type, data, tag_dict['bpm']):
                            tempo_str = data.text
                            bpm_data.tempo = tempo_str
                            if len(tempo_str) > 4:
                                bpm_data.integer_point = tempo_str[:3]
                                bpm_data.decimal_point = tempo_str[3:]
                            else:
                                bpm_data.integer_point = tempo_str[:2]
                                bpm_data.decimal_point = tempo_str[2:]

                    bpm_list.append(bpm_data)

        elif tag_checker(file_type, child, tag_dict['vs_track']):
            track_number = 0
            for track_information in child:
                if tag_checker(file_type, track_information, tag_dict['vs_track_no']):
                    track_number = int(track_information.text)
                elif tag_checker(file_type, track_information, tag_dict['track_name']):
                    track_list[track_number].track_name = track_information.text
                # get note data with playTime
                elif tag_checker(file_type, track_information, tag_dict['musical_part']):
                    play_time = ""
                    note_list = []
                    part_posTick = 0
                    for musical_part_data in track_information:
                        if tag_checker(file_type, musical_part_data, tag_dict['play_time']):
                            play_time = musical_part_data.text
                        elif tag_checker(file_type, musical_part_data, tag_dict['position_tick']):
                            part_posTick = int(musical_part_data.text)

                        # get data for NoteData
                        elif tag_checker(file_type, musical_part_data, tag_dict['note']):
                            # from this, a note will be created and added.
                            note_data = NoteData()
                            note_data.play_time = play_time
                            for note_information in musical_part_data:
                                if tag_checker(file_type, note_information, tag_dict['position_tick']):
                                    # The note tag records the position relative to the part position.
                                    note_tick = part_posTick + int(note_information.text)
                                    note_data.set_begin_tick(note_tick)
                                elif tag_checker(file_type, note_information, tag_dict['duration_tick']):
                                    note_data.set_duration(note_information.text)
                                elif tag_checker(file_type, note_information, tag_dict['note_number']):
                                    note_data.note_number = note_information.text
                                elif tag_checker(file_type, note_information, tag_dict['lyric']):
                                    from romkan import to_hiragana
                                    lyric = note_information.text
                                    note_data.lyric = to_hiragana(lyric) if is_hiragana else lyric

                            note_list.append(note_data)

                    if any(track_list[track_number].note):
                        track_list[track_number].note.extend(note_list.copy())
                    else:
                        track_list[track_number].note = note_list.copy()

    make_ccs(save_file_path, track_list, bpm_list, beat_list)
