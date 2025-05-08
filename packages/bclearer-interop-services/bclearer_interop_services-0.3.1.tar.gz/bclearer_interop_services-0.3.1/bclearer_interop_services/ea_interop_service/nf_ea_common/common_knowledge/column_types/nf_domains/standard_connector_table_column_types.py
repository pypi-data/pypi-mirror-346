from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)


@unique
class StandardConnectorTableColumnTypes(
    ColumnTypes
):
    NF_UUIDS = auto()
    CONNECTOR_UML_NAMES = auto()
    CONNECTOR_UML_TYPE_IDENTIFIERS = (
        auto()
    )
    SUPPLIER_PLACE_1_NF_UUIDS = auto()
    SUPPLIER_PLACE_1_UML_NAMES = auto()
    CLIENT_PLACE_2_NF_UUIDS = auto()
    CLIENT_PLACE_2_UML_NAMES = auto()
    STEREOTYPE_NF_UUIDS = auto()
    STEREOTYPE_UML_NAMES = auto()
    CONNECTOR_NOTES = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    StandardConnectorTableColumnTypes.NF_UUIDS: NfColumnTypes.NF_UUIDS.column_name,
    StandardConnectorTableColumnTypes.CONNECTOR_UML_NAMES: "connector_uml_names",
    StandardConnectorTableColumnTypes.CONNECTOR_UML_TYPE_IDENTIFIERS: "connector_uml_type_identifiers",
    StandardConnectorTableColumnTypes.SUPPLIER_PLACE_1_NF_UUIDS: "supplier_place1_nf_uuids",
    StandardConnectorTableColumnTypes.SUPPLIER_PLACE_1_UML_NAMES: "supplier_place1_uml_names",
    StandardConnectorTableColumnTypes.CLIENT_PLACE_2_NF_UUIDS: "client_place2_nf_uuids",
    StandardConnectorTableColumnTypes.CLIENT_PLACE_2_UML_NAMES: "client_place2_uml_names",
    StandardConnectorTableColumnTypes.STEREOTYPE_NF_UUIDS: "stereotype_nf_uuids",
    StandardConnectorTableColumnTypes.STEREOTYPE_UML_NAMES: "stereotype_uml_names",
    StandardConnectorTableColumnTypes.CONNECTOR_NOTES: "connector_notes",
}
