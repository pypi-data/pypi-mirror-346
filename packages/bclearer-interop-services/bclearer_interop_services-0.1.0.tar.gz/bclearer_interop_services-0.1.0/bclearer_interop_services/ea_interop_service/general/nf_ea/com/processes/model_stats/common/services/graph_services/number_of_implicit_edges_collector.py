def get_number_of_implicit_edges(
    dictionary_of_dataframes: dict,
    dictionary_of_dataframes_table_name: str,
) -> str:
    temporary_implicit_edges_dataframe = dictionary_of_dataframes[
        dictionary_of_dataframes_table_name
    ].index

    number_of_implicit_edges = str(
        len(
            temporary_implicit_edges_dataframe
        )
    )
    return number_of_implicit_edges
