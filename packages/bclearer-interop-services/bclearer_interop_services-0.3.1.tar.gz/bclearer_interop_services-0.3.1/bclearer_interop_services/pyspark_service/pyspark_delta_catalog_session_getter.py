import pyspark
from delta.pip_utils import (
    configure_spark_with_delta_pip,
)


def get_pyspark_delta_catalog_session() -> (
    pyspark.sql.session
):
    builder = (
        pyspark.sql.SparkSession.builder.appName(
            "MyApp",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config(
            "spark.sql.debug.maxToStringFields",
            1000,
        )
    )

    spark_session = (
        configure_spark_with_delta_pip(
            builder,
        ).getOrCreate()
    )

    return spark_session
