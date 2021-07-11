import xml.etree.ElementTree as ET
from typing import Optional

from ccs.utils.file_type import FileTypes


def get_vocaloid_generation(root: ET.Element) -> Optional[FileTypes]:
    raw_tag = root.tag.split('}')[1]

    if raw_tag == 'vsq3':
        return FileTypes.V3
    elif raw_tag == 'vsq4':
        return FileTypes.V4
    else:
        return None
