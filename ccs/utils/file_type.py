from enum import Flag, auto


class FileTypes(Flag):
    V2 = auto()
    V3 = auto()
    V4 = auto()
    UST = auto()
    SVP = auto()
