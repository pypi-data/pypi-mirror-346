from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


def extend_with_stereotypes_data(
    dataframe: DataFrame,
    ea_guid_column_name: str,
    nf_ea_sql_universe,
    type_filter_text: str,
) -> DataFrame:
    stereotypes_dataframe = __get_stereotypes_dataframe(
        nf_ea_sql_universe=nf_ea_sql_universe,
        type_filter_text=type_filter_text,
    )

    dataframe = left_merge_dataframes(
        master_dataframe=dataframe,
        master_dataframe_key_columns=[
            ea_guid_column_name
        ],
        merge_suffixes=[
            "_master",
            "_stereotype",
        ],
        foreign_key_dataframe=stereotypes_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name: EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name,
            "list_of_stereotype_guids": "list_of_stereotype_guids",
        },
    )

    for row in dataframe.loc[
        dataframe[
            "list_of_stereotype_guids"
        ].isnull(),
        "list_of_stereotype_guids",
    ].index:
        dataframe.at[
            row,
            "list_of_stereotype_guids",
        ] = []

    return dataframe


def __get_stereotypes_dataframe(
    nf_ea_sql_universe,
    type_filter_text: str,
) -> DataFrame:
    stereotypes_dataframe = __get_base_stereotypes_dataframe(
        nf_ea_sql_universe=nf_ea_sql_universe,
        type_filter_text=type_filter_text,
    )

    stereotypes_dataframe = __convert_description_to_list_of_guids(
        stereotypes_dataframe=stereotypes_dataframe
    )

    return stereotypes_dataframe


def __get_base_stereotypes_dataframe(
    nf_ea_sql_universe,
    type_filter_text: str,
) -> DataFrame:
    t_xref_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_XREF,
    )

    base_stereotypes_dataframe = t_xref_dataframe.loc[
        t_xref_dataframe[
            EaTXrefColumnTypes.T_XREF_NAMES.nf_column_name
        ]
        == "Stereotypes"
    ]

    base_stereotypes_dataframe = base_stereotypes_dataframe.loc[
        base_stereotypes_dataframe[
            EaTXrefColumnTypes.T_XREF_TYPES.nf_column_name
        ]
        == type_filter_text
    ]

    base_stereotypes_dataframe = base_stereotypes_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    return base_stereotypes_dataframe


def __convert_description_to_list_of_guids(
    stereotypes_dataframe: DataFrame,
) -> DataFrame:
    stereotypes_dataframe[
        "t_xref_descriptions_as_list"
    ] = stereotypes_dataframe[
        EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.nf_column_name
    ].apply(
        lambda x: x.split(";")
    )

    stereotypes_dataframe[
        "guids_texts"
    ] = stereotypes_dataframe[
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

    stereotypes_dataframe[
        "list_of_stereotype_guids"
    ] = stereotypes_dataframe[
        "guids_texts"
    ].apply(
        lambda guid_items: __remove_guid_name_from_guid_items(
            guid_items
        )
    )

    return stereotypes_dataframe


def __remove_guid_name_from_guid_items(
    guid_items: list,
) -> list:
    for index in range(len(guid_items)):
        guid_items[index] = guid_items[
            index
        ][5:43]

    return guid_items
