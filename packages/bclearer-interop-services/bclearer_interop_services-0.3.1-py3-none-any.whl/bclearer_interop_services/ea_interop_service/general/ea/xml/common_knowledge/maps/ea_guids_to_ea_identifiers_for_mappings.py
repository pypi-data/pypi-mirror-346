from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)


class EaGuidsToEaIdentifiersMappings:
    def __init__(self):
        self.__map = dict()

    def add_single_map(
        self,
        ea_identifier: int,
        ea_guid: str,
    ):
        self.__map.update(
            {ea_guid: ea_identifier}
        )

    def set_map(
        self, map_to_be_set: dict
    ):
        self.__map.update(map_to_be_set)

    def get_ea_identifier(
        self, ea_guid: str
    ) -> int:
        if (
            ea_guid
            not in self.__map.keys()
        ):
            return DEFAULT_NULL_VALUE

        ea_identifier = self.__map[
            ea_guid
        ]

        return ea_identifier

    def get_ea_guid(
        self, ea_identifier: int
    ) -> str:
        for (
            ea_guid,
            value,
        ) in self.__map.items():
            if ea_identifier == value:
                return ea_guid

        print(
            "ea_guid does not exist for "
            + str(ea_identifier)
        )

        return ""

    def get_map(self):
        return self.__map
