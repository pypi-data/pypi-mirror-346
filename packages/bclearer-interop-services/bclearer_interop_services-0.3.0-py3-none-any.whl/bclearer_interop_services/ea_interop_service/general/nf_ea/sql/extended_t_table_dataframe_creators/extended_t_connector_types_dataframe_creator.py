from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_standardiser import (
    fill_up_all_empty_cells_with_default_null_value,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.nf_identity_extender import (
    extend_with_identities,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def create_extended_t_connector_types_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    log_message(
        message="creating extended t_connector_types dataframe"
    )

    t_connector_types_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_CONNECTORTYPES,
    )

    extended_t_connector_types_dataframe = extend_with_identities(
        dataframe=t_connector_types_dataframe,
        universe_key=universe_key,
        collection_type_name="extended_t_connector_types",
    )

    extended_t_connector_types_dataframe[
        "t_connector_types_ea_guids"
    ] = None

    extended_t_connector_types_dataframe = fill_up_all_empty_cells_with_default_null_value(
        dataframe=extended_t_connector_types_dataframe
    )

    log_message(
        message="created extended object dataframe"
    )

    return extended_t_connector_types_dataframe
