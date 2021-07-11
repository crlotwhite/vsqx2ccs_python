from typing import Any, Dict, Optional

from ccs.utils.file_type import FileTypes
from ccs.utils.v3.tag_dictionary import tag_dictionary as v3_tags
from ccs.utils.v4.tag_dictionary import tag_dictionary as v4_tags


def get_tag_dictionary(file_type: FileTypes) -> Optional[Dict[str, Any]]:
    if file_type == FileTypes.V3:
        return v3_tags
    elif file_type == FileTypes.V4:
        return v4_tags
    else:
        return None
