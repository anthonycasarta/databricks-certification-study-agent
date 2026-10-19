from datetime import datetime, timedelta
from uuid import UUID

from pytest import raises

from study_agent.ingestion.metadata import (
    calculate_content_hash,
    determine_file_type,
    extract_file_name,
    generate_document_id,
    generate_ingestion_timestamp,
)


def test_wrong_file_extension_raises_value_error():
    with raises(ValueError):
        determine_file_type("image.png")


def test_file_name_without_extension():
    with raises(ValueError):
        determine_file_type("image")


def test_same_input_produces_same_hash():
    a = b"This is content one."
    b = b"This is content one."

    first_hash_pair = calculate_content_hash(a)
    second_hash_pair = calculate_content_hash(b)

    assert first_hash_pair == second_hash_pair


def test_different_input_produces_different_hash():
    a = b"This is content one."
    b = b"This is content two."

    first_hash = calculate_content_hash(a)
    second_hash = calculate_content_hash(b)

    assert first_hash != second_hash


def test_hash_contains_sixty_four_characters():
    a = b"This is content one."
    b = b"This is content two."

    first_hash = calculate_content_hash(a)
    second_hash = calculate_content_hash(b)

    assert len(first_hash) == 64
    assert len(second_hash) == 64


def test_generated_document_id_is_a_string():
    generated_id = generate_document_id()

    assert isinstance(generated_id, str)


def test_generated_document_id_produces_different_uuid_for_each_call():
    first_generated_id = generate_document_id()
    second_generated_id = generate_document_id()

    assert first_generated_id != second_generated_id


def test_generated_id_is_a_valid_uuid4():
    generated_id = generate_document_id()
    parsed_uuid = UUID(generated_id)

    assert parsed_uuid.version == 4


def test_extract_file_name_from_absolute_path():
    path = "/Volumes/study_agent/bronze/source_documents/delta.md"
    extracted_file_name = extract_file_name(path)
    expected_file_name = "delta.md"

    assert extracted_file_name == expected_file_name


def test_extracted_file_name_from_nested_path():
    path = "/Volumes/study_agent/bronze/source_documents/notes/spark.md"
    extracted_file_name = extract_file_name(path)
    expected_file_name = "spark.md"

    assert extracted_file_name == expected_file_name


def test_extracted_file_name_from_filename():
    path = "document.md"
    extracted_file_name = extract_file_name(path)
    expected_file_name = "document.md"

    assert extracted_file_name == expected_file_name


def test_ingestion_timestamp_returns_datetime():
    timestamp = generate_ingestion_timestamp()

    assert isinstance(timestamp, datetime)


def test_ingestion_timestamp_is_utc():
    timestamp = generate_ingestion_timestamp()

    assert timestamp.utcoffset() == timedelta(0)


def test_ingestion_timestamp_is_timezone_aware():
    timestamp = generate_ingestion_timestamp()

    assert timestamp.tzinfo is not None
