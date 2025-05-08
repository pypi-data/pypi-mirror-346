from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.factories.i_dual_element_factory import (
    create_i_dual_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from pandas import DataFrame
from tqdm import tqdm


def load_ea_proxy_connectors(
    ea_proxy_connectors: DataFrame,
):
    nf_uuid_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    type_column_name = (
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
    )

    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    parent_column_name = (
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
    )

    classifier_column_name = (
        NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name
    )

    for (
        index,
        ea_classifier_row,
    ) in tqdm(
        ea_proxy_connectors.iterrows(),
        total=ea_proxy_connectors.shape[
            0
        ],
    ):
        ea_classifier = __load_ea_proxy_connector(
            nf_uuid=ea_classifier_row[
                nf_uuid_column_name
            ],
            ea_package_parent_nf_uuid=ea_classifier_row[
                parent_column_name
            ],
            ea_proxy_connector_name=ea_classifier_row[
                name_column_name
            ],
            ea_proxy_connector_type=ea_classifier_row[
                type_column_name
            ],
            ea_classifier_nf_uuid=ea_classifier_row[
                classifier_column_name
            ],
        )

        ea_proxy_connectors.at[
            index, ea_guid_column_name
        ] = ea_classifier.element_guid

    return ea_proxy_connectors


def __load_ea_proxy_connector(
    nf_uuid: str,
    ea_package_parent_nf_uuid: str,
    ea_proxy_connector_name: str,
    ea_proxy_connector_type: str,
    ea_classifier_nf_uuid: str,
) -> IDualElement:
    ea_package_parent = NfUuidsToIDualObjectsMappings.get_i_dual_package(
        nf_uuid=ea_package_parent_nf_uuid
    )

    ea_proxy_connector = create_i_dual_element(
        container=ea_package_parent,
        element_name=ea_proxy_connector_name,
        element_type=ea_proxy_connector_type,
    )

    ea_classifier = NfUuidsToIDualObjectsMappings.get_i_dual_connector(
        nf_uuid=ea_classifier_nf_uuid
    )

    if not isinstance(
        ea_classifier, IDualConnector
    ):
        raise TypeError

    ea_proxy_connector.classifier_id = (
        ea_classifier.connector_id
    )

    ea_proxy_connector.update()

    NfUuidsToIDualObjectsMappings.map_nf_uuid_to_i_dual_element(
        nf_uuid=nf_uuid,
        i_dual_element=ea_proxy_connector,
    )

    return ea_proxy_connector
