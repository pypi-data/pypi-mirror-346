from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTDiagramobjectsColumnTypes(
    EaTColumnTypes
):
    T_DIAGRAMOBJECTS_DIAGRAM_IDS = (
        auto()
    )
    T_DIAGRAMOBJECTS_OBJECT_IDS = auto()
    T_DIAGRAMOBJECTS_RECT_TOPS = auto()
    T_DIAGRAMOBJECTS_RECT_LEFTS = auto()
    T_DIAGRAMOBJECTS_RECT_RIGHTS = (
        auto()
    )
    T_DIAGRAMOBJECTS_RECT_BOTTOMS = (
        auto()
    )
    T_DIAGRAMOBJECTS_SEQUENCES = auto()
    T_DIAGRAMOBJECTS_OBJECT_STYLES = (
        auto()
    )
    T_DIAGRAMOBJECTS_INSTANCE_IDS = (
        auto()
    )

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
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_DIAGRAM_IDS: "Diagram_ID",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_OBJECT_IDS: "Object_ID",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_TOPS: "RectTop",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_LEFTS: "RectLeft",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_RIGHTS: "RectRight",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_BOTTOMS: "RectBottom",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_SEQUENCES: "Sequence",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_OBJECT_STYLES: "ObjectStyle",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_INSTANCE_IDS: "Instance_ID",
}


nf_column_name_mapping = {
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_DIAGRAM_IDS: "t_diagramobjects_diagram_ids",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_OBJECT_IDS: "t_diagramobjects_object_ids",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_TOPS: "t_diagramobjects_rect_tops",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_LEFTS: "t_diagramobjects_rect_lefts",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_RIGHTS: "t_diagramobjects_rect_rights",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_RECT_BOTTOMS: "t_diagramobjects_rect_bottoms",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_SEQUENCES: "t_diagramobjects_sequences",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_OBJECT_STYLES: "t_diagramobjects_object_styles",
    EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_INSTANCE_IDS: "t_diagramobjects_instance_ids",
}
