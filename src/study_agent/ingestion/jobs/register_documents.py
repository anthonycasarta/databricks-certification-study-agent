from argparse import ArgumentParser

from pyspark.sql import DataFrame, SparkSession


def ensure_metadata_table_exists(
    spark: SparkSession,
    catalog_name: str,
    schema_name: str,
) -> None:

    spark.sql(
        f"""
        create table if not exists {catalog_name}.{schema_name}.document_metadata (
            document_id string,
            file_name string,
            file_path string,
            file_type string,
            file_size_bytes bigint,
            content_hash string,
            ingested_at timestamp,
            status string
            )
            using delta;
        """
    )


def read_raw_documents_stream(
    spark: SparkSession,
    catalog_name: str,
    schema_name: str,
) -> DataFrame:
    data_frame = spark.readStream.table(f"{catalog_name}.{schema_name}.documents_raw")
    return data_frame


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument("--catalog-name", required=True)
    parser.add_argument("--schema-name", required=True)

    args = parser.parse_args()

    spark = SparkSession.active()
    ensure_metadata_table_exists(
        spark,
        args.catalog_name,
        args.schema_name,
    )


if __name__ == "__main__":
    main()
