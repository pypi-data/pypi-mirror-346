from enum import Enum, auto


class TableBDictionaryReturnTypes(Enum):
    NOT_SET = auto()

    ROW_ALREADY_EXISTS = auto()

    ROW_ADDED = auto()
