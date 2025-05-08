from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTDiagramColumnTypes(
    EaTColumnTypes
):
    T_DIAGRAM_IDS = auto()
    T_DIAGRAM_NAMES = auto()
    T_DIAGRAM_EA_GUIDS = auto()
    T_DIAGRAM_TYPES = auto()
    T_DIAGRAM_PACKAGE_IDS = auto()
    T_DIAGRAM_PARENT_IDS = auto()
    T_DIAGRAM_VERSIONS = auto()
    T_DIAGRAM_AUTHORS = auto()
    T_DIAGRAM_NOTES = auto()
    T_DIAGRAM_STEREOTYPES = auto()
    T_DIAGRAM_ORIENTATIONS = auto()
    T_DIAGRAM_SCALES = auto()
    T_DIAGRAM_CREATED_DATES = auto()
    T_DIAGRAM_MODIFIED_DATES = auto()
    T_DIAGRAM_HTML_PATHS = auto()
    T_DIAGRAM_LOCKED = auto()

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
    EaTDiagramColumnTypes.T_DIAGRAM_IDS: "Diagram_ID",
    EaTDiagramColumnTypes.T_DIAGRAM_NAMES: "Name",
    EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS: "ea_guid",
    EaTDiagramColumnTypes.T_DIAGRAM_TYPES: "Diagram_Type",
    EaTDiagramColumnTypes.T_DIAGRAM_PACKAGE_IDS: "Package_ID",
    EaTDiagramColumnTypes.T_DIAGRAM_PARENT_IDS: "ParentID",
    EaTDiagramColumnTypes.T_DIAGRAM_VERSIONS: "Version",
    EaTDiagramColumnTypes.T_DIAGRAM_AUTHORS: "Author",
    EaTDiagramColumnTypes.T_DIAGRAM_NOTES: "Notes",
    EaTDiagramColumnTypes.T_DIAGRAM_STEREOTYPES: "Stereotype",
    EaTDiagramColumnTypes.T_DIAGRAM_ORIENTATIONS: "Orientation",
    EaTDiagramColumnTypes.T_DIAGRAM_SCALES: "Scale",
    EaTDiagramColumnTypes.T_DIAGRAM_CREATED_DATES: "CreatedDate",
    EaTDiagramColumnTypes.T_DIAGRAM_MODIFIED_DATES: "ModifiedDate",
    EaTDiagramColumnTypes.T_DIAGRAM_HTML_PATHS: "HTMLPath",
    EaTDiagramColumnTypes.T_DIAGRAM_LOCKED: "Locked",
}


nf_column_name_mapping = {
    EaTDiagramColumnTypes.T_DIAGRAM_IDS: "t_diagram_ids",
    EaTDiagramColumnTypes.T_DIAGRAM_NAMES: "t_diagram_names",
    EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS: "t_diagram_ea_guids",
    EaTDiagramColumnTypes.T_DIAGRAM_TYPES: "t_diagram_types",
    EaTDiagramColumnTypes.T_DIAGRAM_PACKAGE_IDS: "t_diagram_package_ids",
    EaTDiagramColumnTypes.T_DIAGRAM_PARENT_IDS: "t_diagram_parent_ids",
    EaTDiagramColumnTypes.T_DIAGRAM_VERSIONS: "t_diagram_versions",
    EaTDiagramColumnTypes.T_DIAGRAM_AUTHORS: "t_diagram_authors",
    EaTDiagramColumnTypes.T_DIAGRAM_NOTES: "t_diagram_notes",
    EaTDiagramColumnTypes.T_DIAGRAM_STEREOTYPES: "t_diagram_stereotypes",
    EaTDiagramColumnTypes.T_DIAGRAM_ORIENTATIONS: "t_diagram_orientations",
    EaTDiagramColumnTypes.T_DIAGRAM_SCALES: "t_diagram_scales",
    EaTDiagramColumnTypes.T_DIAGRAM_CREATED_DATES: "t_diagram_created_dates",
    EaTDiagramColumnTypes.T_DIAGRAM_MODIFIED_DATES: "t_diagram_modified_dates",
    EaTDiagramColumnTypes.T_DIAGRAM_HTML_PATHS: "t_diagram_html_paths",
    EaTDiagramColumnTypes.T_DIAGRAM_LOCKED: "t_diagram_locked",
}
