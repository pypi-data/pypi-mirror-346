from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTXrefColumnTypes(
    EaTColumnTypes
):
    T_XREF_EA_GUIDS = auto()
    T_XREF_NAMES = auto()
    T_XREF_TYPES = auto()
    T_XREF_DESCRIPTIONS = auto()
    T_XREF_CLIENT_EA_GUIDS = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    def __nf_column_name(self) -> str:
        nf_column_name = (
            nf_column_name_mapping[self]
        )

        return nf_column_name

    column_name = property(
        fget=__column_name
    )

    nf_column_name = property(
        fget=__nf_column_name
    )


column_name_mapping = {
    EaTXrefColumnTypes.T_XREF_EA_GUIDS: "XrefID",
    EaTXrefColumnTypes.T_XREF_NAMES: "Name",
    EaTXrefColumnTypes.T_XREF_TYPES: "Type",
    EaTXrefColumnTypes.T_XREF_DESCRIPTIONS: "Description",
    EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS: "Client",
}


nf_column_name_mapping = {
    EaTXrefColumnTypes.T_XREF_EA_GUIDS: "t_xref_ea_guids",
    EaTXrefColumnTypes.T_XREF_NAMES: "t_xref_names",
    EaTXrefColumnTypes.T_XREF_TYPES: "t_xref_types",
    EaTXrefColumnTypes.T_XREF_DESCRIPTIONS: "t_xref_descriptions",
    EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS: "t_xref_client_ea_guids",
}
