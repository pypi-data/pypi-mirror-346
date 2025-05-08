from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)


@unique
class ExtendedTObjectColumnTypes(
    ColumnTypes
):
    T_OBJECT_PATHS = auto()
    T_XREF_DESCRIPTIONS = auto()
    LIST_OF_STEREOTYPE_GUIDS = auto()
    T_OBJECT_EA_HUMAN_READABLE_NAMES = (
        auto()
    )

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    ExtendedTObjectColumnTypes.T_OBJECT_PATHS: "t_object_paths",
    ExtendedTObjectColumnTypes.T_XREF_DESCRIPTIONS: EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name,
    ExtendedTObjectColumnTypes.LIST_OF_STEREOTYPE_GUIDS: "list_of_stereotype_guids",
    ExtendedTObjectColumnTypes.T_OBJECT_EA_HUMAN_READABLE_NAMES: "t_object_ea_human_readable_names",
}
