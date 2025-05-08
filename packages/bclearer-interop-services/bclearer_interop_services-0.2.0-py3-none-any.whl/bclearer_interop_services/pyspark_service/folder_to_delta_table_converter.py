import pyspark.sql
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.pyspark_service.pyspark_delta_catalog_session_getter import (
    get_pyspark_delta_catalog_session,
)
from delta.tables import DeltaTable


def convert_folder_to_delta_table(
    output_root_folder: Folders,
    spark_session: pyspark.sql.SparkSession = None,
) -> None:
    if not spark_session:
        spark_session = (
            get_pyspark_delta_catalog_session()
        )

    DeltaTable.convertToDelta(
        spark_session,
        f"parquet_service.`{output_root_folder.absolute_path_string}`",
    )

    if not DeltaTable.isDeltaTable(
        spark_session,
        output_root_folder.absolute_path_string,
    ):
        raise Exception
