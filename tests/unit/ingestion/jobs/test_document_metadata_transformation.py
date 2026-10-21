from datetime import datetime
from uuid import UUID

from pyspark.sql import DataFrame, SparkSession
from pyspark.testing.utils import assertDataFrameEqual
from pytest import fixture

from study_agent.ingestion.jobs.register_documents import build_document_metadata
from study_agent.ingestion.metadata import calculate_content_hash


@fixture
def sample_document_df(spark: SparkSession) -> DataFrame:
    delta_path = "/Volumes/study_agent/bronze/source_documents/delta.md"
    study_guide_path = "/Volumes/study_agent/bronze/source_documents/study_guide.PDF"

    document_df = spark.createDataFrame(
        [
            (
                delta_path,
                908,
                b"Sample Markdown content",
            ),
            (
                study_guide_path,
                1024,
                b"Sample PDF content",
            ),
        ],
        ["path", "length", "content"],
    )

    return document_df


@fixture
def expected_document_metadata_df(spark: SparkSession) -> DataFrame:
    """Create expected metadata containing only deterministic fields.

    Excludes document_id and ingested_at because their values are
    generated dynamically and validated separately.
    """
    delta_content_hash = calculate_content_hash(b"Sample Markdown content")
    study_guide_content_hash = calculate_content_hash(b"Sample PDF content")
    document_metadata_df = spark.createDataFrame(
        [
            (
                "delta.md",
                "/Volumes/study_agent/bronze/source_documents/delta.md",
                "md",
                908,
                delta_content_hash,
            ),
            (
                "study_guide.PDF",
                "/Volumes/study_agent/bronze/source_documents/study_guide.PDF",
                "pdf",
                1024,
                study_guide_content_hash,
            ),
        ],
        [
            "file_name",
            "file_path",
            "file_type",
            "file_size_bytes",
            "content_hash",
        ],
    )

    return document_metadata_df


def test_metadata_columns_structure(sample_document_df: DataFrame) -> None:
    metadata_df = build_document_metadata(sample_document_df)

    assert len(metadata_df.columns) == 7
    assert "document_id" in metadata_df.columns
    assert "file_name" in metadata_df.columns
    assert "file_path" in metadata_df.columns
    assert "file_type" in metadata_df.columns
    assert "file_size_bytes" in metadata_df.columns
    assert "content_hash" in metadata_df.columns
    assert "ingested_at" in metadata_df.columns


def test_documents_metadata_columns_values(
    expected_document_metadata_df: DataFrame,
    sample_document_df: DataFrame,
) -> None:
    deterministic_columns = [
        "file_name",
        "file_path",
        "file_type",
        "file_size_bytes",
        "content_hash",
    ]

    actual_document_metadata_df = build_document_metadata(sample_document_df)
    assertDataFrameEqual(
        actual_document_metadata_df.select(*deterministic_columns),
        expected_document_metadata_df,
    )

    actual_document_metadata_rows = actual_document_metadata_df.collect()
    for row in actual_document_metadata_rows:
        assert UUID(row["document_id"]).version == 4
        assert isinstance(row["ingested_at"], datetime)

    document_ids = [row["document_id"] for row in actual_document_metadata_rows]
    assert len(document_ids) == len(set(document_ids))
    assert len(actual_document_metadata_rows) == 2
