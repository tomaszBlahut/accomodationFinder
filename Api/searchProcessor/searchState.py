from enum import Enum


class SearchState(Enum):
    NEW = 1,
    PROCESSING = 2,
    COMPLETED = 3,
    FAILED = 4
