from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_object_column_types import (
    ExtendedTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def create_extended_t_xref_dataframe(
    nf_ea_sql_universe,
) -> DataFrame:
    log_message(
        message="creating extended t_xref dataframe"
    )

    t_xref_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_XREF,
    )

    extended_t_object_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT
    )

    extended_t_xref_dataframe = __extend_with_object_data(
        t_xref_dataframe=t_xref_dataframe,
        extended_t_object_dataframe=extended_t_object_dataframe,
    )

    extended_t_connector_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR
    )

    extended_t_xref_dataframe = __extend_with_connector_data(
        extended_t_xref_dataframe=extended_t_xref_dataframe,
        extended_t_connector_dataframe=extended_t_connector_dataframe,
    )

    extended_t_xref_dataframe[
        "t_xref_ea_human_readable_names"
    ] = (
        "(xref"
        + "-"
        + extended_t_xref_dataframe[
            EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name
        ]
        + "-"
        + extended_t_xref_dataframe[
            EaTXrefColumnTypes.T_XREF_NAMES.nf_column_name
        ]
        + ") "
        + extended_t_xref_dataframe[
            "t_xref_t_object_names"
        ]
    )

    log_message(
        message="created extended t_xref dataframe"
    )

    return extended_t_xref_dataframe


def __extend_with_object_data(
    t_xref_dataframe: DataFrame,
    extended_t_object_dataframe: DataFrame,
) -> DataFrame:
    extended_t_xref_dataframe = left_merge_dataframes(
        master_dataframe=t_xref_dataframe,
        master_dataframe_key_columns=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name
        ],
        merge_suffixes=[
            "_xref",
            "_object",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name: "t_xref_t_object_ea_guids",
            EaTObjectColumnTypes.T_OBJECT_NAMES.nf_column_name: "t_xref_t_object_names",
            ExtendedTObjectColumnTypes.T_OBJECT_PATHS.column_name: "t_xref_container_paths",
        },
    )

    extended_t_xref_dataframe = extended_t_xref_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return extended_t_xref_dataframe


def __extend_with_connector_data(
    extended_t_xref_dataframe: DataFrame,
    extended_t_connector_dataframe: DataFrame,
) -> DataFrame:
    extended_t_xref_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_xref_dataframe,
        master_dataframe_key_columns=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name
        ],
        merge_suffixes=[
            "_xref",
            "_connector",
        ],
        foreign_key_dataframe=extended_t_connector_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            "start_t_object_paths": "t_xref_t_connector_start_paths"
        },
    )

    extended_t_xref_dataframe[
        "t_xref_container_paths"
    ] = extended_t_xref_dataframe.apply(
        lambda row: (
            row[
                "t_xref_t_connector_start_paths"
            ]
            if row[
                "t_xref_container_paths"
            ]
            == DEFAULT_NULL_VALUE
            else row[
                "t_xref_container_paths"
            ]
        ),
        axis=1,
    )

    extended_t_xref_dataframe = extended_t_xref_dataframe.drop(
        columns=[
            "t_xref_t_connector_start_paths"
        ]
    )

    return extended_t_xref_dataframe
