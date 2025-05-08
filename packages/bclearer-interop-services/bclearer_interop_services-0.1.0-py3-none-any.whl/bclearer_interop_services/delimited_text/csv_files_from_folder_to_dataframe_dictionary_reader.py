import os

import pandas


def read_csv_files_from_folder_to_dataframe_dictionary(
    folder: str,
) -> dict:
    dataframe_dictionary = dict()

    csv_files = (
        __get_all_csv_files_from_folder(
            folder,
        )
    )

    for csv_file in csv_files:
        dataframe_dictionary = (
            __add_dataframe(
                csv_file,
                folder,
                dataframe_dictionary,
            )
        )

    return dataframe_dictionary


def __get_all_csv_files_from_folder(
    folder: str,
) -> list:
    csv_files = list()

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            csv_files.append(file)
    return csv_files


def __add_dataframe(
    csv_file: str,
    folder_name: str,
    dataframe_dictionary: dict,
) -> dict:
    dataframe_name = csv_file.replace(
        ".csv",
        "",
    )

    csv_path = os.path.join(
        folder_name,
        csv_file,
    )

    dataframe = pandas.read_csv(
        filepath_or_buffer=csv_path,
    )

    dataframe_dictionary.update(
        {dataframe_name: dataframe},
    )

    return dataframe_dictionary
