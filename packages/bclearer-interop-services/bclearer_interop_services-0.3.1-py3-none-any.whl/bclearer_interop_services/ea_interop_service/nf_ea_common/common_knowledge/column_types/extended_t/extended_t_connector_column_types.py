from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)


@unique
class ExtendedTConnectorColumnTypes(
    ColumnTypes
):
    START_T_OBJECT_EA_GUIDS = auto()
    START_T_OBJECT_NAMES = auto()
    END_T_OBJECT_EA_GUIDS = auto()
    END_T_OBJECT_NAMES = auto()
    T_XREF_DESCRIPTIONS = auto()
    LIST_OF_STEREOTYPE_GUIDS = auto()
    T_CONNECTOR_EA_HUMAN_READABLE_NAMES = (
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
    ExtendedTConnectorColumnTypes.START_T_OBJECT_EA_GUIDS: "start_t_object_ea_guids",
    ExtendedTConnectorColumnTypes.START_T_OBJECT_NAMES: "start_t_object_names",
    ExtendedTConnectorColumnTypes.END_T_OBJECT_EA_GUIDS: "end_t_object_ea_guids",
    ExtendedTConnectorColumnTypes.END_T_OBJECT_NAMES: "end_t_object_names",
    ExtendedTConnectorColumnTypes.T_XREF_DESCRIPTIONS: EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name,
    ExtendedTConnectorColumnTypes.LIST_OF_STEREOTYPE_GUIDS: "list_of_stereotype_guids",
    ExtendedTConnectorColumnTypes.T_CONNECTOR_EA_HUMAN_READABLE_NAMES: "t_connector_ea_human_readable_names",
}
