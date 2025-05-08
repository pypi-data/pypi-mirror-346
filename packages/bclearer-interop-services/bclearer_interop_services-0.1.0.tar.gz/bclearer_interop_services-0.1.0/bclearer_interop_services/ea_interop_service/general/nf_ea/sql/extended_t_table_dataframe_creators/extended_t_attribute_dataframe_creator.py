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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
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


def create_extended_t_attribute_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    log_message(
        message="creating extended t_attribute dataframe"
    )

    t_attribute_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_ATTRIBUTE,
    )

    extended_t_object_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT
    )

    extended_t_attribute_dataframe = extend_with_identities(
        dataframe=t_attribute_dataframe,
        universe_key=universe_key,
        collection_type_name="extended_t_objects",
    )

    extended_t_attribute_dataframe = __extend_with_object_data(
        t_attribute_dataframe=extended_t_attribute_dataframe,
        extended_t_object_dataframe=extended_t_object_dataframe,
    )

    extended_t_attribute_dataframe = __extend_with_type_data(
        extended_t_attribute_dataframe=extended_t_attribute_dataframe,
        extended_t_object_dataframe=extended_t_object_dataframe,
    )

    extended_t_attribute_dataframe = extend_with_stereotypes_data(
        dataframe=extended_t_attribute_dataframe,
        ea_guid_column_name=EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS.nf_column_name,
        nf_ea_sql_universe=nf_ea_sql_universe,
        type_filter_text=EaPropertyTypes.ATTRIBUTE_PROPERTY.type_name,
    )

    extended_t_attribute_dataframe[
        "t_attribute_ea_human_readable_names"
    ] = (
        "(attribute) "
        + extended_t_attribute_dataframe[
            "attributed_t_object_names"
        ]
        + "."
        + extended_t_attribute_dataframe[
            EaTAttributeColumnTypes.T_ATTRIBUTE_NAMES.nf_column_name
        ]
    )

    log_message(
        message="created extended t_attribute dataframe"
    )

    return (
        extended_t_attribute_dataframe
    )


def __extend_with_object_data(
    t_attribute_dataframe: DataFrame,
    extended_t_object_dataframe: DataFrame,
) -> DataFrame:
    extended_t_attribute_dataframe = left_merge_dataframes(
        master_dataframe=t_attribute_dataframe,
        master_dataframe_key_columns=[
            EaTAttributeColumnTypes.T_ATTRIBUTE_OBJECT_IDS.nf_column_name
        ],
        merge_suffixes=[
            "_attribute",
            "_object",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "attributed_t_object_nf_uuids",
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name: "attributed_t_object_ea_guids",
            EaTObjectColumnTypes.T_OBJECT_NAMES.nf_column_name: "attributed_t_object_names",
            ExtendedTObjectColumnTypes.T_OBJECT_PATHS.column_name: "attributed_t_object_paths",
            "t_object_package_ea_guids": "t_attribute_package_ea_guids",
        },
    )

    return (
        extended_t_attribute_dataframe
    )


def __extend_with_type_data(
    extended_t_attribute_dataframe: DataFrame,
    extended_t_object_dataframe: DataFrame,
) -> DataFrame:
    extended_t_attribute_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_attribute_dataframe,
        master_dataframe_key_columns=[
            EaTAttributeColumnTypes.T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS.nf_column_name
        ],
        merge_suffixes=[
            "_attribute",
            "_object",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "t_attribute_classifiers_t_object_nf_uuids",
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name: "t_attribute_classifiers_t_object_ea_guids",
            EaTObjectColumnTypes.T_OBJECT_NAMES.nf_column_name: "t_attribute_classifiers_t_object_names",
            ExtendedTObjectColumnTypes.T_OBJECT_PATHS.column_name: "t_attribute_classifiers_t_object_paths",
            "t_object_package_ea_guids": "t_attribute_classifiers_package_ea_guids",
        },
    )

    return (
        extended_t_attribute_dataframe
    )
