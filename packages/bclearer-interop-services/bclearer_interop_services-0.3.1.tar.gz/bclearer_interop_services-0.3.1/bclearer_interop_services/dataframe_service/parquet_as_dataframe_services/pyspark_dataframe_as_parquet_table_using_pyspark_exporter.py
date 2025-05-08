import os

import pyspark.sql
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


# TODO: to further work of collapsing the similar methods and parametrize the engine and the compression (for example)
def export_pyspark_dataframe_as_parquet_table_using_pyspark(
    output_root_folder: Folders,
    pyspark_dataframe: pyspark.sql.DataFrame,
) -> None:
    if not os.path.exists(
        output_root_folder.absolute_path_string,
    ):
        os.makedirs(
            output_root_folder.absolute_path_string,
        )

    pyspark_dataframe.write.save(
        path=output_root_folder.absolute_path_string,
        format="delta",
        mode="overwrite",
        overwriteSchema=True,
    )
