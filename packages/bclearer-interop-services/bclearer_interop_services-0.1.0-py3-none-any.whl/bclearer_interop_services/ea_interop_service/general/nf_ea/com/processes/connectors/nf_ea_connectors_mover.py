from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.tuple_service.tuple_attribute_value_getter import (
    get_tuple_attribute_value_if_required,
)
from pandas import DataFrame


def move_nf_ea_connectors(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    input_dataframe: DataFrame,
):
    input_dataframe = (
        input_dataframe.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    for (
        input_tuple
    ) in input_dataframe.itertuples():
        __move_nf_ea_connectors_using_input_tuple(
            ea_tools_session_manager=ea_tools_session_manager,
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __move_nf_ea_connectors_using_input_tuple(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    from_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="from_guid",
    )

    to_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="to_guid",
    )

    single_other_end_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="single_other_end_guid",
    )

    connector_type = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="connector_type",
    )

    direction = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="direction",
    )

    __move_nf_ea_connectors_from_classifier(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        from_guid=from_guid,
        to_guid=to_guid,
        single_other_end_guid=single_other_end_guid,
        connector_type=connector_type,
        direction=direction,
    )


def __move_nf_ea_connectors_from_classifier(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    from_guid: str,
    to_guid: str,
    single_other_end_guid: str,
    connector_type: str,
    direction: str,
):
    connectors_to_move = __get_connectors_to_move(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        from_guid=from_guid,
        single_other_end_guid=single_other_end_guid,
        connector_type=connector_type,
        direction=direction,
    )

    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    to_element = i_dual_repository.get_element_by_guid(
        element_ea_guid=to_guid
    )

    if not isinstance(
        to_element, IDualElement
    ):
        raise TypeError

    for (
        connector_tuple
    ) in (
        connectors_to_move.itertuples()
    ):
        __move_nf_ea_connector(
            i_dual_repository=i_dual_repository,
            connector_tuple=connector_tuple,
            to_element_id=to_element.element_id,
            direction=direction,
        )


def __get_connectors_to_move(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    from_guid: str,
    single_other_end_guid: str,
    connector_type: str,
    direction: str,
) -> DataFrame:
    ea_connectors = ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager.get_ea_connectors(
        ea_repository=ea_repository
    )

    ea_connector_type_column_name = (
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
    )

    typed_ea_connectors = ea_connectors.loc[
        ea_connectors[
            ea_connector_type_column_name
        ]
        == connector_type
    ]

    if direction == "Incoming":
        connector_end_column_name = (
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        )

    else:
        connector_end_column_name = (
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        )

    from_nf_uuid = __get_nf_uuid_from_ea_guid(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        ea_guid=from_guid,
    )

    connectors_to_move = typed_ea_connectors.loc[
        typed_ea_connectors[
            connector_end_column_name
        ]
        == from_nf_uuid
    ]

    if (
        single_other_end_guid
        == DEFAULT_NULL_VALUE
    ):
        return connectors_to_move

    if direction == "Incoming":
        connector_end_column_name = (
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        )

    else:
        connector_end_column_name = (
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        )

    other_nf_uuid = __get_nf_uuid_from_ea_guid(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        ea_guid=single_other_end_guid,
    )

    connectors_to_move = connectors_to_move.loc[
        connectors_to_move[
            connector_end_column_name
        ]
        == other_nf_uuid
    ]

    return connectors_to_move


def __get_nf_uuid_from_ea_guid(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    ea_guid: str,
):
    ea_classifiers = ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager.get_ea_classifiers(
        ea_repository=ea_repository
    )

    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    from_ea_classifier = (
        ea_classifiers.loc[
            ea_classifiers[
                ea_guid_column_name
            ]
            == ea_guid
        ]
    )

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    from_ea_classifier_nf_uuid = (
        from_ea_classifier.iloc[0][
            nf_uuids_column_name
        ]
    )

    return from_ea_classifier_nf_uuid


def __move_nf_ea_connector(
    i_dual_repository: IDualRepository,
    connector_tuple: tuple,
    to_element_id: int,
    direction: str,
):
    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    connector_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=connector_tuple,
        attribute_name=ea_guid_column_name,
    )

    i_dual_connector = i_dual_repository.get_connector_by_guid(
        connector_ea_guid=connector_ea_guid
    )

    if not isinstance(
        i_dual_connector, IDualConnector
    ):
        raise TypeError

    if direction == "Incoming":
        i_dual_connector.supplier_id = (
            to_element_id
        )

    else:
        i_dual_connector.client_id = (
            to_element_id
        )

    i_dual_connector.update()
