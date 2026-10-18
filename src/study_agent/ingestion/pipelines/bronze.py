from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession


@dp.table(name="documents_raw", comment="Raw study documents")
def documents_raw() -> DataFrame:
    spark = SparkSession.active()
    load_path = spark.conf.get("source_documents_path")

    data_frame = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "binaryFile")
        .load(load_path)
    )

    return data_frame
