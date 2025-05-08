from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)

__map = {
    EaConnectorTypes.GENERALIZATION.type_name: "Source -> Destination",
    EaConnectorTypes.DEPENDENCY.type_name: "Source -> Destination",
    EaConnectorTypes.ASSOCIATION.type_name: "Source -> Destination",
    EaConnectorTypes.AGGREGATION.type_name: "Source -> Destination",
    EaConnectorTypes.REALISATION.type_name: "Source -> Destination",
    EaConnectorTypes.NOTE_LINK.type_name: "Source -> Destination",
}


def get_direction_string_from_connector_type(
    connector_type: str,
) -> str:
    return __map[connector_type]
