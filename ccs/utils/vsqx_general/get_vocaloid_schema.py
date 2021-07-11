from typing import Optional

from ccs.utils.file_type import FileTypes


def get_vocaloid_schema(file_type: FileTypes) -> Optional[str]:
    if file_type == FileTypes.V3:
        return '{http://www.yamaha.co.jp/vocaloid/schema/vsq3/}'
    elif file_type == FileTypes.V4:
        return '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}'
    else:
        return None
