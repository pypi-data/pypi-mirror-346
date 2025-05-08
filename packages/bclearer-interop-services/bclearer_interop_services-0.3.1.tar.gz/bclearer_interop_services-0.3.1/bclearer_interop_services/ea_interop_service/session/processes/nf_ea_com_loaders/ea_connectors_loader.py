from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.factories.i_dual_connector_factory import (
    create_i_dual_connector,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_connector import (
    IConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_null_connector import (
    INullConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_stereotypes_load_helper import (
    get_ea_stereotype_ex,
)
from pandas import DataFrame
from tqdm import tqdm


def load_ea_connectors(
    ea_connectors: DataFrame,
    stereotype_usage_with_names: DataFrame,
):
    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    ea_connector_name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    ea_connector_type_column_name = (
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
    )

    ea_object_place1_column_name = (
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
    )

    ea_object_place2_column_name = (
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
    )

    ea_connector_note_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name
    )

    for index, ea_connector_row in tqdm(
        ea_connectors.iterrows(),
        total=ea_connectors.shape[0],
    ):
        ea_connector = __load_ea_connector(
            nf_uuid=ea_connector_row[
                nf_uuids_column_name
            ],
            ea_connector_name=ea_connector_row[
                ea_connector_name_column_name
            ],
            ea_connector_type=ea_connector_row[
                ea_connector_type_column_name
            ],
            child_nf_uuid=ea_connector_row[
                ea_object_place1_column_name
            ],
            parent_nf_uuid=ea_connector_row[
                ea_object_place2_column_name
            ],
            note=ea_connector_row[
                ea_connector_note_column_name
            ],
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

        if isinstance(
            ea_connector, INullConnector
        ):
            ea_connectors.at[
                index,
                ea_guid_column_name,
            ] = DEFAULT_NULL_VALUE

        elif isinstance(
            ea_connector, IDualConnector
        ):
            ea_connectors.at[
                index,
                ea_guid_column_name,
            ] = (
                ea_connector.connector_guid
            )

    return ea_connectors


def __load_ea_connector(
    nf_uuid: str,
    ea_connector_name: str,
    ea_connector_type: str,
    child_nf_uuid: str,
    parent_nf_uuid: str,
    note: str,
    stereotype_usage_with_names: DataFrame,
) -> IConnector:
    child = NfUuidsToIDualObjectsMappings.get_i_dual_element(
        nf_uuid=child_nf_uuid
    )

    if not isinstance(
        child, IDualElement
    ):
        return INullConnector()

    parent = NfUuidsToIDualObjectsMappings.get_i_dual_element(
        nf_uuid=parent_nf_uuid
    )

    if not isinstance(
        parent, IDualElement
    ):
        return INullConnector()

    if (
        ea_connector_name
        == DEFAULT_NULL_VALUE
    ):
        ea_connector_name = None

    ea_connector_stereotype_ex = get_ea_stereotype_ex(
        client_nf_uuid=nf_uuid,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    ea_connector = create_i_dual_connector(
        child_object=child,
        parent_object=parent,
        connector_type=ea_connector_type,
        connector_name=ea_connector_name,
        ea_object_note=note,
        ea_connector_stereotype_ex=ea_connector_stereotype_ex,
    )

    NfUuidsToIDualObjectsMappings.map_nf_uuid_to_i_dual_connector(
        nf_uuid=nf_uuid,
        i_dual_connector=ea_connector,
    )

    return ea_connector
