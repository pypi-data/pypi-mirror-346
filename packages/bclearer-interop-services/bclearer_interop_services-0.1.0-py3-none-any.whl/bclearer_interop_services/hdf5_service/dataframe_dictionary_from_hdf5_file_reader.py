import pandas


def read_dataframe_dictionary_from_hdf5_file(
    hdf_store_filename: str,
) -> dict:
    hdf_store = pandas.HDFStore(
        hdf_store_filename,
    )

    dataframes_dictionary = {}

    for key in hdf_store.keys():
        dataframes_dictionary = __add_dataframe_to_dictionary(
            hdf_store=hdf_store,
            key=key[1:],
            dataframes_dictionary=dataframes_dictionary,
        )

    hdf_store.close()

    return dataframes_dictionary


def __add_dataframe_to_dictionary(
    hdf_store: pandas.HDFStore,
    key: str,
    dataframes_dictionary: dict,
) -> dict:
    dataframe = hdf_store.select(key)

    dataframes_dictionary[key] = (
        dataframe
    )

    return dataframes_dictionary
