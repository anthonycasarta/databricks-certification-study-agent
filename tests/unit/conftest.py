from collections.abc import Iterator

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> Iterator[SparkSession]:
    # Use local[1] to minimize CPU overhead and speed up tests
    # Disable the Spark UI to save memory and processing time
    spark_session = (
        SparkSession.builder.master("local[1]")
        .appName("pyspark-unit-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark_session
    spark_session.stop()
