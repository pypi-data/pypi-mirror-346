from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from pandas import DataFrame


def convert_mapper_objects_to_table(
    mapper_objects: set,
) -> DataFrame:
    table_as_dictionary = dict()

    for mapper_object in mapper_objects:
        table_as_dictionary[
            mapper_object
        ] = vars(mapper_object)

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary,
    )

    table_as_dataframe = (
        table_as_dataframe.astype(str)
    )

    table_as_dataframe.drop_duplicates(
        inplace=True,
        ignore_index=True,
    )

    return table_as_dataframe
