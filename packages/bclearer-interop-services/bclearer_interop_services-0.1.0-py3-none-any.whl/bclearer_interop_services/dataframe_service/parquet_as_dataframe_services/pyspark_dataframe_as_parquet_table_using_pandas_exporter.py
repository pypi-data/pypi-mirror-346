import os.path

import pyspark.sql
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


# TODO: to further work of collapsing the similar methods and parametrize the engine and the compression (for example)
def export_pyspark_dataframe_as_parquet_table_using_pandas(
    output_root_folder: Folders,
    pyspark_dataframe: pyspark.sql.DataFrame,
) -> None:
    pandas_dataframe = (
        pyspark_dataframe.toPandas()
    )

    if not os.path.exists(
        output_root_folder.absolute_path_string,
    ):
        os.makedirs(
            output_root_folder.absolute_path_string,
        )

    pandas_dataframe.to_parquet(
        path=output_root_folder.absolute_path_string
        + os.sep
        + "file.snappy.parquet_service",
        engine="auto",
        compression="snappy",
    )
