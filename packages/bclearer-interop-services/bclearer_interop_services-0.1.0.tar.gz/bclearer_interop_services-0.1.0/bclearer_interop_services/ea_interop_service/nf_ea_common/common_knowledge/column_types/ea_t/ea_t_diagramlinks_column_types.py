from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTDiagramlinksColumnTypes(
    EaTColumnTypes
):
    T_DIAGRAMLINKS_DIAGRAM_IDS = auto()
    T_DIAGRAMLINKS_CONNECTOR_IDS = (
        auto()
    )
    T_DIAGRAMLINKS_GEOMETRIES = auto()
    T_DIAGRAMLINKS_STYLES = auto()
    T_DIAGRAMLINKS_HIDDEN = auto()
    T_DIAGRAMLINKS_PATHS = auto()
    T_DIAGRAMLINKS_INSTANCE_IDS = auto()

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
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_DIAGRAM_IDS: "DiagramID",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_CONNECTOR_IDS: "ConnectorID",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_GEOMETRIES: "Geometry",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_STYLES: "Style",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_HIDDEN: "Hidden",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_PATHS: "Path",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_INSTANCE_IDS: "Instance_ID",
}


nf_column_name_mapping = {
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_DIAGRAM_IDS: "t_diagramlinks_diagram_ids",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_CONNECTOR_IDS: "t_diagramlinks_connector_ids",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_GEOMETRIES: "t_diagramlinks_geometries",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_STYLES: "t_diagramlinks_styles",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_HIDDEN: "t_diagramlinks_hidden",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_PATHS: "t_diagramlinks_paths",
    EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_INSTANCE_IDS: "t_diagramlinks_instance_ids",
}
