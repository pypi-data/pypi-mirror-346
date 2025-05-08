from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTDiagramTypesColumnTypes(
    EaTColumnTypes
):
    T_DIAGRAMTYPES_DIAGRAM_TYPES = (
        auto()
    )
    T_DIAGRAMTYPES_NAMES = auto()
    T_DIAGRAMTYPES_PACKAGE_IDS = auto()

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
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_DIAGRAM_TYPES: "Diagram_Type",
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_NAMES: "Name",
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_PACKAGE_IDS: "Package_ID",
}


nf_column_name_mapping = {
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_DIAGRAM_TYPES: "t_diagramtypes_diagram_types",
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_NAMES: "t_diagramtypes_names",
    EaTDiagramTypesColumnTypes.T_DIAGRAMTYPES_PACKAGE_IDS: "t_diagramtypes_package_ids",
}
