from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class StandardAttributeTableColumnTypes(
    ColumnTypes
):
    ATTRIBUTED_OBJECT_UUIDS = auto()
    ATTRIBUTE_TYPE_UUIDS = auto()
    UML_VISIBILITY_KIND = auto()
    ATTRIBUTE_VALUES = auto()
    ATTRIBUTED_OBJECT_NAMES = auto()
    ATTRIBUTE_TYPE_NAMES = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    StandardAttributeTableColumnTypes.ATTRIBUTED_OBJECT_UUIDS: "attributed_object_uuids",
    StandardAttributeTableColumnTypes.ATTRIBUTE_TYPE_UUIDS: "attribute_type_uuids",
    StandardAttributeTableColumnTypes.UML_VISIBILITY_KIND: "uml_visibility_kind",
    StandardAttributeTableColumnTypes.ATTRIBUTE_VALUES: "attribute_values",
    StandardAttributeTableColumnTypes.ATTRIBUTED_OBJECT_NAMES: "attributed_object_names",
    StandardAttributeTableColumnTypes.ATTRIBUTE_TYPE_NAMES: "attribute_type_names",
}
