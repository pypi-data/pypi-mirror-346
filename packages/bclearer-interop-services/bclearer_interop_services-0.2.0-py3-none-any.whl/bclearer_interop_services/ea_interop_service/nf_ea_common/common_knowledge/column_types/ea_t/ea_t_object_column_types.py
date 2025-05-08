from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTObjectColumnTypes(
    EaTColumnTypes
):
    T_OBJECT_IDS = auto()
    T_OBJECT_TYPES = auto()
    T_OBJECT_NAMES = auto()
    T_OBJECT_ALIASES = auto()
    T_OBJECT_AUTHORS = auto()
    T_OBJECT_VERSIONS = auto()
    T_OBJECT_NOTES = auto()
    T_OBJECT_PACKAGE_IDS = auto()
    T_OBJECT_STEREOTYPES = auto()
    T_OBJECT_STYLES = auto()
    T_OBJECT_BACKCOLORS = auto()
    T_OBJECT_BORDER_WIDTHS = auto()
    T_OBJECT_FONT_COLORS = auto()
    T_OBJECT_BORDER_COLORS = auto()
    T_OBJECT_BORDER_STYLES = auto()
    T_OBJECT_CREATED_DATES = auto()
    T_OBJECT_MODIFIED_DATES = auto()
    T_OBJECT_CARDINALITIES = auto()
    T_OBJECT_PDATA1 = auto()
    T_OBJECT_GEN_TYPES = auto()
    T_OBJECT_PHASES = auto()
    T_OBJECT_SCOPES = auto()
    T_OBJECT_CLASSIFIERS = auto()
    T_OBJECT_EA_GUIDS = auto()
    T_OBJECT_PARENT_IDS = auto()
    T_OBJECT_CLASSIFIER_GUIDS = auto()
    T_OBJECT_MULTIPLICITIES = auto()
    T_OBJECT_STYLE_EXS = auto()
    T_OBJECT_STATUS = auto()

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
    EaTObjectColumnTypes.T_OBJECT_IDS: "Object_ID",
    EaTObjectColumnTypes.T_OBJECT_TYPES: "Object_Type",
    EaTObjectColumnTypes.T_OBJECT_NAMES: "Name",
    EaTObjectColumnTypes.T_OBJECT_ALIASES: "Alias",
    EaTObjectColumnTypes.T_OBJECT_AUTHORS: "Author",
    EaTObjectColumnTypes.T_OBJECT_VERSIONS: "Version",
    EaTObjectColumnTypes.T_OBJECT_NOTES: "Note",
    EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS: "Package_ID",
    EaTObjectColumnTypes.T_OBJECT_STEREOTYPES: "Stereotype",
    EaTObjectColumnTypes.T_OBJECT_STYLES: "Style",
    EaTObjectColumnTypes.T_OBJECT_BACKCOLORS: "Backcolor",
    EaTObjectColumnTypes.T_OBJECT_BORDER_WIDTHS: "BorderWidth",
    EaTObjectColumnTypes.T_OBJECT_FONT_COLORS: "Fontcolor",
    EaTObjectColumnTypes.T_OBJECT_BORDER_COLORS: "Bordercolor",
    EaTObjectColumnTypes.T_OBJECT_BORDER_STYLES: "BorderStyle",
    EaTObjectColumnTypes.T_OBJECT_CREATED_DATES: "CreatedDate",
    EaTObjectColumnTypes.T_OBJECT_MODIFIED_DATES: "ModifiedDate",
    EaTObjectColumnTypes.T_OBJECT_CARDINALITIES: "Cardinality",
    EaTObjectColumnTypes.T_OBJECT_PDATA1: "PDATA1",
    EaTObjectColumnTypes.T_OBJECT_GEN_TYPES: "GenType",
    EaTObjectColumnTypes.T_OBJECT_PHASES: "Phase",
    EaTObjectColumnTypes.T_OBJECT_SCOPES: "Scope",
    EaTObjectColumnTypes.T_OBJECT_CLASSIFIERS: "Classifier",
    EaTObjectColumnTypes.T_OBJECT_EA_GUIDS: "ea_guid",
    EaTObjectColumnTypes.T_OBJECT_PARENT_IDS: "ParentID",
    EaTObjectColumnTypes.T_OBJECT_CLASSIFIER_GUIDS: "Classifier_guid",
    EaTObjectColumnTypes.T_OBJECT_MULTIPLICITIES: "Multiplicity",
    EaTObjectColumnTypes.T_OBJECT_STYLE_EXS: "StyleEx",
    EaTObjectColumnTypes.T_OBJECT_STATUS: "Status",
}


nf_column_name_mapping = {
    EaTObjectColumnTypes.T_OBJECT_IDS: "t_object_ids",
    EaTObjectColumnTypes.T_OBJECT_TYPES: "t_object_types",
    EaTObjectColumnTypes.T_OBJECT_NAMES: "t_object_names",
    EaTObjectColumnTypes.T_OBJECT_ALIASES: "t_object_aliases",
    EaTObjectColumnTypes.T_OBJECT_AUTHORS: "t_object_authors",
    EaTObjectColumnTypes.T_OBJECT_VERSIONS: "t_object_versions",
    EaTObjectColumnTypes.T_OBJECT_NOTES: "t_object_notes",
    EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS: "t_object_package_ids",
    EaTObjectColumnTypes.T_OBJECT_STEREOTYPES: "t_object_stereotypes",
    EaTObjectColumnTypes.T_OBJECT_STYLES: "t_object_styles",
    EaTObjectColumnTypes.T_OBJECT_BACKCOLORS: "t_object_backcolors",
    EaTObjectColumnTypes.T_OBJECT_BORDER_WIDTHS: "t_object_border_widths",
    EaTObjectColumnTypes.T_OBJECT_FONT_COLORS: "t_object_font_colors",
    EaTObjectColumnTypes.T_OBJECT_BORDER_COLORS: "t_object_border_colors",
    EaTObjectColumnTypes.T_OBJECT_BORDER_STYLES: "t_object_border_styles",
    EaTObjectColumnTypes.T_OBJECT_CREATED_DATES: "t_object_created_dates",
    EaTObjectColumnTypes.T_OBJECT_MODIFIED_DATES: "t_object_modified_dates",
    EaTObjectColumnTypes.T_OBJECT_CARDINALITIES: "t_object_cardinalities",
    EaTObjectColumnTypes.T_OBJECT_PDATA1: "t_object_pdata1",
    EaTObjectColumnTypes.T_OBJECT_GEN_TYPES: "t_object_gen_types",
    EaTObjectColumnTypes.T_OBJECT_PHASES: "t_object_phases",
    EaTObjectColumnTypes.T_OBJECT_SCOPES: "t_object_scopes",
    EaTObjectColumnTypes.T_OBJECT_CLASSIFIERS: "t_object_classifiers",
    EaTObjectColumnTypes.T_OBJECT_EA_GUIDS: "t_object_ea_guids",
    EaTObjectColumnTypes.T_OBJECT_PARENT_IDS: "t_object_parent_ids",
    EaTObjectColumnTypes.T_OBJECT_CLASSIFIER_GUIDS: "t_object_classifier_guids",
    EaTObjectColumnTypes.T_OBJECT_MULTIPLICITIES: "t_object_multiplicities",
    EaTObjectColumnTypes.T_OBJECT_STYLE_EXS: "t_object_style_exs",
    EaTObjectColumnTypes.T_OBJECT_STATUS: "t_object_status",
}
