from pathlib import Path
from urllib.parse import urlparse

from pyspark.sql import SparkSession
from pytest import fixture

from study_agent.ingestion.batch import read_documents


@fixture
def sample_documents(tmp_path: Path) -> Path:
    volume_path = tmp_path / "Volumes" / "study_agent" / "bronze" / "source_documents"

    volume_path.mkdir(parents=True)

    (volume_path / "delta.md").write_text("Delta Lake supports ACID transactions.")
    (volume_path / "spark.pdf").write_text("Apache Spark is a processing engine.")

    return volume_path


def test_read_documents_return_file_content(
    spark: SparkSession, sample_documents: Path
) -> None:

    df = read_documents(spark, str(sample_documents))

    actual_filenames = {Path(urlparse(row.path).path).name for row in df.collect()}

    expected_filenames = {file.name for file in sample_documents.iterdir()}

    assert actual_filenames == expected_filenames
