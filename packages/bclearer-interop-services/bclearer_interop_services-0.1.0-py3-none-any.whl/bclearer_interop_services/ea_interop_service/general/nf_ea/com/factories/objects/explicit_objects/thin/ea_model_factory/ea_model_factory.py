from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
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
from pandas import DataFrame


def get_ea_models(
    nf_ea_com_universe,
) -> DataFrame:
    ea_models = (
        nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_packages()
    )

    extended_t_object_dataframe = nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
        ea_repository=nf_ea_com_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
    )

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    ea_models = left_merge_dataframes(
        master_dataframe=ea_models,
        master_dataframe_key_columns=[
            nf_uuids_column_name
        ],
        merge_suffixes=[
            "_model",
            "_object",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            nf_uuids_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            nf_uuids_column_name: "nullable"
        },
    )

    ea_models = ea_models.fillna(
        DEFAULT_NULL_VALUE
    )

    ea_models = ea_models.loc[
        ea_models["nullable"]
        == DEFAULT_NULL_VALUE
    ]

    ea_models.drop(
        labels="nullable",
        axis=1,
        inplace=True,
    )

    extended_t_package_dataframe = nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
        ea_repository=nf_ea_com_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.EXTENDED_T_PACKAGE,
    )

    package_ea_guid_column_name = (
        EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
    )

    ea_models = left_merge_dataframes(
        master_dataframe=ea_models,
        master_dataframe_key_columns=[
            package_ea_guid_column_name
        ],
        merge_suffixes=[
            "_model",
            "_package",
        ],
        foreign_key_dataframe=extended_t_package_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            "package_names_0": "ea_model_names"
        },
    )

    ea_models["ea_model_notes"] = (
        DEFAULT_NULL_VALUE
    )

    return ea_models
