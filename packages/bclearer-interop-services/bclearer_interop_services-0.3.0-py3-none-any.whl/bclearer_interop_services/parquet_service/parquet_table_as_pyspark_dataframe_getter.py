import pyspark


def get_parquet_table_as_pyspark_dataframe(
    spark_session: pyspark.sql.session,
    absolute_table_name_folder_path: str,
    number_of_rows_to_keep: int,
) -> pyspark.sql.DataFrame:
    parquet_table_as_pyspark_dataframe = spark_session.read.parquet(
        absolute_table_name_folder_path,
    ).limit(
        number_of_rows_to_keep,
    )

    return parquet_table_as_pyspark_dataframe
