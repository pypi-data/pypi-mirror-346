from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame, concat


def add_classifier_column_to_extended_t_object_dataframe(
    nf_ea_sql_universe,
) -> DataFrame:
    log_message(
        message="adding classifier to t_object dataframe"
    )

    extended_t_object_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT
    )

    extended_t_connector_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR
    )

    extended_t_object_dataframe = __extend_extended_t_object_dataframe_with_classifier_data(
        extended_t_object_dataframe=extended_t_object_dataframe,
        extended_t_connector_dataframe=extended_t_connector_dataframe,
    )

    log_message(
        message="added classifier to t_object dataframe"
    )

    return extended_t_object_dataframe


def __extend_extended_t_object_dataframe_with_classifier_data(
    extended_t_object_dataframe: DataFrame,
    extended_t_connector_dataframe: DataFrame,
) -> DataFrame:
    extended_t_object_non_proxy_connectors_dataframe_with_classifier_column = __extend_filtered_extended_t_object_with_classifier_column(
        extended_t_object_dataframe=extended_t_object_dataframe,
        classifier_dataframe=extended_t_object_dataframe,
        classifier_dataframe_ea_guid_column_name=EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name,
        is_proxy_connector=False,
    )

    extended_t_object_proxy_connectors_dataframe_with_classifier_column = __extend_filtered_extended_t_object_with_classifier_column(
        extended_t_object_dataframe=extended_t_object_dataframe,
        classifier_dataframe=extended_t_connector_dataframe,
        classifier_dataframe_ea_guid_column_name=EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name,
        is_proxy_connector=True,
    )

    extended_t_object_dataframe = concat(
        [
            extended_t_object_non_proxy_connectors_dataframe_with_classifier_column,
            extended_t_object_proxy_connectors_dataframe_with_classifier_column,
        ]
    )

    extended_t_object_dataframe = extended_t_object_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return extended_t_object_dataframe


def __extend_filtered_extended_t_object_with_classifier_column(
    extended_t_object_dataframe: DataFrame,
    classifier_dataframe: DataFrame,
    classifier_dataframe_ea_guid_column_name: str,
    is_proxy_connector: bool,
) -> DataFrame:
    object_type_column_name = (
        EaTObjectColumnTypes.T_OBJECT_TYPES.nf_column_name
    )

    if is_proxy_connector:
        filtered_extended_t_objects = extended_t_object_dataframe.loc[
            extended_t_object_dataframe[
                object_type_column_name
            ]
            == EaElementTypes.PROXY_CONNECTOR.type_name
        ]
    else:
        filtered_extended_t_objects = extended_t_object_dataframe.loc[
            extended_t_object_dataframe[
                object_type_column_name
            ]
            != EaElementTypes.PROXY_CONNECTOR.type_name
        ]

    filtered_extended_t_objects = left_merge_dataframes(
        master_dataframe=filtered_extended_t_objects,
        master_dataframe_key_columns=[
            EaTObjectColumnTypes.T_OBJECT_CLASSIFIER_GUIDS.nf_column_name
        ],
        merge_suffixes=[
            "_master",
            "_linked",
        ],
        foreign_key_dataframe=classifier_dataframe,
        foreign_key_dataframe_fk_columns=[
            classifier_dataframe_ea_guid_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "t_object_classifier_nf_uuids"
        },
    )

    return filtered_extended_t_objects
