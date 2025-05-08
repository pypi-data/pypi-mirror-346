from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)


@unique
class StandardObjectTableColumnTypes(
    ColumnTypes
):
    NF_UUIDS = auto()
    UML_OBJECT_NAMES = auto()
    PARENT_PACKAGE_NF_UUIDS = auto()
    PARENT_PACKAGE_UML_NAMES = auto()
    OBJECT_UML_TYPE_IDENTIFIERS = auto()
    OBJECT_CLASSIFIER_NF_UUIDS = auto()
    STEREOTYPE_GROUP_NF_UUIDS = auto()
    STEREOTYPE_NF_UUIDS = auto()
    STEREOTYPE_EA_GUIDS = auto()
    CLIENT_NF_UUIDS = auto()
    CLIENT_EA_GUIDS = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    StandardObjectTableColumnTypes.NF_UUIDS: NfColumnTypes.NF_UUIDS.column_name,
    StandardObjectTableColumnTypes.UML_OBJECT_NAMES: "uml_object_names",
    StandardObjectTableColumnTypes.PARENT_PACKAGE_NF_UUIDS: "parent_package_nf_uuids",
    StandardObjectTableColumnTypes.PARENT_PACKAGE_UML_NAMES: "parent_package_uml_names",
    StandardObjectTableColumnTypes.OBJECT_UML_TYPE_IDENTIFIERS: "object_uml_type_identifiers",
    StandardObjectTableColumnTypes.OBJECT_CLASSIFIER_NF_UUIDS: "object_classifier_nf_uuids",
    StandardObjectTableColumnTypes.STEREOTYPE_GROUP_NF_UUIDS: "stereotype_group_nf_uuids",
    StandardObjectTableColumnTypes.STEREOTYPE_NF_UUIDS: "stereotype_nf_uuids",
    StandardObjectTableColumnTypes.STEREOTYPE_EA_GUIDS: "stereotype_ea_guids",
    StandardObjectTableColumnTypes.CLIENT_NF_UUIDS: "client_nf_uuids",
    StandardObjectTableColumnTypes.CLIENT_EA_GUIDS: "client_ea_guids",
}
