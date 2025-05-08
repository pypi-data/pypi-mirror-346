from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.stereotypes.ea_model_load_helper import (
    get_stereotype_usage_with_names_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.attribute_reorderers.ea_attributes_reorderer import (
    reorder_ea_attributes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_attributes_loader import (
    map_and_load_ea_attributes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_classifiers_loader import (
    map_and_load_ea_classifiers,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_connectors_loader import (
    map_and_load_ea_connectors,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_packges_loader import (
    map_and_load_ea_packages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_proxy_connectors_loader import (
    map_and_load_ea_proxy_connectors,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.ea_interop_loader.object_loaders.ea_stereotypes_loader import (
    map_and_load_ea_stereotypes,
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


def orchestrate_ea_model_loader(
    nf_ea_com_dataframes_dictionary: dict,
):
    with EaToolsSessionManagers() as ea_tools_session_manager:
        ea_repository = (
            ea_tools_session_manager.create_ea_repository()
        )

        i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
            ea_repository=ea_repository
        )

        __turn_on_performance_flags(
            i_dual_repository=i_dual_repository
        )

        __map_and_load_ea_project(
            ea_tools_session_manager=ea_tools_session_manager,
            ea_repository=ea_repository,
            nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary,
        )

        __turn_off_performance_flags(
            i_dual_repository=i_dual_repository
        )


def __map_and_load_ea_project(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
    nf_ea_com_dataframes_dictionary: dict,
):
    stereotype_usage_with_names = get_stereotype_usage_with_names_dataframe(
        nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary
    )

    map_and_load_ea_stereotypes(
        ea_stereotypes=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_STEREOTYPES
        ],
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
    )

    map_and_load_ea_packages(
        ea_packages=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_PACKAGES
        ],
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
    )

    map_and_load_ea_classifiers(
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        stereotype_usage_with_names=stereotype_usage_with_names,
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository=ea_repository,
    )

    map_and_load_ea_attributes(
        ea_attributes=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_ATTRIBUTES
        ],
        ea_tools_session_manager=ea_tools_session_manager,
    )

    reorder_ea_attributes(
        ea_attributes_order=nf_ea_com_dataframes_dictionary[
            "ea_attributes_order"
        ],
        ea_tools_session_manager=ea_tools_session_manager,
    )

    map_and_load_ea_connectors(
        ea_connectors=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CONNECTORS
        ],
        stereotype_usage_with_names=stereotype_usage_with_names,
        ea_tools_session_manager=ea_tools_session_manager,
    )

    map_and_load_ea_proxy_connectors(
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        ea_tools_session_manager=ea_tools_session_manager,
    )

    map_and_load_ea_connectors(
        ea_connectors=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CONNECTORS_PC
        ],
        stereotype_usage_with_names=stereotype_usage_with_names,
        ea_tools_session_manager=ea_tools_session_manager,
    )


def __turn_on_performance_flags(
    i_dual_repository: IDualRepository,
):
    i_dual_repository.batch_append = (
        True
    )

    i_dual_repository.enable_ui_updates = (
        False
    )


def __turn_off_performance_flags(
    i_dual_repository: IDualRepository,
):
    i_dual_repository.batch_append = (
        False
    )

    i_dual_repository.enable_ui_updates = (
        True
    )

    __refresh_ea_project(
        i_dual_repository=i_dual_repository
    )


def __refresh_ea_project(
    i_dual_repository: IDualRepository,
):
    for index in range(
        i_dual_repository.models.count
    ):
        __refresh_ea_model(
            i_dual_repository=i_dual_repository,
            index=index,
        )


def __refresh_ea_model(
    i_dual_repository: IDualRepository,
    index: int,
):
    ea_model = (
        i_dual_repository.models.get_at(
            index
        )
    )

    i_dual_repository.refresh_model_view(
        ea_model.package_id
    )
