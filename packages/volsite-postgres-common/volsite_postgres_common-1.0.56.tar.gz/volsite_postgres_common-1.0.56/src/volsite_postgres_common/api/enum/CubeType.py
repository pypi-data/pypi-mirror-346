from enum import IntEnum
from db.E import E
from volsite_postgres_common.api.enum.enum import create_enum_type


class CubeType(IntEnum):

    R = 12,
    G = 13,
    B = 14,
    Y = 15,
    V = 16,


