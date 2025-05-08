from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTConnectorColumnTypes(
    EaTColumnTypes
):
    T_CONNECTOR_IDS = auto()
    T_CONNECTOR_NAMES = auto()
    T_CONNECTOR_DIRECTIONS = auto()
    T_CONNECTOR_TYPES = auto()
    T_CONNECTOR_START_OBJECT_IDS = (
        auto()
    )
    T_CONNECTOR_END_OBJECT_IDS = auto()
    T_CONNECTOR_STEREOTYPES = auto()
    T_CONNECTOR_EA_GUIDS = auto()
    T_CONNECTOR_SOURCE_STYLES = auto()
    T_CONNECTOR_DEST_STYLES = auto()
    T_CONNECTOR_SOURCE_IS_AGGREGATE = (
        auto()
    )
    T_CONNECTOR_DEST_IS_AGGREGATE = (
        auto()
    )
    T_CONNECTOR_LINE_STYLES = auto()
    T_CONNECTOR_ROUTE_STYLES = auto()
    T_CONNECTOR_IS_BOLD = auto()
    T_CONNECTOR_LINE_COLORS = auto()
    T_CONNECTOR_SOURCE_CARDINALITIES = (
        auto()
    )
    T_CONNECTOR_DEST_CARDINALITIES = (
        auto()
    )
    T_CONNECTOR_NOTES = auto()

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
    EaTConnectorColumnTypes.T_CONNECTOR_IDS: "Connector_ID",
    EaTConnectorColumnTypes.T_CONNECTOR_NAMES: "Name",
    EaTConnectorColumnTypes.T_CONNECTOR_DIRECTIONS: "Direction",
    EaTConnectorColumnTypes.T_CONNECTOR_TYPES: "Connector_Type",
    EaTConnectorColumnTypes.T_CONNECTOR_START_OBJECT_IDS: "Start_Object_ID",
    EaTConnectorColumnTypes.T_CONNECTOR_END_OBJECT_IDS: "End_Object_ID",
    EaTConnectorColumnTypes.T_CONNECTOR_STEREOTYPES: "Stereotype",
    EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS: "ea_guid",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_STYLES: "SourceStyle",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_STYLES: "DestStyle",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_IS_AGGREGATE: "SourceIsAggregate",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_IS_AGGREGATE: "DestIsAggregate",
    EaTConnectorColumnTypes.T_CONNECTOR_LINE_STYLES: "LineStyle",
    EaTConnectorColumnTypes.T_CONNECTOR_ROUTE_STYLES: "RouteStyle",
    EaTConnectorColumnTypes.T_CONNECTOR_IS_BOLD: "IsBold",
    EaTConnectorColumnTypes.T_CONNECTOR_LINE_COLORS: "LineColor",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_CARDINALITIES: "SourceCard",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_CARDINALITIES: "DestCard",
    EaTConnectorColumnTypes.T_CONNECTOR_NOTES: "Notes",
}


nf_column_name_mapping = {
    EaTConnectorColumnTypes.T_CONNECTOR_IDS: "t_connector_ids",
    EaTConnectorColumnTypes.T_CONNECTOR_NAMES: "t_connector_names",
    EaTConnectorColumnTypes.T_CONNECTOR_DIRECTIONS: "t_connector_directions",
    EaTConnectorColumnTypes.T_CONNECTOR_TYPES: "t_connector_types",
    EaTConnectorColumnTypes.T_CONNECTOR_START_OBJECT_IDS: "t_connector_start_object_ids",
    EaTConnectorColumnTypes.T_CONNECTOR_END_OBJECT_IDS: "t_connector_end_object_ids",
    EaTConnectorColumnTypes.T_CONNECTOR_STEREOTYPES: "t_connector_stereotypes",
    EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS: "t_connector_ea_guids",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_STYLES: "t_connector_source_styles",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_STYLES: "t_connector_dest_styles",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_IS_AGGREGATE: "t_connector_source_is_aggregate",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_IS_AGGREGATE: "t_connector_dest_is_aggregate",
    EaTConnectorColumnTypes.T_CONNECTOR_LINE_STYLES: "t_connector_line_styles",
    EaTConnectorColumnTypes.T_CONNECTOR_ROUTE_STYLES: "t_connector_route_styles",
    EaTConnectorColumnTypes.T_CONNECTOR_IS_BOLD: "t_connector_is_bold",
    EaTConnectorColumnTypes.T_CONNECTOR_LINE_COLORS: "t_connector_line_colors",
    EaTConnectorColumnTypes.T_CONNECTOR_SOURCE_CARDINALITIES: "t_connector_source_cardinalities",
    EaTConnectorColumnTypes.T_CONNECTOR_DEST_CARDINALITIES: "t_connector_dest_cardinalities",
    EaTConnectorColumnTypes.T_CONNECTOR_NOTES: "t_connector_notes",
}
