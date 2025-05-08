from enum import Enum, auto, unique


@unique
class IDualRepositoryCreationResultTypes(
    Enum
):
    SUCCEEDED = auto()

    FAILED_TO_OPEN_EA = auto()

    FAILED_TO_OPEN_EA_PROJECT = auto()
