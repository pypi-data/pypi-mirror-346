from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_uuidifier import (
    uuidify_dataframe,
)


def uuidify_dictionary_of_dataframes(
    dictionary_of_dataframes: dict,
    uuid_column_name: str,
) -> dict:
    dictionary_of_uuidified_dataframes = (
        {}
    )

    for (
        dataframe_name,
        dataframe,
    ) in (
        dictionary_of_dataframes.items()
    ):
        dictionary_of_uuidified_dataframes[
            dataframe_name
        ] = uuidify_dataframe(
            dataframe=dataframe,
            uuid_column_name=uuid_column_name,
        )

    return dictionary_of_uuidified_dataframes
