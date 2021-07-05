import xml.etree.ElementTree as ET

from ccs.models.base_tick import BaseTick
from ccs.utils.xml_indent import xml_indent


def make_ccs(save_file_name, track_list, bpm_list, beat_list):
    # create ccs file
    deff = BaseTick()
    ccs_root = ET.Element('Scenario', Code=deff.ccs_code)

    # create sequence
    ccs_sequence = ET.Element('Sequence', Id='')
    ccs_root.append(ccs_sequence)

    # create scene
    ccs_scene = ET.Element('Scene', Id='')
    ccs_sequence.append(ccs_scene)

    # create collections
    ccs_units = ET.SubElement(ccs_scene, 'Units')
    ccs_groups = ET.SubElement(ccs_scene, 'Groups')

    # create sound setting
    ccs_sound_setting = ET.Element('SoundSetting', Rhythm='4/4', Tempo='78')
    ccs_scene.append(ccs_sound_setting)

    # create track data
    for track in track_list:
        ccs_unit_attributes = {
            'Version': '1.0',
            'Id': '',
            'Category': 'SingerSong',
            'Group': track.track_guid,
            'StartTime': '00:00:00',
            'Duration': '10:00:00'
        }
        ccs_unit = ET.SubElement(ccs_units, 'Unit', attrib=ccs_unit_attributes)

        # create song
        ccs_song = ET.SubElement(ccs_unit, 'Song', attrib={'Version': '1.07'})

        # create tempo
        ccs_tempo = ET.SubElement(ccs_song, 'Tempo')
        for bpm_data in bpm_list:
            ccs_sound_attribute = {
                'Clock': '0', # bpm_data.clock,
                'Tempo': bpm_data.integer_point
            }
            ET.SubElement(ccs_tempo, 'Sound', attrib=ccs_sound_attribute)

        # create beat
        ccs_beat = ET.SubElement(ccs_song, 'Beat')
        for beat_data in beat_list:
            ccs_time_attribute = {
                'Clock': str(beat_data.tempo_change_point),
                'Beats': beat_data.numerator,
                'BeatType': beat_data.denominator
            }
            ET.SubElement(ccs_beat, 'Time', attrib=ccs_time_attribute)

        # create score
        ccs_score = ET.SubElement(ccs_song, 'Score')

        # create key
        ccs_key_attribute = {
            'Clock': '0',
            'Fifths': '0',
            'Mode': '0'
        }
        ET.SubElement(ccs_score, 'Key', attrib=ccs_key_attribute)

        # create note
        for note_data in track.note:
            ccs_note_attribute = {
                'Clock': note_data.clock,
                'PitchStep': note_data.pitch_step,
                'PitchOctave': note_data.pitch_octave,
                'Duration': note_data.duration,
                'Lyric': note_data.lyric
            }
            ET.SubElement(ccs_score, 'Note', attrib=ccs_note_attribute)

    # create group
    for track in track_list:
        ccs_group_attribute = {
            'Version': '1.0',
            'Id': track.track_guid,
            'Category': 'SingerSong',
            'Name': track.track_name,
            'Color': '#FFFF0000',
            'Volume': '0',
            'Pan': '0',
            'IsSolo': str(track.solo),
            'IsMuted': str(track.mute)
        }
        ET.SubElement(ccs_groups, 'Group', attrib=ccs_group_attribute)

    xml_indent(ccs_root)
    ET.dump(ccs_root)
    ET.ElementTree(ccs_root).write(save_file_name, encoding='utf-8', xml_declaration=True)
