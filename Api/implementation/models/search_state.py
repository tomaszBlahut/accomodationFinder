from enum import IntEnum


class SearchState(IntEnum):
    NEW = 1,
    PROCESSING = 2,
    COMPLETED = 3,
    FAILED = 4
