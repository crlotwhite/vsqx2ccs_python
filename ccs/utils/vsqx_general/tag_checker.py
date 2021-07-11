import xml.etree.ElementTree as ET

from ccs.utils.file_type import FileTypes
from ccs.utils.vsqx_general.get_vocaloid_schema import get_vocaloid_schema


def tag_checker(file_type: FileTypes, element: ET.Element, tag_str: str) -> bool:
    def make_tag(raw_tag):
        schema_string = get_vocaloid_schema(file_type)
        return f'{schema_string}{raw_tag}'

    return element.tag == make_tag(tag_str)
