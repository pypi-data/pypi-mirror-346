from enum import Enum, auto


class BDictionaryReturnTypes(Enum):
    NOT_SET = auto()

    KEY_ALREADY_EXISTS = auto()

    VALUE_ADDED = auto()
