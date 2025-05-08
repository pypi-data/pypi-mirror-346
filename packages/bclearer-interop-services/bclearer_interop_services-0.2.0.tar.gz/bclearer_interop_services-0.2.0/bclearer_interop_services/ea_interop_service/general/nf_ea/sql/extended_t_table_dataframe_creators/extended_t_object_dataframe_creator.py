from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.nf_identity_extender import (
    extend_with_identities,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.stereotypes_extender import (
    extend_with_stereotypes_data,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_object_column_types import (
    ExtendedTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_property_types import (
    EaPropertyTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def create_extended_t_object_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    log_message(
        message="creating extended t_object dataframe"
    )

    t_object_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_OBJECT,
    )

    extended_t_object_dataframe = extend_with_identities(
        dataframe=t_object_dataframe,
        universe_key=universe_key,
        collection_type_name="extended_t_objects",
    )

    extended_t_package_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_PACKAGE
    )

    extended_t_object_dataframe = __extend_with_package_data(
        extended_t_object_dataframe=extended_t_object_dataframe,
        extended_t_package_dataframe=extended_t_package_dataframe,
    )

    extended_t_object_dataframe = __extend_with_object_data(
        extended_t_object_dataframe=extended_t_object_dataframe
    )

    extended_t_object_dataframe = extend_with_stereotypes_data(
        dataframe=extended_t_object_dataframe,
        ea_guid_column_name=EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name,
        nf_ea_sql_universe=nf_ea_sql_universe,
        type_filter_text=EaPropertyTypes.ELEMENT_PROPERTY.type_name,
    )

    extended_t_object_dataframe[
        ExtendedTObjectColumnTypes.T_OBJECT_EA_HUMAN_READABLE_NAMES.column_name
    ] = (
        "("
        + extended_t_object_dataframe[
            EaTObjectColumnTypes.T_OBJECT_TYPES.nf_column_name
        ]
        + ") "
        + extended_t_object_dataframe[
            EaTObjectColumnTypes.T_OBJECT_NAMES.nf_column_name
        ]
    )

    log_message(
        message="created extended t_object dataframe"
    )

    return extended_t_object_dataframe


def __extend_with_object_data(
    extended_t_object_dataframe: DataFrame,
) -> DataFrame:
    extended_t_object_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_object_dataframe,
        master_dataframe_key_columns=[
            EaTObjectColumnTypes.T_OBJECT_PARENT_IDS.nf_column_name
        ],
        merge_suffixes=[
            "_master",
            "_linked",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "t_object_parent_nf_uuids"
        },
    )

    extended_t_object_dataframe = extended_t_object_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return extended_t_object_dataframe


def __extend_with_package_data(
    extended_t_object_dataframe: DataFrame,
    extended_t_package_dataframe: DataFrame,
) -> DataFrame:
    extended_t_object_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_object_dataframe,
        master_dataframe_key_columns=[
            EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS.nf_column_name
        ],
        merge_suffixes=[
            "_object",
            "_package",
        ],
        foreign_key_dataframe=extended_t_package_dataframe,
        foreign_key_dataframe_fk_columns=[
            "package_ids_0"
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            "paths": ExtendedTObjectColumnTypes.T_OBJECT_PATHS.column_name,
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name: "t_object_package_ea_guids",
        },
    )

    extended_t_object_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_object_dataframe,
        master_dataframe_key_columns=[
            "t_object_package_ea_guids"
        ],
        merge_suffixes=[
            "_master",
            "_linked",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "t_object_package_nf_uuids"
        },
    )

    extended_t_object_dataframe = extended_t_object_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return extended_t_object_dataframe
