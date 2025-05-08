from bclearer_interop_services.dataframe_service.parquet_as_dataframe_services.pandas_dataframe_as_parquet_table_using_fastparquet_exporter import (
    export_pandas_dataframe_as_parquet_table_using_fastparquet,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.parquet_service.reducer.reduced_parquet_table_as_pandas_dataframe_getter import (
    get_reduced_parquet_table_as_pandas_dataframe,
)
from bclearer_interop_services.pyspark_service.folder_to_delta_table_converter import (
    convert_folder_to_delta_table,
)


def reduce_and_export_parquet_table_as_pandas_dataframe_using_fastparquet(
    number_of_rows_to_keep: int,
    parquet_folder_path: str,
    output_root_folder: Folders,
) -> None:
    reduced_parquet_table_as_pandas_dataframe = get_reduced_parquet_table_as_pandas_dataframe(
        number_of_rows_to_keep=number_of_rows_to_keep,
        parquet_folder_path=parquet_folder_path,
    )

    export_pandas_dataframe_as_parquet_table_using_fastparquet(
        output_root_folder=output_root_folder,
        pandas_dataframe=reduced_parquet_table_as_pandas_dataframe,
    )

    convert_folder_to_delta_table(
        output_root_folder=output_root_folder,
    )
