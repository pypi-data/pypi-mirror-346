from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.attributes.nf_ea_attribute_remover import (
    remove_nf_ea_attribute,
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
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def delete_nf_ea_attribute_instances_for_type(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    attribute_type_ea_guid: str,
):
    ea_attribute_instances_dataframe = __get_ea_attribute_instances_dataframe(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        attribute_type_ea_guid=attribute_type_ea_guid,
    )

    for (
        ea_attribute_instances_tuple
    ) in (
        ea_attribute_instances_dataframe.itertuples()
    ):
        __remove_ea_attribute_instance(
            ea_attribute_instances_tuple=ea_attribute_instances_tuple,
            ea_repository=ea_repository,
        )


def __get_ea_attribute_instances_dataframe(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    attribute_type_ea_guid: str,
):
    ea_attributes = ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager.get_ea_attributes(
        ea_repository=ea_repository
    )

    attribute_type_nf_uuid = __get_nf_uuid_from_ea_guid(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
        ea_guid=attribute_type_ea_guid,
    )

    classifying_classifier_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name
    )

    ea_attribute_instances_dataframe = ea_attributes.loc[
        ea_attributes[
            classifying_classifier_column_name
        ]
        == attribute_type_nf_uuid
    ]

    log_message(
        "Attribute type: "
        + attribute_type_ea_guid
        + " has "
        + str(
            ea_attribute_instances_dataframe.shape[
                0
            ]
        )
        + " instances"
    )

    return (
        ea_attribute_instances_dataframe
    )


def __remove_ea_attribute_instance(
    ea_attribute_instances_tuple: tuple,
    ea_repository: EaRepositories,
):
    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    attribute_ea_guid = getattr(
        ea_attribute_instances_tuple,
        ea_guid_column_name,
    )

    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    remove_nf_ea_attribute(
        i_dual_repository=i_dual_repository,
        ea_attribute_guid=attribute_ea_guid,
    )


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
