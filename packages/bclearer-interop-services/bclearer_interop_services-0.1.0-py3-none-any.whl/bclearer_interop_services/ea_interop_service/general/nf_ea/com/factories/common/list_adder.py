import numpy
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from pandas import DataFrame


def add_list(
    master_dataframe: DataFrame,
    foreign_key_dataframe: DataFrame,
    foreign_key_dataframe_fk_columns: list,
    master_dataframe_new_column_name: str,
) -> DataFrame:
    if foreign_key_dataframe.empty:
        return __add_empty_column(
            master_dataframe=master_dataframe,
            master_dataframe_new_column_name=master_dataframe_new_column_name,
        )

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    master_dataframe_with_list_items = left_merge_dataframes(
        master_dataframe=master_dataframe,
        master_dataframe_key_columns=[
            nf_uuids_column_name
        ],
        merge_suffixes=[
            "_master",
            "_foreign",
        ],
        foreign_key_dataframe=foreign_key_dataframe,
        foreign_key_dataframe_fk_columns=foreign_key_dataframe_fk_columns,
        foreign_key_dataframe_other_column_rename_dictionary={
            nf_uuids_column_name: master_dataframe_new_column_name
        },
    )

    nf_uuids_with_list = master_dataframe_with_list_items.groupby(
        nf_uuids_column_name
    )[
        master_dataframe_new_column_name
    ].apply(
        list
    )

    nf_uuids_with_list = (
        nf_uuids_with_list.reset_index()
    )

    nf_uuids_with_list[
        master_dataframe_new_column_name
    ] = nf_uuids_with_list[
        master_dataframe_new_column_name
    ].apply(
        lambda nf_uuids_list: (
            []
            if nf_uuids_list
            == [numpy.nan]
            else nf_uuids_list
        )
    )

    master_dataframe = left_merge_dataframes(
        master_dataframe=master_dataframe,
        master_dataframe_key_columns=[
            nf_uuids_column_name
        ],
        merge_suffixes=[
            "_element",
            "_list",
        ],
        foreign_key_dataframe=nf_uuids_with_list,
        foreign_key_dataframe_fk_columns=[
            nf_uuids_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            master_dataframe_new_column_name: master_dataframe_new_column_name
        },
    )

    return master_dataframe


def __add_empty_column(
    master_dataframe: DataFrame,
    master_dataframe_new_column_name: str,
) -> DataFrame:
    master_dataframe[
        master_dataframe_new_column_name
    ] = numpy.nan

    master_dataframe[
        master_dataframe_new_column_name
    ] = master_dataframe[
        master_dataframe_new_column_name
    ].apply(
        lambda nf_uuids_list: (
            []
            if nf_uuids_list
            == numpy.nan
            else []
        )
    )

    return master_dataframe
