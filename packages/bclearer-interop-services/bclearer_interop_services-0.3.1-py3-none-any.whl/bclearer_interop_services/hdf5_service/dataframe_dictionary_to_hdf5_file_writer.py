import pandas


def write_dataframe_dictionary_to_hdf5_file(
    hdf5_file_name: str,
    dataframes_dictionary: dict,
):
    hdf_store = pandas.HDFStore(
        hdf5_file_name,
    )

    for (
        key,
        value,
    ) in dataframes_dictionary.items():
        hdf_store.put(
            key,
            value,
            format="fixed",
            data_columns=True,
        )

    hdf_store.close()
