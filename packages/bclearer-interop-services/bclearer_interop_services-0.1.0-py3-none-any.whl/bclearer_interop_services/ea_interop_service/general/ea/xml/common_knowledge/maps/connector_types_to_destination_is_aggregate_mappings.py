from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)

__map = {
    EaConnectorTypes.GENERALIZATION.type_name: "0",
    EaConnectorTypes.DEPENDENCY.type_name: "0",
    EaConnectorTypes.ASSOCIATION.type_name: "0",
    EaConnectorTypes.AGGREGATION.type_name: "2",
    EaConnectorTypes.REALISATION.type_name: "0",
    EaConnectorTypes.NOTE_LINK.type_name: "0",
}


def get_destination_is_aggregate_from_connector_type(
    connector_type: str,
) -> str:
    return __map[connector_type]
