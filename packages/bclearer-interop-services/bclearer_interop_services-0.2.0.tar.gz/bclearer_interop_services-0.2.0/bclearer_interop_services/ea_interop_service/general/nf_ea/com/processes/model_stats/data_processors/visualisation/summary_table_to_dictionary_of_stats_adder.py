from pandas import DataFrame


def add_summary_table_to_dictionary_of_stats(
    stats_summary_table: DataFrame,
    dictionary_of_stats: dict,
    stats_summary_table_name: str,
) -> dict:
    stats_summary_table_as_dictionary = {
        stats_summary_table_name: stats_summary_table
    }

    dictionary_of_stats.update(
        stats_summary_table_as_dictionary
    )

    return dictionary_of_stats
