from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_dual_package import (
    IDualPackage,
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
from pandas import DataFrame, Series


def map_and_load_ea_packages(
    ea_packages: DataFrame,
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository: EaRepositories,
):
    ea_packages = ea_packages.fillna(
        DEFAULT_NULL_VALUE
    )

    __map_matched_ea_packages(
        ea_packages=ea_packages,
        ea_repository=ea_repository,
    )

    __load_unmatched_ea_packages(
        ea_packages=ea_packages,
        ea_tools_session_manager=ea_tools_session_manager,
    )


def __map_matched_ea_packages(
    ea_packages: DataFrame,
    ea_repository: EaRepositories,
):
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    nf_uuid_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    matched_ea_packages = (
        ea_packages.loc[
            ea_packages[
                ea_guids_column_name
            ]
            != DEFAULT_NULL_VALUE
        ]
    )

    log_message(
        "Mapping "
        + str(
            matched_ea_packages.shape[0]
        )
        + " packages"
    )

    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    for (
        index,
        ea_package_row,
    ) in matched_ea_packages.iterrows():
        __map_matched_ea_package(
            ea_package_row=ea_package_row,
            i_dual_repository=i_dual_repository,
            nf_uuid_column_name=nf_uuid_column_name,
            ea_guids_column_name=ea_guids_column_name,
        )


def __map_matched_ea_package(
    ea_package_row: Series,
    i_dual_repository: IDualRepository,
    nf_uuid_column_name: str,
    ea_guids_column_name: str,
):
    nf_uuid = ea_package_row[
        nf_uuid_column_name
    ]

    ea_guid = ea_package_row[
        ea_guids_column_name
    ]

    ea_package = i_dual_repository.get_package_by_guid(
        package_ea_guid=ea_guid
    )

    if not isinstance(
        ea_package, IDualPackage
    ):
        raise TypeError

    NfUuidsToIDualObjectsMappings.map_nf_uuid_to_i_dual_package(
        nf_uuid=nf_uuid,
        i_dual_package=ea_package,
    )


def __load_unmatched_ea_packages(
    ea_packages: DataFrame,
    ea_tools_session_manager: EaToolsSessionManagers,
):
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    unmatched_ea_packages = (
        ea_packages.loc[
            ea_packages[
                ea_guids_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    log_message(
        "Loading "
        + str(
            unmatched_ea_packages.shape[
                0
            ]
        )
        + " packages"
    )

    ea_tools_session_manager.load_ea_packages(
        ea_packages=unmatched_ea_packages
    )
