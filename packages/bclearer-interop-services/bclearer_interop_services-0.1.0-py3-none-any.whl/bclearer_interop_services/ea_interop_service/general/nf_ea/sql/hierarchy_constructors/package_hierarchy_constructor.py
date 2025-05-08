from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def construct_package_hierarchy_dataframe(
    nf_ea_sql_universe,
) -> DataFrame:
    log_message(
        message="creating package_hierarchy dataframe"
    )

    t_package_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_PACKAGE,
    )

    package_hierarchy_dataframe = (
        t_package_dataframe.copy()
    )

    package_hierarchy_dataframe = package_hierarchy_dataframe.rename(
        columns={
            EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name: "package_ids_0",
            EaTPackageColumnTypes.T_PACKAGE_NAMES.nf_column_name: "package_names_0",
            EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS.nf_column_name: "package_ids_1",
        }
    )

    package_hierarchy_dataframe[
        "paths"
    ] = package_hierarchy_dataframe[
        "package_names_0"
    ]

    level = 0

    while (
        package_hierarchy_dataframe[
            "package_names_"
            + str(level)
        ].nunique()
        > 1
    ):
        level = level + 1

        package_hierarchy_dataframe = __add_level_to_hierarchy(
            level=level,
            package_hierarchy_dataframe=package_hierarchy_dataframe,
            t_package_dataframe=t_package_dataframe,
        )

    log_message(
        message="created package_hierarchy dataframe"
    )

    return package_hierarchy_dataframe


def __add_level_to_hierarchy(
    level: int,
    package_hierarchy_dataframe: DataFrame,
    t_package_dataframe: DataFrame,
):
    package_hierarchy_dataframe = left_merge_dataframes(
        master_dataframe=package_hierarchy_dataframe,
        master_dataframe_key_columns=[
            "package_ids_" + str(level)
        ],
        merge_suffixes=[
            "_" + str(level - 1),
            "_" + str(level),
        ],
        foreign_key_dataframe=t_package_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name: "package_ea_guids_"
            + str(level),
            EaTPackageColumnTypes.T_PACKAGE_NAMES.nf_column_name: "package_names_"
            + str(level),
            EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS.nf_column_name: "package_ids_"
            + str(level + 1),
        },
    )

    package_hierarchy_dataframe = package_hierarchy_dataframe.fillna(
        value=DEFAULT_NULL_VALUE
    )

    package_hierarchy_dataframe[
        "paths"
    ] = package_hierarchy_dataframe.apply(
        lambda row: (
            row["paths"]
            if row[
                "package_names_"
                + str(level)
            ]
            == DEFAULT_NULL_VALUE
            else row[
                "package_names_"
                + str(level)
            ]
            + "/"
            + row["paths"]
        ),
        axis=1,
    )

    return package_hierarchy_dataframe
