import numpy
from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_operation_column_types import (
    EaTOperationColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_property_types import (
    EaPropertyTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame, concat


def create_object_stereotypes_dataframe(
    nf_ea_sql_universe,
) -> DataFrame:
    log_message(
        message="creating object_stereotypes dataframe"
    )

    t_xref_extended_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_XREF
    )

    object_stereotypes_dataframe = __filter_to_stereotype_usages(
        t_xref_extended_dataframe=t_xref_extended_dataframe
    )

    object_stereotypes_dataframe = __convert_description_to_list_of_guids(
        object_stereotypes_dataframe=object_stereotypes_dataframe
    )

    object_stereotypes_dataframe = __convert_list_of_guids_to_rows(
        object_stereotypes_dataframe=object_stereotypes_dataframe
    )

    object_stereotypes_dataframe = __add_nf_uuids(
        object_stereotypes_dataframe=object_stereotypes_dataframe,
        nf_ea_sql_universe=nf_ea_sql_universe,
    )

    log_message(
        message="created object_stereotypes dataframe"
    )

    return object_stereotypes_dataframe


def __filter_to_stereotype_usages(
    t_xref_extended_dataframe: DataFrame,
) -> DataFrame:
    object_stereotypes_dataframe = t_xref_extended_dataframe.loc[
        t_xref_extended_dataframe[
            EaTXrefColumnTypes.T_XREF_NAMES.nf_column_name
        ]
        == "Stereotypes"
    ]

    object_stereotypes_dataframe = object_stereotypes_dataframe.loc[
        (
            object_stereotypes_dataframe[
                EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name
            ]
            == EaPropertyTypes.CONNECTOR_PROPERTY.type_name
        )
        | (
            object_stereotypes_dataframe[
                EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name
            ]
            == EaPropertyTypes.ELEMENT_PROPERTY.type_name
        )
        | (
            object_stereotypes_dataframe[
                EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name
            ]
            == EaPropertyTypes.ATTRIBUTE_PROPERTY.type_name
        )
    ]

    object_stereotypes_dataframe = object_stereotypes_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return object_stereotypes_dataframe


def __convert_description_to_list_of_guids(
    object_stereotypes_dataframe: DataFrame,
) -> DataFrame:
    object_stereotypes_dataframe[
        "t_xref_descriptions_as_list"
    ] = object_stereotypes_dataframe[
        EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name
    ].apply(
        lambda x: x.split(";")
    )

    object_stereotypes_dataframe[
        "guids_texts"
    ] = object_stereotypes_dataframe[
        "t_xref_descriptions_as_list"
    ].apply(
        lambda text_items: [
            text_item
            for text_item in text_items
            if text_item.startswith(
                "GUID"
            )
        ]
    )

    object_stereotypes_dataframe[
        ExtendedTObjectColumnTypes.LIST_OF_STEREOTYPE_GUIDS.column_name
    ] = object_stereotypes_dataframe[
        "guids_texts"
    ].apply(
        lambda guid_items: __remove_guid_name_from_guid_items(
            guid_items
        )
    )

    return object_stereotypes_dataframe


def __remove_guid_name_from_guid_items(
    guid_items: list,
) -> list:
    for index in range(len(guid_items)):
        guid_items[index] = guid_items[
            index
        ][5:43]

    return guid_items


def __convert_list_of_guids_to_rows(
    object_stereotypes_dataframe: DataFrame,
) -> DataFrame:
    list_column_name = (
        "list_of_stereotype_guids"
    )

    empty_expanded_list_dataframe = DataFrame(
        {
            column: numpy.repeat(
                object_stereotypes_dataframe[
                    column
                ].values,
                object_stereotypes_dataframe[
                    list_column_name
                ].str.len(),
            )
            for column in object_stereotypes_dataframe.columns.drop(
                list_column_name
            )
        }
    )

    if (
        object_stereotypes_dataframe.shape[
            0
        ]
        == 0
    ):
        return DataFrame(
            columns=[
                EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
                "stereotype_guids",
                EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name,
            ]
        )

    expanded_list_array = numpy.concatenate(
        object_stereotypes_dataframe[
            list_column_name
        ].values
    )

    expanded_list_dataframe = empty_expanded_list_dataframe.assign(
        **{
            list_column_name: expanded_list_array
        }
    )

    expanded_list_dataframe = expanded_list_dataframe.filter(
        items=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
            "list_of_stereotype_guids",
            EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name,
        ]
    )

    expanded_list_dataframe = expanded_list_dataframe.rename(
        columns={
            "list_of_stereotype_guids": "stereotype_guids",
            EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name: NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name,
        }
    )

    return expanded_list_dataframe


