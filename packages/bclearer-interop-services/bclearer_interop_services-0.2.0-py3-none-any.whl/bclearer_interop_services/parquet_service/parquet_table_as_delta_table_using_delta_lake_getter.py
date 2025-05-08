from deltalake import DeltaTable


def get_parquet_table_as_delta_table_using_delta_lake(
    absolute_table_name_folder_path: str,
) -> DeltaTable:
    delta_table = DeltaTable(
        absolute_table_name_folder_path,
    )

    return delta_table
