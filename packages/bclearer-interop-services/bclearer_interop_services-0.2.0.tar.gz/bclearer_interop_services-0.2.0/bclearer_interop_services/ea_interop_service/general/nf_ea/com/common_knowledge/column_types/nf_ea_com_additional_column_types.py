from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class NfEaComAdditionalColumnTypes(
    ColumnTypes
):
    ORIGINAL_EA_GUIDS = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    NfEaComAdditionalColumnTypes.ORIGINAL_EA_GUIDS: "original_ea_guids",
}