def __add_nf_uuids(
    object_stereotypes_dataframe: DataFrame,
    nf_ea_sql_universe,
) -> DataFrame:
    extended_t_object_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT
    )

    object_stereotype_usage_dataframe = __add_collection_type_objects_to_usage_dataframe(
        object_stereotypes_dataframe=object_stereotypes_dataframe,
        extended_collection_type_dataframe=extended_t_object_dataframe,
        collection_type_ea_guid_nf_column_name=EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name,
    )

    extended_t_connector_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR
    )

    connector_stereotype_usage_dataframe = __add_collection_type_objects_to_usage_dataframe(
        object_stereotypes_dataframe=object_stereotypes_dataframe,
        extended_collection_type_dataframe=extended_t_connector_dataframe,
        collection_type_ea_guid_nf_column_name=EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name,
    )

    extended_t_attribute_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_ATTRIBUTE
    )

    attribute_stereotype_usage_dataframe = __add_collection_type_objects_to_usage_dataframe(
        object_stereotypes_dataframe=object_stereotypes_dataframe,
        extended_collection_type_dataframe=extended_t_attribute_dataframe,
        collection_type_ea_guid_nf_column_name=EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS.nf_column_name,
    )

    extended_t_operation_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OPERATION
    )

    operation_stereotype_usage_dataframe = __add_collection_type_objects_to_usage_dataframe(
        object_stereotypes_dataframe=object_stereotypes_dataframe,
        extended_collection_type_dataframe=extended_t_operation_dataframe,
        collection_type_ea_guid_nf_column_name=EaTOperationColumnTypes.T_OPERATION_EA_GUIDS.nf_column_name,
    )

    nf_uuids_object_stereotypes_dataframe = concat(
        [
            object_stereotype_usage_dataframe,
            connector_stereotype_usage_dataframe,
            attribute_stereotype_usage_dataframe,
            operation_stereotype_usage_dataframe,
        ]
    )

    object_stereotypes_dataframe = left_merge_dataframes(
        master_dataframe=object_stereotypes_dataframe,
        master_dataframe_key_columns=[
            "stereotype_guids",
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
        ],
        merge_suffixes=[
            "_usage",
            "_client",
        ],
        foreign_key_dataframe=nf_uuids_object_stereotypes_dataframe,
        foreign_key_dataframe_fk_columns=[
            "stereotype_guids",
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name: NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        },
    )

    extended_t_stereotypes_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_STEREOTYPES
    )

    object_stereotypes_dataframe = left_merge_dataframes(
        master_dataframe=object_stereotypes_dataframe,
        master_dataframe_key_columns=[
            "stereotype_guids"
        ],
        merge_suffixes=[
            "_usage",
            "_stereotype",
        ],
        foreign_key_dataframe=extended_t_stereotypes_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTStereotypesColumnTypes.T_STEREOTYPES_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: "stereotype_nf_uuids"
        },
    )

    return object_stereotypes_dataframe


def __add_collection_type_objects_to_usage_dataframe(
    object_stereotypes_dataframe: DataFrame,
    extended_collection_type_dataframe: DataFrame,
    collection_type_ea_guid_nf_column_name: str,
) -> DataFrame:
    collection_type_object_stereotypes_dataframe = inner_merge_dataframes(
        master_dataframe=object_stereotypes_dataframe,
        master_dataframe_key_columns=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name
        ],
        merge_suffixes=[
            "_usage",
            "_collection_type",
        ],
        foreign_key_dataframe=extended_collection_type_dataframe,
        foreign_key_dataframe_fk_columns=[
            collection_type_ea_guid_nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfColumnTypes.NF_UUIDS.column_name: NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        },
    )

    collection_type_object_stereotypes_dataframe = dataframe_filter_and_rename(
        dataframe=collection_type_object_stereotypes_dataframe,
        filter_and_rename_dictionary={
            "stereotype_guids": "stereotype_guids",
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name: EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name: NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name,
        },
    )

    return collection_type_object_stereotypes_dataframe
