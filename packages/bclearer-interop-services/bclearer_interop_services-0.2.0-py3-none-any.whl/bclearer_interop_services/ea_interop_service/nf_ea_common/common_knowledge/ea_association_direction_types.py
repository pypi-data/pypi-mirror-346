from enum import Enum, auto, unique


@unique
class EaAssociationDirectionTypes(Enum):
    NOT_SET = auto()
    FORWARD = auto()
    BACKWARD = auto()
