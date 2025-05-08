from bclearer_interop_services.dataframe_service.parquet_as_dataframe_services.pyspark_dataframe_as_parquet_table_using_pandas_exporter import (
    export_pyspark_dataframe_as_parquet_table_using_pandas,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.parquet_service.reducer.reduced_parquet_table_as_pyspark_dataframe_getter import (
    get_reduced_parquet_table_as_pyspark_dataframe,
)
from bclearer_interop_services.pyspark_service.folder_to_delta_table_converter import (
    convert_folder_to_delta_table,
)
from bclearer_interop_services.pyspark_service.pyspark_delta_catalog_session_getter import (
    get_pyspark_delta_catalog_session,
)


def reduce_and_export_parquet_table_as_pyspark_dataframe_using_pandas(
    number_of_rows_to_keep: int,
    parquet_folder_path: str,
    output_root_folder: Folders,
) -> None:
    spark_session = (
        get_pyspark_delta_catalog_session()
    )

    reduced_parquet_table_as_pyspark_dataframe = get_reduced_parquet_table_as_pyspark_dataframe(
        spark_session=spark_session,
        number_of_rows_to_keep=number_of_rows_to_keep,
        parquet_folder_path=parquet_folder_path,
    )

    export_pyspark_dataframe_as_parquet_table_using_pandas(
        output_root_folder=output_root_folder,
        pyspark_dataframe=reduced_parquet_table_as_pyspark_dataframe,
    )

    convert_folder_to_delta_table(
        output_root_folder=output_root_folder,
        spark_session=spark_session,
    )
