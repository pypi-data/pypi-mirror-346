from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def map_and_load_ea_proxy_connectors(
    ea_classifiers: DataFrame,
    ea_tools_session_manager: EaToolsSessionManagers,
):
    ea_classifiers = (
        ea_classifiers.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    __load_unmatched_ea_proxy_connectors(
        ea_classifiers=ea_classifiers,
        ea_tools_session_manager=ea_tools_session_manager,
    )


def __load_unmatched_ea_proxy_connectors(
    ea_classifiers: DataFrame,
    ea_tools_session_manager: EaToolsSessionManagers,
):
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    type_column_name = (
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
    )

    unmatched_ea_proxy_connectors = (
        ea_classifiers.loc[
            ea_classifiers[
                ea_guids_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    unmatched_ea_proxy_connectors = unmatched_ea_proxy_connectors.loc[
        ea_classifiers[type_column_name]
        == EaElementTypes.PROXY_CONNECTOR.type_name
    ]

    log_message(
        "Loading "
        + str(
            unmatched_ea_proxy_connectors.shape[
                0
            ]
        )
        + " proxy connectors"
    )

    ea_tools_session_manager.load_ea_proxy_connectors(
        ea_proxy_connectors=unmatched_ea_proxy_connectors
    )
