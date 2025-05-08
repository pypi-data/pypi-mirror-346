from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTAttributeColumnTypes(
    EaTColumnTypes
):
    T_ATTRIBUTE_EA_GUIDS = auto()
    T_ATTRIBUTE_OBJECT_IDS = auto()
    T_ATTRIBUTE_NAMES = auto()
    T_ATTRIBUTE_SCOPES = auto()
    T_ATTRIBUTE_STEREOTYPES = auto()
    T_ATTRIBUTE_NOTES = auto()
    T_ATTRIBUTE_IDS = auto()
    T_ATTRIBUTE_POSITIONS = auto()
    T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS = (
        auto()
    )
    T_ATTRIBUTE_DEFAULTS = auto()
    T_ATTRIBUTE_TYPES = auto()
    T_ATTRIBUTE_STYLE_EXS = auto()
    T_ATTRIBUTE_LOWER_BOUNDS = auto()
    T_ATTRIBUTE_UPPER_BOUNDS = auto()

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
    EaTAttributeColumnTypes.T_ATTRIBUTE_OBJECT_IDS: "Object_ID",
    EaTAttributeColumnTypes.T_ATTRIBUTE_NAMES: "Name",
    EaTAttributeColumnTypes.T_ATTRIBUTE_SCOPES: "Scope",
    EaTAttributeColumnTypes.T_ATTRIBUTE_STEREOTYPES: "Stereotype",
    EaTAttributeColumnTypes.T_ATTRIBUTE_NOTES: "Notes",
    EaTAttributeColumnTypes.T_ATTRIBUTE_IDS: "ID",
    EaTAttributeColumnTypes.T_ATTRIBUTE_POSITIONS: "Pos",
    EaTAttributeColumnTypes.T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS: "Classifier",
    EaTAttributeColumnTypes.T_ATTRIBUTE_DEFAULTS: "Default",
    EaTAttributeColumnTypes.T_ATTRIBUTE_TYPES: "Type",
    EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS: "ea_guid",
    EaTAttributeColumnTypes.T_ATTRIBUTE_STYLE_EXS: "StyleEx",
    EaTAttributeColumnTypes.T_ATTRIBUTE_LOWER_BOUNDS: "LowerBound",
    EaTAttributeColumnTypes.T_ATTRIBUTE_UPPER_BOUNDS: "UpperBound",
}


nf_column_name_mapping = {
    EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS: "t_attribute_ea_guids",
    EaTAttributeColumnTypes.T_ATTRIBUTE_OBJECT_IDS: "t_attribute_object_ids",
    EaTAttributeColumnTypes.T_ATTRIBUTE_NAMES: "t_attribute_names",
    EaTAttributeColumnTypes.T_ATTRIBUTE_SCOPES: "t_attribute_scopes",
    EaTAttributeColumnTypes.T_ATTRIBUTE_STEREOTYPES: "t_attribute_stereotypes",
    EaTAttributeColumnTypes.T_ATTRIBUTE_NOTES: "t_attribute_notes",
    EaTAttributeColumnTypes.T_ATTRIBUTE_IDS: "t_attribute_ids",
    EaTAttributeColumnTypes.T_ATTRIBUTE_POSITIONS: "t_attribute_positions",
    EaTAttributeColumnTypes.T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS: "t_attribute_classifier_t_object_ids",
    EaTAttributeColumnTypes.T_ATTRIBUTE_DEFAULTS: "t_attribute_defaults",
    EaTAttributeColumnTypes.T_ATTRIBUTE_TYPES: "t_attribute_types",
    EaTAttributeColumnTypes.T_ATTRIBUTE_STYLE_EXS: "t_attribute_style_exs",
    EaTAttributeColumnTypes.T_ATTRIBUTE_LOWER_BOUNDS: "t_attribute_lower_bounds",
    EaTAttributeColumnTypes.T_ATTRIBUTE_UPPER_BOUNDS: "t_attribute_upper_bounds",
}
