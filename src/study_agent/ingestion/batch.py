from pyspark.sql import DataFrame, SparkSession


def read_documents(spark: SparkSession, load_path: str) -> DataFrame:
    data_frame = spark.read.format("binaryFile").load(load_path)

    return data_frame
