import pandas


def delete_dataframe_from_dataframe_dictionary_in_hdf5_file(
    hdf_store_filename: str,
    dataframe_name: str,
):
    hdf_store = pandas.HDFStore(
        hdf_store_filename,
    )

    prefixed_dataframe_name = (
        "/" + dataframe_name
    )

    if (
        prefixed_dataframe_name
        not in hdf_store.keys()
    ):
        print(
            "No dataframe with name "
            + prefixed_dataframe_name
            + " in "
            + hdf_store_filename,
        )

        return

    hdf_store.remove(
        key=prefixed_dataframe_name,
    )

    hdf_store.close()
