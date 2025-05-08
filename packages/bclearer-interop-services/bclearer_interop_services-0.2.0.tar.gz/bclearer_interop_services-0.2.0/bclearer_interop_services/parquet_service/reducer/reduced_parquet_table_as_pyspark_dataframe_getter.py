import pyspark
from bclearer_interop_services.parquet_service.parquet_table_as_pyspark_dataframe_getter import (
    get_parquet_table_as_pyspark_dataframe,
)


def get_reduced_parquet_table_as_pyspark_dataframe(
    spark_session: pyspark.sql.SparkSession,
    number_of_rows_to_keep: int,
    parquet_folder_path: str,
) -> pyspark.sql.DataFrame:
    reduced_parquet_table_as_pyspark_dataframe = get_parquet_table_as_pyspark_dataframe(
        spark_session=spark_session,
        absolute_table_name_folder_path=parquet_folder_path,
        number_of_rows_to_keep=number_of_rows_to_keep,
    )

    repartitioned_parquet_table_as_pyspark_dataframe = reduced_parquet_table_as_pyspark_dataframe.repartition(
        numPartitions=1,
    )

    return repartitioned_parquet_table_as_pyspark_dataframe
